#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {"metadata_version": "1.0", "status": ["preview"], "supported_by": "certified"}

DOCUMENTATION = r"""
---
module: kentik_device
short_description: This is a module that will perform idempotent operations on kentik device management
version_added: "1.0.0"
description: The module will gather the current list of devices from Kentik and create or update the device if it is not in the list.
options:
    deviceName:
        description: The name of the device.
        required: true
        type: str
    deviceDescription:
        description: The device description.
        type: str
        default: Added by Ansible
    deviceSubtype:
        description: The device subtype.
        choices: [ router, host-nprobe-dns-www, aws-subnet, azure_subnet, cisco_asa, gcp-subnet, istio_beta, open_nms, paloalto, silverpeak ]
        type: str
        default: "router"
    cdnAttr:
        description: If this is a DNS server, you can contribute its queries to Kentik's CDN attribution database.
        choices: [ none, y, n ]
        type: str
    deviceSampleRate:
        description: The rate at which the device is sampling flows.
        type: int
        default: 1
    planName:
        description: The ID of the plan to which this device is assigned.
        required: true
        type: str
    siteName:
        description: The name of the site (if any) to which this device is assigned.
        type: str
    sendingIps:
        description: IP addresses from which the device is sending flow.
        required: false
        type: list
        elements: str
    minimizeSnmp:
        description: IP addresses from which the device is sending flow.
        type: bool
    deviceSnmpIp:
        description: IP address from which the device is listening on snmp.
        type: str
    deviceSnmpCommunity:
        description: The SNMP community to use when polling the device.
        type: str
    updateSnmpAuth:
        description: Update the SNMP Authentication.
        type: bool
        default: false
    deviceSnmpV3Conf:
        description:
        - A dictionary with all snmpv3 attributes.
        - Reference Kentik API Documentation for exact dictionary format.
        type: dict
    deviceBgpType:
        description: BGP (device_bgp_type) - Device bgp type.
        choices: [ none, device, other_device ]
        type: str
        default: none
    deviceBgpNeighborIp:
        description: Your IPv4 peering address.
        type: str
    deviceBgpNeighborIp6:
        description: Your IPv6 peering address.
        type: str
    deviceBgpNeighborAsn:
        description: The valid AS number (ASN) of the autonomous system that this device belongs to.
        type: str
    deviceBgpPassword:
        description: Optional BGP MD5 password.
        type: str
    useBgpDeviceId:
        description: The ID of the device whose BGP table should be shared with this device.
        type: int
    deviceBgpFlowspec:
        description: Toggle BGP Flowspec Compatibility for device.
        type: bool
    region:
        description: The reqion that your Kentik portal is located in.
        type: str
        default: US
        choices: [ US, EU ]
    nms:
        description:
        - A dictionary for adding NMS SNMP or streaming telemetry to a device.
        - Reference Kentik API Documentation for exact dictionary format.
        type: dict
    state:
        description: Whether to ensure the device should be present or if it should be removed. Run twice on absent to delete.
        type: str
        choices: [present, absent]
        default: present
    token:
        description: The Kentik API Token used to authenticate.
        type: str
        required: true
    email:
        description: The Kentik API Email used to authenticate.
        type: str
        required: true
    labels:
        description: Labels that get assigned to the device.
        type: list
        elements: str
author:
- Ethan Angele (@kentikethan)
"""

EXAMPLES = r"""
# Pass in a message
- name: Create a device
  kentik_device:
    name: edge_la1_001
    description: Edge router 1 in la data center
    sampleRate: 10
    type: router
    planId: 12345
    siteId: 12345
    flowSendingIp: 192.168.0.1
    snmpVersion: v2c
    snmpIp: 192.168.0.1
    snmpCommunity: myPreciousCommunity
    bgpType: device
    bgpNeighborIp: 192.168.0.1
    bgpNeighborAsn: 65001
    deviceBgpPassword: myPreciousPassword
    deviceBgpFlowspec: True
    region: EU
# fail the module
- name: Test failure of the module
  kentik_device:
    name: just_the_name_nothing_else_fail
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
"""

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
try:
    import requests
except ImportError:
    HAS_ANOTHER_LIBRARY = False
import logging
import time


def gather_labels(base_url, api_version, auth, module):
    """Gather the current list of labels"""
    url = f"{base_url}/label/{api_version}/labels"
    payload = {}
    headers = auth
    response = http_request_func("GET", url, headers, payload, module)
    label_data = response.json()
    label_dict = {}
    for label in label_data["labels"]:
        label_dict[label["name"]] = label["id"]
    return label_dict


def build_labels(base_url, api_version, auth, module):
    """Function to build the list of labels to be added to a device"""
    api_version = "v202210"
    current_labels = gather_labels(base_url, api_version, auth, module)
    label_ids = []
    for label in module.params["labels"]:
        if label in current_labels:
            label_ids.append(current_labels[label])
        elif label == "":
            continue
        else:
            module.fail_json(msg=f"Label {label} does not exist.")
    return label_ids


def gather_sites(base_url, api_version, auth, module):
    """Gather a list of sites"""
    url = f"{base_url}{api_version}/sites"
    payload = {}
    headers = auth
    response = http_request_func("GET", url, headers, payload, module)
    site_data = response.json()
    site_dict = {}
    for site in site_data["sites"]:
        site_dict[site["title"]] = site["id"]
    return site_dict


def compare_site(site_list, module):
    """Check to see if the site exists"""
    site = module.params["title"]
    if site in site_list:
        logging.info("Site Exists")
        function_return = site_list[site]
    else:
        logging.info("Site does not exists")
        function_return = False
    return function_return


def build_payload(base_url, auth, module):
    """Function to build the device object payload by removing unnecessary items."""
    payload = module.params
    del payload["email"]
    del payload["token"]
    del [payload["state"]]
    payload["title"] = module.params["siteName"]
    del [payload["siteName"]]
    # REMEMBER TO PASS THE CORRECT API VERSION FOR SITES HERE
    site_list = gather_sites(base_url, "/site/v202211", auth, module)
    site_id = compare_site(site_list, module)
    if site_id is False:
        module.fail_json(msg=f"Site {payload['title']} does not exist.")
    payload["siteId"] = int(site_id)
    plan_dict = gather_plans(auth, module)
    plan_id = compare_plan(plan_dict, module)
    payload["planId"] = int(plan_id)
    del [payload["planName"]]
    del [payload["labels"]]
    del [payload["title"]]
    del [payload["region"]]
    del [payload["updateSnmpAuth"]]
    none_keys = []
    for key in payload:
        if payload[key] is None:
            none_keys.append(key)
    for key in none_keys:
        del [payload[key]]
    if "nms" in payload:
        if "port" in payload["nms"]["snmp"]:
            payload["nms"]["snmp"]["port"] = int(payload["nms"]["snmp"]["port"])
    return payload


def http_request_func(method, url, headers, payload, module, retries=0):
    """Function for hanlding HTTP Requests"""
    if retries < 3:
        try:
            response = requests.request(
                method, url, headers=headers, data=payload, timeout=30
            )
            if response.status_code == 200:
                logging.info("%s HTTP Request Successfull for url: %s", method, url)
            elif response.status_code == 429:
                if 'x-ratelimit-reset' in response.headers:
                    time.sleep(int(response.headers['x-ratelimit-reset']))
                else:
                    time.sleep(60)
                retries += 1
                http_request_func(method, url, headers, payload, module, retries)
            elif response.status_code == 404:
                return False
            else:
                module.fail_json(msg=response.text)
            if 'x-ratelimit-remaining' in response.headers:
                if int(response.headers['x-ratelimit-remaining']) < 10:
                    time.sleep(10)  # Helps to slow down the rate of execution for throttling.
        except ConnectionError as exc:
            module.fail_json(msg=to_text(exc))
    else:
        module.fail_json(msg="ERROR - RETRIED 3 TIMES")
    return response


def gather_plans(auth, module):
    """Function to gather a list of existing plans"""
    if module.params["region"] == "EU":
        url = "https://api.kentik.eu/api/v5/plans"
    else:
        url = "https://api.kentik.com/api/v5/plans"
    payload = {}
    headers = auth
    plan_data = ''
    response = http_request_func("GET", url, headers, payload, module)
    plan_data = response.json()
    plan_dict = {}
    for plan in plan_data["plans"]:
        plan_dict[plan["name"]] = plan["id"]
    return plan_dict


def compare_plan(plan_dict, module):
    """Function to determine whether the plan exists"""
    plan = module.params["planName"]
    if plan in plan_dict:
        logging.info("Plan exists")
    else:
        logging.info("Plan does not exists")
        module.fail_json(msg=f"Plan {plan} does not exist.")
    return plan_dict[plan]


def gather_devices(base_url, api_version, auth, module):
    """Function to gather a list of devices for comparison"""
    url = f"{base_url}/device/{api_version}/device"
    payload = {}
    headers = auth
    response = http_request_func("GET", url, headers, payload, module)
    device_data = response.json()
    device_dict = {}
    for device in device_data["devices"]:
        device_dict[device["deviceName"]] = device["id"]
    return device_dict


def compare_device(device_list, module):
    """Function to determine whether a device already exists"""
    device = module.params["deviceName"]
    if device in device_list:
        logging.info("Device exists")
        function_return = device_list[device]
    else:
        logging.info("Device, %s does not exists", device)
        function_return = False
    return function_return


def compare_labels(base_url, api_version, auth, module, device_id, labels):
    """Function to compare labels on a device to determine if it needs updated."""
    url = f"{base_url}/device/{api_version}/device/{device_id}"
    payload = {}
    headers = auth
    function_return = ''
    response = http_request_func("GET", url, headers, payload, module)
    device_data = response.json()
    device_labels = []
    for device_label in device_data["device"]["labels"]:
        device_labels.append(device_label["id"])
    device_labels.sort()
    if labels:
        labels.sort()
    if labels == device_labels:
        function_return = False
    else:
        function_return = labels
    return function_return


def delete_device(base_url, api_version, auth, device_id, module):
    """Function to delete a device from Kentik"""
    logging.info("Archiving Device...")
    url = f"{base_url}/device/{api_version}/device/{device_id}"
    payload = {}
    headers = auth
    http_request_func("DELETE", url, headers, payload, module)
    logging.info("Device deleted successfully")


def check_device(auth, module, region):
    """Function to check if the device exists in kentik"""
    logging.info("Checking if the device needs updated...")
    device_name = module.params["deviceName"]
    if region == "EU":
        url = f"https://api.kentik.eu/api/v5/device/{device_name}"
    else:
        url = f"https://api.kentik.com/api/v5/device/{device_name}"
    headers = auth
    device_data = {}
    payload = {}
    response = http_request_func("GET", url, headers, payload, module)
    if response:
        device_data['exists'] = True
        device_info = response.json()
        device_data['id'] = device_info['device']['id']
    else:
        device_data['exists'] = False
    return device_data


def create_device(base_url, api_version, auth, module, device_object):
    """Function to add a device to kentik"""
    logging.info("Creating Device...")
    url = f"{base_url}/device/{api_version}/device"
    payload = json.dumps({"device": device_object})
    headers = auth
    device_data = ''
    response = http_request_func("POST", url, headers, payload, module)
    device_data = response.json()
    return device_data["device"]["id"]


def update_device_labels(base_url, api_version, auth, module, device_id, labels):
    """Function to add or update device labels"""
    logging.info("Updating Device Labels...")
    url = f"{base_url}/device/{api_version}/device/{device_id}/labels"
    headers = auth
    labels_list = []
    device_data = ''
    for label in labels:
        label_dict = {"id": int(label)}
        labels_list.append(label_dict)
    payload = json.dumps({"id": device_id, "labels": labels_list})
    response = http_request_func("PUT", url, headers, payload, module)
    device_data = response.json()
    return device_data["device"]["id"]


def update_check(base_url, api_version, auth, module, device_id, device_object, update_bool):
    """Function to check whether a device needs to be updated"""
    logging.info("Checking device update...")
    url = f"{base_url}/device/{api_version}/device/{device_id}"
    headers = auth
    device_data = {}
    payload = {}
    response = http_request_func("GET", url, headers, payload, module)
    device_data = response.json()
    if "nms" in device_object:
        logging.info("NMS will be configured...")
        if "port" in device_object["nms"]["snmp"]:
            logging.info("Port is configured in nms settings...")
            device_object["nms"]["snmp"]["port"] = int(device_object["nms"]["snmp"]["port"])
        elif "nms" in device_data["device"]:
            del [device_data["device"]["nms"]["snmp"]["port"]]
    return_bool = False
    if int(device_data["device"]["site"]["id"]) != int(device_object["siteId"]):
        logging.info("Site does not match...updating...")
        return_bool = True
    elif int(device_data["device"]["plan"]["id"]) != int(device_object["planId"]):
        logging.info("Plan IDs don't match...updating")
        return_bool = True
    elif update_bool:
        return_bool = True
    else:
        del [device_object["siteId"]]
        del [device_object["planId"]]
        del [device_object["deviceSnmpCommunity"]]
        for key in device_object:
            if key not in device_data["device"]:
                logging.info("Configured %s: %s is not yet configured.", key, device_object[key])
                return_bool = True
            else:
                if str(device_data["device"][key]) != str(device_object[key]):
                    logging.info("Configured %s: %s does not match returned %s: %s",
                                 key,
                                 device_object[key],
                                 key,
                                 device_data["device"][key])
                    return_bool = True
    if return_bool is False:
        logging.info("Device is up to date...")
    return return_bool


def update_device(base_url, api_version, auth, module, device_id, device_object):
    """Function to update a device to kentik"""
    logging.info("Updating Device...")
    url = f"{base_url}/device/{api_version}/device/{device_id}"
    device_object['id'] = device_id
    payload = json.dumps({"device": device_object})
    headers = auth
    device_data = ''
    response = http_request_func("PUT", url, headers, payload, module)
    device_data = response.json()
    return device_data["device"]["id"]


def main():
    """The main function of the program"""
    base_url = "https://grpc.api.kentik.com"
    argument_spec = dict(
        deviceName=dict(type="str", required=True),
        deviceDescription=dict(type="str", required=False, default="Added by Ansible"),
        deviceSubtype=dict(
            type="str",
            required=False,
            default="router",
            choices=[
                "router",
                "host-nprobe-dns-www",
                "aws-subnet",
                "azure_subnet",
                "cisco_asa",
                "gcp-subnet",
                "istio_beta",
                "open_nms",
                "paloalto",
                "silverpeak",
            ],
        ),
        cdnAttr=dict(type="str", required=False, choices=["none", "y", "n"]),
        deviceSampleRate=dict(type="int", required=False, default=1),
        planName=dict(type="str", required=True),
        siteName=dict(type="str", required=False),
        sendingIps=dict(type="list", required=False, elements="str"),
        minimizeSnmp=dict(type="bool", required=False),
        deviceSnmpIp=dict(type="str", required=False),
        deviceSnmpCommunity=dict(type="str", required=False),
        updateSnmpAuth=dict(type="bool", required=False, default=False),
        deviceSnmpV3Conf=dict(type="dict", required=False),
        deviceBgpType=dict(
            type="str",
            required=False,
            choices=["none", "device", "other_device"],
            default="none",
        ),
        deviceBgpNeighborIp=dict(type="str", required=False),
        deviceBgpNeighborIp6=dict(type="str", required=False),
        deviceBgpNeighborAsn=dict(type="str", required=False),
        deviceBgpPassword=dict(type="str", required=False, no_log=True),
        useBgpDeviceId=dict(type="int", required=False),
        deviceBgpFlowspec=dict(type="bool", required=False),
        nms=dict(type="dict", required=False),
        labels=dict(type="list", required=False, elements="str"),
        email=dict(type="str", required=True),
        token=dict(type="str", no_log=True, required=True),
        region=dict(type="str", required=False, default="US", choices=["US", "EU"]),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    result = {"changed": False}
    state = module.params["state"]
    auth = {
        "X-CH-Auth-Email": module.params["email"],
        "X-CH-Auth-API-Token": module.params["token"],
        "Content-Type": "application/json",
    }
    if module.params["region"] == "EU":
        base_url = "https://grpc.api.kentik.eu"
        region = "EU"
    else:
        base_url = "https://grpc.api.kentik.com"
        region = "US"
    api_version = "v202308beta1"
    if module.params["labels"]:
        logging.info("Labels found")
        labels = build_labels(base_url, api_version, auth, module)
    else:
        logging.info("No Labels found")
        labels = False
    update_snmp_auth_bool = module.params["updateSnmpAuth"]
    result = {"changed": False}
    # device_list = gather_devices(base_url, api_version, auth, module)
    # device_id = compare_device(device_list, module)
    device_exists = check_device(auth, module, region)
    if state == "absent" and device_exists['exists']:
        delete_device(base_url, api_version, auth, device_exists['id'], module)
        result["changed"] = True
    elif device_exists['exists'] and state == "present":
        labels = compare_labels(base_url, api_version, auth, module, device_exists['id'], labels)
        device_object = build_payload(base_url, auth, module)
        needs_updated = update_check(base_url,
                                     api_version,
                                     auth, module,
                                     device_exists['id'],
                                     device_object,
                                     update_snmp_auth_bool)
        if needs_updated:
            update_device(base_url, api_version, auth, module, device_exists['id'], device_object)
            result["changed"] = True
        else:
            result["changed"] = False
    elif not device_exists['exists'] and state == "present":
        device_object = build_payload(base_url, auth, module)
        device_id = create_device(base_url,
                                  api_version,
                                  auth,
                                  module,
                                  device_object)
        result["changed"] = True
        result["device_id"] = device_id
    elif state == "absent" and not device_exists['exists']:
        result["changed"] = False
    if labels and len(labels) > 0 and state == "present":
        update_device_labels(base_url, api_version, auth, module, device_id, labels)
        result["changed"] = True
    module.exit_json(**result)


if __name__ == "__main__":
    main()
