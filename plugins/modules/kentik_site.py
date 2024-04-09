#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: kentik_site

short_description: This is a module that will perform idempoent operations on kentik site management. 

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: The module will gather the current list of sites from Kentik and create the site if it is not in the list. 

options:
    title:
        description: The site name to be displayed and referenced going forward.
        required: true
        type: str
    postalAddress:
        description: The physicall address of the site. 
        required: false
        type: str
    type:
        description: The type of site this is, see choices for options. 
        required: true
        type: str
        default: SITE_TYPE_OTHER
        choices:
            - SITE_TYPE_DATA_CENTER
            - SITE_TYPE_CLOUD
            - SITE_TYPE_BRANCH
            - SITE_TYPE_CONNECTIVITY
            - SITE_TYPE_CUSTOMER
            - SITE_TYPE_OTHER
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Ethan Angele (@kentikethan)
'''

EXAMPLES = r'''
# Pass in a message
- name: Create a Site
  kentik_site:
    title: LA1
    postalAddress: 
            address: 600 W 7th Street,
            city: Los Angeles,
            country: US
    type: SITE_TYPE_DATA_CENTER

# fail the module
- name: Test failure of the module
  create_kentik_site:
    title: fail me because site type not included
'''

RETURN = r'''
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
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
import requests
import json
import os

def buildPayload(module):
    payload = module.params
    del payload['email']
    del payload['token']
    del[payload['state']]
    return payload

def gatherSites(base_url,api_version,auth,module):
    url = f"{base_url}{api_version}/sites"
    payload = {}
    headers = auth
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        site_data = response.json()
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    site_dict = {}
    for site in site_data['sites']:
        site_dict[site['title']] = site['id']
    return site_dict

def compareSite(site_list, module):
    site=module.params["title"]
    if site in site_list:
        print("Site exists")
        return site_list[site]
    else:
        print("Site does not exists")
        return False

def deleteSite(base_url,api_version,auth,site_id,module):
    print("Deleting Site...")
    url = f"{base_url}{api_version}/sites/{site_id}"
    payload = {}
    headers = auth
    try:
        response = requests.request("DELETE", url, headers=headers, data=payload)
        if response.status_code == 200:
            return
        else:
            module.fail_json(msg=response.text)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))

def createSite(base_url,api_version,auth,site_object,module):
    print("Creating Site...")
    url = f"{base_url}{api_version}/sites"

    payload = json.dumps({
        "site": site_object
        })
    headers = auth
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            site_data = response.json()
            return site_data['site']['id']
        else:
            module.fail_json(msg=response.text)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))

def main():
    base_url = "https://grpc.api.kentik.com/site/"
    api_version = "v202211"
    argument_spec = dict(
        title=dict(type='str', required=True),
        postalAddress=dict(type='dict', required=False),
        type=dict(choices=["SITE_TYPE_DATA_CENTER","SITE_TYPE_CLOUD","SITE_TYPE_BRANCH","SITE_TYPE_CONNECTIVITY","SITE_TYPE_CUSTOMER","SITE_TYPE_OTHER"], required=False, default="SITE_TYPE_OTHER"),
        lat=dict(type="int", required=False),
        lon=dict(type="int", required=False),
        email=dict(type='str', required=False, default=os.environ['KENTIK_EMAIL']),
        token=dict(type='str', no_log=True, required=False, default=os.environ['KENTIK_TOKEN']),
        state=dict(default="present", choices=["present", "absent"])
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    result = {"changed": False}
    warnings = list()
    state = module.params['state']
    auth = {
        'X-CH-Auth-Email': module.params['email'], 
        'X-CH-Auth-API-Token': module.params['token'], 
        'Content-Type': 'application/json'
        }
    site_object = buildPayload(module)
    site_list = gatherSites(base_url,api_version,auth,module)
    site_exists = compareSite(site_list, module)

    if site_exists:
        if state == "present":
            result["changed"] = False
            result["site_id"] = site_exists
        elif state == "absent":
            deleteSite(base_url,api_version,auth,site_exists,module)
            result["changed"] = True
    else:
        if state == "present":
            site_id = createSite(base_url,api_version,auth,site_object,module)
            result["changed"] = True
            result["site_id"] = site_id
        elif state == "absent":
            result["changed"] = False
    module.exit_json(**result)

if __name__ == '__main__':
    main()