#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {"metadata_version": "1.0", "status": ["preview"], "supported_by": "certified"}

DOCUMENTATION = r"""
---
module: kentik_as_groups
short_description: This is a module that will add as groups to kentik.
version_added: "1.2.3"
description: The module will perform standard CRUD operations against the Kentik AS group API.
options:
    name:
        description: The name of the group.
        required: true
        type: str
    asn:
        description: List of ASNs.
        type: list
        elements: str
        required: true
    region:
        description: The reqion that your Kentik portal is located in.
        type: str
        default: US
        choices:
        - US
        - EU
        - ENV
    state:
        description: Whether to ensure the device should be present or if it should be removed.
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
author:
- Ethan Angele (@kentikethan)
"""

EXAMPLES = r"""
# Pass in a message
- name: Create an AS Group
  kentik_as_group:
    name: my_special_group
    asns: 65535
# fail the module
- name: Test failure of the module
  kentik_as_group:
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
import os
try:
    import requests
except ImportError:
    HAS_ANOTHER_LIBRARY = False
import logging
import time

def build_payload(module):
    """Build the request payload"""
    payload = module.params
    del payload["email"]
    del payload["token"]
    del [payload["state"]]
    del [payload["region"]]
    return payload


def gather_groups(url, auth, module):
    """Gather the current list of groups"""
    payload = {}
    headers = auth
    group_data = {}
    
    try:
        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=30
        )
        if response.status_code == 200:
            group_data = response.json()
        else:
            module.fail_json(msg=f"gathergroups: {response.text}")
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    group_dict = {}
    for group in group_data["asGroups"]:
        group_dict[group["name"]] = group["id"]
    return group_dict


def compare_group(group_list, module):
    """Check to see if the group already exists"""
    group = module.params["name"]
    if group in group_list:
        logging.info("group %s exists", group)
        function_return = group_list[group]
    else:
        logging.info("group does not exists...")
        function_return = False
    return function_return


def delete_group(url, auth, module, group_id):
    """Deletes the site"""
    logging.info("Deleting group...")
    payload = {}
    headers = auth
    function_return = ""
    try:
        response = requests.request(
            "DELETE", f"{url}/{group_id}", headers=headers, data=payload, timeout=30
        )
        if response.status_code == 200:
            function_return = "OK"
        else:
            module.fail_json(msg=response.text)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    return function_return


def create_group(url, auth, module, group_object):
    """Creates a site"""
    logging.info("Creating group...")

    payload = json.dumps({"asGroup": group_object})
    headers = auth
    function_return = ''
    try:
        response = requests.request(
            "POST", url, headers=headers, data=payload, timeout=30
        )
        group_data = response.json()
        if response.status_code == 200:
            function_return = group_data["asGroup"]["id"]
        else:
            module.fail_json(msg=response.text)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    return function_return


def main():
    """Main function for the program starts here"""
    argument_spec = dict(
        name=dict(type="str", required=True),
        asn=dict(type="list", required=True),
        email=dict(type="str", required=True),
        token=dict(type="str", no_log=True, required=True),
        region=dict(type="str", default="US", choices=["US", "EU", "ENV"]),
        state=dict(default="present", choices=["present", "absent"]),
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
        base_url = "https://grpc.api.kentik.eu"
    elif module.params["region"] == "ENV":
        base_url = os.environ("KENTIK_URL")
        region = "ENV"
    else:
        base_url = "https://grpc.api.kentik.com"
    api_url = f"{base_url}/as_group/v202212/as_group"
    result = {"changed": False}
    warnings = list()
    group_object = build_payload(module)
    group_list = gather_groups(api_url, auth, module)
    group_exists = compare_group(group_list, module)
    if group_exists:
        if state == "present":
            result["changed"] = False
            result["group_id"] = group_exists
        elif state == "absent":
            group_id = delete_group(api_url, auth, module, group_exists)
            result["changed"] = True
    else:
        if state == "present":
            group_id = create_group(api_url, auth, module, group_object)
            result["changed"] = True
            result["group_id"] = group_id
        elif state == "absent":
            result["changed"] = False
    module.exit_json(**result)


if __name__ == "__main__":
    main()