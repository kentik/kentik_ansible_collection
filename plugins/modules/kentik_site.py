#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: kentik_site
short_description: This is a module that will perform idempotent operations on kentik site management.
version_added: "1.0.0"
description: The module will gather the current list of sites from Kentik and create the site if it is not in the list.
options:
    title:
        description: The site name to be displayed and referenced going forward.
        required: true
        type: str
    postalAddress:
        description: The physicall address of the site.
        type: dict
    type:
        description: The type of site this is, see choices for options.
        type: str
        default: SITE_TYPE_OTHER
        choices:
            - SITE_TYPE_DATA_CENTER
            - SITE_TYPE_CLOUD
            - SITE_TYPE_BRANCH
            - SITE_TYPE_CONNECTIVITY
            - SITE_TYPE_CUSTOMER
            - SITE_TYPE_OTHER
    lat:
        description: The latitude of the site.
        type: float
    lon:
        description: The longitude of the site.
        type: float
    siteMarket:
        description: Name of the Site Market this site belongs to.
        type: str
    region:
        description: The reqion that your Kentik portal is located in.
        type: str
        default: US
        choices:
            - US
            - EU
    state:
        description: States whether to delete or create.
        type: str
        default: present
        choices:
            - present
            - absent
    token:
        description: The Kentik API Token used to authenticate.
        type: str
        required: true
    email:
        description: The Kentik API Email used to authenticate.
        type: str
        required: true
author:
- Ethan Angele (@kentikethan)
"""

EXAMPLES = r"""
# Pass in a message
- name: Create a Site
  kentik_site:
    title: LA1
    postalAddress:
            address: 600 W 7th Street,
            city: Los Angeles,
            country: US
    type: SITE_TYPE_DATA_CENTER
- name: Create a Site in EU Cluster
  kentik_site:
    title: LA1
    postalAddress:
            address: 600 W 7th Street,
            city: Los Angeles,
            country: US
    type: SITE_TYPE_DATA_CENTER
    region: EU

# fail the module
- name: Test failure of the module
  create_kentik_site:
    title: fail me because site type not included
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

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
try:
    import requests
except ImportError:
    HAS_ANOTHER_LIBRARY = False
import json
import logging


def build_payload(module):
    """Build the payload"""
    payload = module.params
    del payload["email"]
    del payload["token"]
    del [payload["state"]]
    del [payload["region"]]
    return payload


def gather_sites(base_url, api_version, auth, module):
    """Gather a list of sites"""
    url = f"{base_url}{api_version}/sites"

    payload = {}
    headers = auth
    try:
        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=20
        )
        site_data = response.json()
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
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


def delete_site(base_url, api_version, auth, site_id, module):
    """Function to delete a site"""
    logging.info("Deleting Site...")
    url = f"{base_url}{api_version}/sites/{site_id}"
    payload = {}
    headers = auth
    try:
        response = requests.request(
            "DELETE", url, headers=headers, data=payload, timeout=20
        )
        if response.status_code == 200:
            function_return = "ok"
        else:
            module.fail_json(msg=response.text)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    return function_return


def create_site(base_url, api_version, auth, site_object, module):
    """Function for creating the site"""
    logging.info("Creating Site...")
    url = f"{base_url}{api_version}/sites"

    payload = json.dumps({"site": site_object})
    headers = auth
    try:
        response = requests.request(
            "POST", url, headers=headers, data=payload, timeout=20
        )
        if response.status_code == 200:
            site_data = response.json()
            function_return = site_data["site"]["id"]
        else:
            module.fail_json(msg=response.text)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    return function_return


def main():
    """Main function for the program"""
    argument_spec = dict(
        title=dict(type="str", required=True),
        postalAddress=dict(type="dict", required=False),
        type=dict(
            choices=[
                "SITE_TYPE_DATA_CENTER",
                "SITE_TYPE_CLOUD",
                "SITE_TYPE_BRANCH",
                "SITE_TYPE_CONNECTIVITY",
                "SITE_TYPE_CUSTOMER",
                "SITE_TYPE_OTHER",
            ],
            required=False,
            default="SITE_TYPE_OTHER",
        ),
        lat=dict(type="float", required=False),
        lon=dict(type="float", required=False),
        email=dict(type="str", required=True),
        token=dict(type="str", no_log=True, required=True),
        region=dict(type="str", required=False, default="US", choices=["US", "EU"]),
        state=dict(default="present", choices=["present", "absent"]),
        siteMarket=dict(type="str", required=False),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    result = {"changed": False}
    warnings = list()
    state = module.params["state"]
    auth = {
        "X-CH-Auth-Email": module.params["email"],
        "X-CH-Auth-API-Token": module.params["token"],
        "Content-Type": "application/json",
    }
    if module.params["region"] == "EU":
        base_url = "https://grpc.api.kentik.eu/site/"
    else:
        base_url = "https://grpc.api.kentik.com/site/"
    api_version = "v202211"
    site_object = build_payload(module)
    site_list = gather_sites(base_url, api_version, auth, module)
    site_exists = compare_site(site_list, module)

    if site_exists:
        if state == "present":
            result["changed"] = False
            result["site_id"] = site_exists
        elif state == "absent":
            delete_site(base_url, api_version, auth, site_exists, module)
            result["changed"] = True
    else:
        if state == "present":
            site_id = create_site(base_url, api_version, auth, site_object, module)
            result["changed"] = True
            result["site_id"] = site_id
        elif state == "absent":
            result["changed"] = False
    module.exit_json(**result)


if __name__ == "__main__":
    main()
