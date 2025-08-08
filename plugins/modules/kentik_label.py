#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: kentik_label
short_description: This is a module that will perform idempotent operations on kentik label management.
version_added: "1.0.0"
description: The module will gather the current list of sites from Kentik and create the site if it is not in the list.
options:
    name:
        description: The name or title of the label.
        required: true
        type: str
    color:
        description: The hexidecimal color code to be applied to the label. Default is a gray color.
        type: str
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
- name: Create a Label
  kentik_label:
    name: ACCESS_SWITCH
    color: #007090
    state: present
# Delete a label
- name: Delete a Label
  kentik_label:
    name: ACCESS_SWITCH
    state: absent
    region: EU
# Fail the module
- name: Test failure of the module
  kentik_label:
    name: fail me because wrong state
    state: create
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
import os


def build_payload(module):
    """Build the request payload"""
    payload = module.params
    del payload["email"]
    del payload["token"]
    del [payload["state"]]
    del [payload["region"]]
    return payload


def gather_labels(base_url, api_version, auth, module):
    """Gather the current list of labels"""
    url = f"{base_url}/label/{api_version}/labels"
    payload = {}
    headers = auth
    label_data = {}
    try:
        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=30
        )
        if response.status_code == 200:
            label_data = response.json()
        else:
            module.fail_json(msg=f"gatherLabels: {response.text}")
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    label_dict = {}
    for label in label_data["labels"]:
        label_dict[label["name"]] = label["id"]
    return label_dict


def compare_label(label_list, module):
    """Check to see if the label already exists"""
    label = module.params["name"]
    if label in label_list:
        logging.info("Label %s exists", label)
        function_return = label_list[label]
    else:
        logging.info("Label does not exists...")
        function_return = False
    return function_return


def delete_label(base_url, api_version, auth, module, label_id):
    """Deletes the site"""
    logging.info("Deleting Label...")
    url = f"{base_url}/label/{api_version}/labels/{label_id}"
    payload = {}
    headers = auth
    function_return = ""
    try:
        response = requests.request(
            "DELETE", url, headers=headers, data=payload, timeout=30
        )
        if response.status_code == 200:
            function_return = "OK"
        else:
            module.fail_json(msg=response.text)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    return function_return


def create_label(base_url, api_version, auth, module, site_object):
    """Creates a site"""
    logging.info("Creating Label...")
    url = f"{base_url}/label/{api_version}/labels"

    payload = json.dumps({"label": site_object})
    headers = auth
    function_return = ''
    try:
        response = requests.request(
            "POST", url, headers=headers, data=payload, timeout=30
        )
        label_data = response.json()
        if response.status_code == 200:
            function_return = label_data["label"]["id"]
        else:
            module.fail_json(msg=response.text)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    return function_return


def main():
    """Main function for the program starts here"""
    argument_spec = dict(
        name=dict(type="str", required=True),
        color=dict(type="str", required=True),
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
    api_version = "v202210"
    site_object = build_payload(module)
    result = {"changed": False}
    warnings = list()
    label_list = gather_labels(base_url, api_version, auth, module)
    label_exists = compare_label(label_list, module)

    if label_exists:
        if state == "present":
            result["changed"] = False
            result["label_id"] = label_exists
        elif state == "absent":
            label_id = delete_label(base_url, api_version, auth, module, label_exists)
            result["changed"] = True
    else:
        if state == "present":
            label_id = create_label(base_url, api_version, auth, module, site_object)
            result["changed"] = True
            result["label_id"] = label_id
        elif state == "absent":
            result["changed"] = False
    module.exit_json(**result)


if __name__ == "__main__":
    main()
