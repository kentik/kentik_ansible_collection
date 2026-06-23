#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sync NetBox devices, sites, and labels to Kentik.

Execution order:
  1. Sites  – ensure every NetBox site exists in Kentik (create if missing).
  2. Devices – create or update every NetBox device in Kentik.
  3. Labels  – create role/tenant/tag labels, then assign them to devices.

Configuration (env vars or CLI flags):
  KENTIK_EMAIL          Kentik API email             --kentik-email
  KENTIK_TOKEN          Kentik API token             --kentik-token
  NETBOX_URL            NetBox base URL              --netbox-url
  NETBOX_TOKEN          NetBox API token             --netbox-token
  KENTIK_PLAN_NAME      Kentik plan name             --kentik-plan
  KENTIK_REGION         US or EU (default: US)       --kentik-region
  KENTIK_SNMP_COMMUNITY SNMP community string        --snmp-community
  KENTIK_SNMP_CRED      SNMP credential name         --snmp-credential
  KENTIK_SAMPLE_RATE    Flow sample rate (default:1) --sample-rate

NMS agent detection:
  If a device carries a NetBox tag named 'kentik_primary_agent=<agentId>' it is flagged
  for Kentik NMS monitoring. The <agentId> portion is used as the NMS agent ID.
"""

import argparse
import json
import logging
import os
import sys
import time

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

NMS_AGENT_TAG = "kentik_primary_agent"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def get_config():
    parser = argparse.ArgumentParser(description="Sync NetBox to Kentik")
    parser.add_argument("--kentik-email", default=os.environ.get("KENTIK_EMAIL"))
    parser.add_argument("--kentik-token", default=os.environ.get("KENTIK_TOKEN"))
    parser.add_argument("--netbox-url", default=os.environ.get("NETBOX_URL"))
    parser.add_argument("--netbox-token", default=os.environ.get("NETBOX_TOKEN"))
    parser.add_argument("--kentik-plan", default=os.environ.get("KENTIK_PLAN_NAME"))
    parser.add_argument("--kentik-region", default=os.environ.get("KENTIK_REGION", "US"),
                        choices=["US", "EU"])
    parser.add_argument("--snmp-community", default=os.environ.get("KENTIK_SNMP_COMMUNITY", ""))
    parser.add_argument("--snmp-credential", default=os.environ.get("KENTIK_SNMP_CRED", "default"))
    parser.add_argument("--sample-rate", type=int,
                        default=int(os.environ.get("KENTIK_SAMPLE_RATE", "1")))
    cfg = parser.parse_args()

    missing = [name for name, attr in [
        ("KENTIK_EMAIL", "kentik_email"),
        ("KENTIK_TOKEN", "kentik_token"),
        ("NETBOX_URL", "netbox_url"),
        ("NETBOX_TOKEN", "netbox_token"),
        ("KENTIK_PLAN_NAME", "kentik_plan"),
    ] if not getattr(cfg, attr)]
    if missing:
        sys.exit(f"Missing required config: {', '.join(missing)}")

    return cfg


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def kentik_request(method, url, headers, payload=None, retries=0):
    """Issue a Kentik API request with rate-limit back-off and retry."""
    if retries >= 3:
        raise RuntimeError(f"HTTP {method} {url} failed after 3 retries")

    data = json.dumps(payload) if payload is not None else None
    response = requests.request(method, url, headers=headers, data=data, timeout=30)

    if response.status_code == 429:
        wait = int(response.headers.get("x-ratelimit-reset", 60))
        log.warning("Rate limited; sleeping %ds before retry", wait)
        time.sleep(wait)
        return kentik_request(method, url, headers, payload, retries + 1)

    if response.status_code == 404:
        return None

    if response.status_code not in (200, 201):
        raise RuntimeError(
            f"HTTP {method} {url} returned {response.status_code}: {response.text}"
        )

    remaining = response.headers.get("x-ratelimit-remaining")
    if remaining and int(remaining) < 10:
        time.sleep(10)

    return response


def netbox_get_all(url, headers):
    """Fetch every page from a NetBox paginated endpoint and return the full list."""
    results = []
    next_url = url
    while next_url:
        resp = requests.get(next_url, headers=headers, timeout=30, verify=False)
        if resp.status_code != 200:
            raise RuntimeError(
                f"NetBox GET {next_url} returned {resp.status_code}: {resp.text}"
            )
        body = resp.json()
        results.extend(body.get("results", []))
        next_url = body.get("next")
    return results


# ---------------------------------------------------------------------------
# Kentik API client
# ---------------------------------------------------------------------------

class KentikClient:
    def __init__(self, email, token, region="US"):
        if region == "EU":
            self._base = "https://grpc.api.kentik.eu"
            self._v5 = "https://api.kentik.eu/api/v5"
        else:
            self._base = "https://grpc.api.kentik.com"
            self._v5 = "https://api.kentik.com/api/v5"

        self._h = {
            "X-CH-Auth-Email": email,
            "X-CH-Auth-API-Token": token,
            "Content-Type": "application/json",
        }

    # ---- Sites ----

    def get_sites(self):
        """Return {title: id} for all Kentik sites."""
        resp = kentik_request("GET", f"{self._base}/site/v202211/sites", self._h)
        return {s["title"]: s["id"] for s in resp.json().get("sites", [])}

    def create_site(self, title, lat=0.0, lon=0.0):
        payload = {
            "site": {
                "title": title,
                "lat": lat or 0,
                "lon": lon or 0,
                "type": "SITE_TYPE_OTHER",
                "addressClassification": {
                    "infrastructureNetworks": [],
                    "userAccessNetworks": [],
                    "otherNetworks": [],
                },
            }
        }
        resp = kentik_request("POST", f"{self._base}/site/v202211/sites", self._h, payload)
        return resp.json()["site"]["id"]

    def ensure_site(self, title, lat=0.0, lon=0.0, site_cache=None):
        """Return the Kentik site ID, creating the site if it does not exist."""
        if site_cache is None:
            site_cache = {}
        if title not in site_cache:
            log.info("Creating missing site: %s", title)
            site_cache[title] = self.create_site(title, lat, lon)
        return site_cache[title]

    # ---- Labels ----

    def get_labels(self):
        """Return {name.lower(): id} for all Kentik labels."""
        resp = kentik_request("GET", f"{self._base}/label/v202210/labels", self._h)
        return {l["name"].lower(): l["id"] for l in resp.json().get("labels", [])}

    def create_label(self, name, color):
        payload = {"label": {"name": name, "color": color}}
        resp = kentik_request("POST", f"{self._base}/label/v202210/labels", self._h, payload)
        return resp.json()["label"]["id"]

    def ensure_label(self, name, color, label_cache):
        """Return the Kentik label ID, creating it if it does not exist."""
        key = name.lower()
        if key not in label_cache:
            log.info("Creating missing label: %s (%s)", name, color)
            try:
                label_cache[key] = self.create_label(name, color)
            except RuntimeError as exc:
                if "already exists" not in str(exc):
                    raise
                log.info("Label %s already exists, refreshing cache", name)
                label_cache.update(self.get_labels())
                if key not in label_cache:
                    raise RuntimeError(f"Label '{name}' exists in Kentik but was not returned by GET /labels") from exc
        return label_cache[key]

    # ---- Plans ----

    def get_plan_id(self, plan_name):
        resp = kentik_request("GET", f"{self._v5}/plans", self._h)
        for plan in resp.json().get("plans", []):
            if plan["name"] == plan_name:
                return plan["id"]
        raise RuntimeError(f"Kentik plan '{plan_name}' not found")

    # ---- Devices ----

    def check_device(self, device_name):
        """Return the Kentik device ID if it exists, else None."""
        resp = kentik_request("GET", f"{self._v5}/device/{device_name.lower()}", self._h)
        if resp is None:
            return None
        return resp.json()["device"]["id"]

    def create_device(self, device_obj):
        resp = kentik_request(
            "POST", f"{self._base}/device/v202504beta2/device", self._h,
            {"device": device_obj}
        )
        return resp.json()["device"]["id"]

    def update_device(self, device_id, device_obj):
        device_obj["id"] = device_id
        resp = kentik_request(
            "PUT", f"{self._base}/device/v202504beta2/device/{device_id}", self._h,
            {"device": device_obj}
        )
        return resp.json()["device"]["id"]

    def get_device_label_ids(self, device_id):
        resp = kentik_request(
            "GET", f"{self._base}/device/v202504beta2/device/{device_id}", self._h
        )
        return [lbl["id"] for lbl in resp.json()["device"].get("labels", [])]

    def set_device_labels(self, device_id, label_ids):
        payload = {
            "id": device_id,
            "labels": [{"id": int(lid)} for lid in label_ids],
        }
        kentik_request(
            "PUT", f"{self._base}/device/v202504beta2/device/{device_id}/labels",
            self._h, payload
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_cidr(ip_str):
    """'192.0.2.1/24' -> '192.0.2.1'."""
    return ip_str.split("/")[0] if ip_str and "/" in ip_str else ip_str


def nms_agent_tag(nb_device):
    """Return agent ID string if the device carries a kentik_primary_agent=<id> tag."""
    prefix = NMS_AGENT_TAG + "="
    tags = nb_device.get("tags", [])
    tag_names = [t.get("name", "") for t in tags]
    log.debug("Device %s tags: %s", nb_device.get("name"), tag_names)
    for name in tag_names:
        if name.startswith(prefix):
            return name.split("=", 1)[1]
    return None


# ---------------------------------------------------------------------------
# Phase 1 – Sites
# ---------------------------------------------------------------------------

def sync_sites(kentik, netbox_sites):
    """Ensure every NetBox site exists in Kentik. Returns {name: kentik_id}."""
    log.info("=== Phase 1: Syncing sites (%d NetBox sites) ===", len(netbox_sites))
    site_cache = kentik.get_sites()

    for nb_site in netbox_sites:
        name = nb_site["name"]
        if name in site_cache:
            log.info("Site already exists: %s", name)
            continue
        kentik.ensure_site(
            title=name,
            lat=nb_site.get("latitude") or 0.0,
            lon=nb_site.get("longitude") or 0.0,
            site_cache=site_cache,
        )

    log.info("Phase 1 complete. %d sites in Kentik.", len(site_cache))
    return site_cache


# ---------------------------------------------------------------------------
# Phase 2 – Devices
# ---------------------------------------------------------------------------

def sync_devices(kentik, netbox_devices, site_cache, plan_id, cfg):
    """Create or update every NetBox device in Kentik. Returns {name: kentik_device_id}."""
    log.info("=== Phase 2: Syncing devices (%d NetBox devices) ===", len(netbox_devices))
    device_ids = {}

    for nb in netbox_devices:
        name = nb["name"].lower()

        # Resolve site
        nb_site = nb.get("site") or {}
        site_name = nb_site.get("name")
        if not site_name or site_name not in site_cache:
            log.warning("Device %s: site '%s' not found in Kentik, skipping", name, site_name)
            continue
        site_id = site_cache[site_name]

        # Primary IP
        primary_ip4 = nb.get("primary_ip4")
        ip_address = strip_cidr(primary_ip4.get("address")) if primary_ip4 else None

        # NMS agent
        agent_id = nms_agent_tag(nb)

        device_obj = {
            "deviceName": name,
            "deviceDescription": nb.get("description") or "Synced from NetBox",
            "deviceSubtype": "router",
            "deviceSampleRate": cfg.sample_rate,
            "planId": int(plan_id),
            "siteId": int(site_id),
            "deviceBgpType": "none",
            "minimizeSnmp": False,
        }

        if ip_address:
            device_obj["sendingIps"] = [ip_address]
            device_obj["deviceSnmpIp"] = ip_address

        if cfg.snmp_community:
            device_obj["deviceSnmpCommunity"] = cfg.snmp_community

        if agent_id and ip_address:
            log.info("Device %s: configuring NMS with agent=%s ip=%s", name, agent_id, ip_address)
            device_obj["nms"] = {
                "agentId": agent_id,
                "ipAddress": ip_address,
                "snmp": {"credentialName": cfg.snmp_credential},
            }
        elif agent_id and not ip_address:
            log.warning("Device %s: NMS agent tag found (id=%s) but no primary IP — skipping NMS", name, agent_id)

        existing_id = kentik.check_device(name)
        if existing_id:
            log.info("Updating device: %s (id=%s)", name, existing_id)
            kentik.update_device(existing_id, device_obj)
            device_ids[name] = existing_id
        else:
            log.info("Creating device: %s", name)
            device_ids[name] = kentik.create_device(device_obj)

    log.info("Phase 2 complete. %d devices synced.", len(device_ids))
    return device_ids


# ---------------------------------------------------------------------------
# Phase 3 – Labels
# ---------------------------------------------------------------------------

def sync_labels(kentik, netbox_devices, netbox_roles, netbox_tenants, netbox_tags, device_ids):
    """Create labels from NetBox metadata and assign them to devices."""
    log.info("=== Phase 3: Syncing labels ===")
    label_cache = kentik.get_labels()

    # --- Create labels ---
    log.info("Ensuring role labels...")
    for role in netbox_roles:
        color = f"#{role.get('color', '808080')}"
        kentik.ensure_label(role["slug"], color, label_cache)

    log.info("Ensuring tenant labels...")
    for tenant in netbox_tenants:
        kentik.ensure_label(tenant["slug"], "#00ff00", label_cache)

    log.info("Ensuring tag labels...")
    for tag in netbox_tags:
        if tag.get("name", "").startswith(NMS_AGENT_TAG):
            continue  # internal control tag, not a metadata label
        color = f"#{tag.get('color', '808080')}"
        kentik.ensure_label(tag["slug"], color, label_cache)

    # --- Assign labels to devices ---
    log.info("Assigning labels to devices...")
    for nb in netbox_devices:
        name = nb["name"].lower()
        device_id = device_ids.get(name)
        if not device_id:
            continue

        desired = []

        if nb.get("role"):
            slug = nb["role"]["slug"]
            if slug in label_cache:
                desired.append(label_cache[slug])

        if nb.get("tenant"):
            slug = nb["tenant"]["slug"]
            if slug in label_cache:
                desired.append(label_cache[slug])

        for tag in nb.get("tags", []):
            if tag.get("name", "").startswith(NMS_AGENT_TAG):
                continue
            slug = tag.get("slug", "")
            if slug in label_cache:
                desired.append(label_cache[slug])

        if not desired:
            continue

        existing = kentik.get_device_label_ids(device_id)
        merged = list(set(existing + desired))
        if sorted(merged) != sorted(existing):
            log.info("Setting labels for %s: %s", name, merged)
            kentik.set_device_labels(device_id, merged)

    log.info("Phase 3 complete.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    cfg = get_config()

    nb_headers = {
        "Authorization": f"Token {cfg.netbox_token}",
        "Content-Type": "application/json",
    }
    nb_base = cfg.netbox_url.rstrip("/")

    log.info("Fetching data from NetBox at %s ...", nb_base)
    netbox_sites = netbox_get_all(f"{nb_base}/api/dcim/sites/?limit=0", nb_headers)
    netbox_devices = netbox_get_all(f"{nb_base}/api/dcim/devices/?limit=0", nb_headers)
    netbox_roles = netbox_get_all(f"{nb_base}/api/dcim/device-roles/?limit=0", nb_headers)
    netbox_tenants = netbox_get_all(f"{nb_base}/api/tenancy/tenants/?limit=0", nb_headers)
    netbox_tags = netbox_get_all(f"{nb_base}/api/extras/tags/?limit=0", nb_headers)
    log.info(
        "NetBox data: %d sites, %d devices, %d roles, %d tenants, %d tags",
        len(netbox_sites), len(netbox_devices), len(netbox_roles),
        len(netbox_tenants), len(netbox_tags),
    )

    kentik = KentikClient(cfg.kentik_email, cfg.kentik_token, cfg.kentik_region)
    plan_id = kentik.get_plan_id(cfg.kentik_plan)
    log.info("Kentik plan: '%s' (id=%s)", cfg.kentik_plan, plan_id)

    site_cache = sync_sites(kentik, netbox_sites)
    device_ids = sync_devices(kentik, netbox_devices, site_cache, plan_id, cfg)
    sync_labels(kentik, netbox_devices, netbox_roles, netbox_tenants, netbox_tags, device_ids)

    log.info("Sync complete.")


if __name__ == "__main__":
    main()
