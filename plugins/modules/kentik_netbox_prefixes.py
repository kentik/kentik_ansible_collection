#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: kentik_netbox_prefixes
short_description: This is a module that will perform idempotent operations to synchronize netbox prefixes.
version_added: "1.2.0"
description: The module will gather the list of prefixes from netbox and then proceed to create kentik elements with them depending on the users selection.
options:
    netboxUrl:
        description: The Netbox Url to collect the prefixes from.
        required: true
        type: str
    netboxToken:
        description: The Netbox Token to use for authentication.
        required: true
        type: str
    enableSitebyIP:
        description: Add the IP addresses to the Site.
        type: bool
        default: false
    enableTenant:
        description: Create custom dimensions based on the prefix Tenant.
        type: bool
        default: false
    tenantName:
        description: The custom dimension name to be used for tenants.
        type: str
        default: tenant
    enableVlan:
        description: Create custom dimensions based on the prefix Vlan.
        type: bool
        default: false
    vlanName:
        description: The custom dimension name to be used for vlans.
        type: str
        default: vlans
    enableRoles:
        description: Create custom dimensions based on the prefix Role.
        type: bool
        default: false
    roleName:
        description: The custom dimension name to be used for roles.
        type: str
        default: role
    enableDescriptions:
        description: Create custom dimensions based on the prefix Descriptions.
        type: bool
        default: false
    descriptionName:
        description: The custom dimension name to be used for description.
        type: str
        default: description
    enableCustomFields:
        description: Creat custom dimensions based on the prefix Custom Fields.
        type: bool
        default: false
    customFieldName:
        description: Custom Field to add as a custom dimension.
        type: str
    activeOnly:
        description: Only add prefixes that are active in Netbox.
        type: bool
        default: true
    region:
        description: The reqion that your Kentik portal is located in.
        type: str
        default: US
        choices:
            - US
            - EU
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
- name: Synchronize all Netbox Prefixes and Components
  kentik_netbox_prefixes:
    netboxUrl: https://www.netboxlabs.com
    netboxToken: kfjdkfdihfq093ru3029ur3qef
    enableTenant: True
    enableSitebyIP: True
    enableRoles: True
    enableDescriptions: True
    enableVlan: True
    enableCustomFields: True
    customFieldName: POD
    activeOnly: True
    email: someoneawesome@kentik.com
    token: ewjhrtefngkrbgfsdgfh4o43r523
    region: US

# fail the module
- name: Test failure of the module. Fails because custom field name was not included.
  kentik_netbox_prefixes:
    netboxUrl: https://www.netboxlabs.com
    netboxToken: kfjdkfdihfq093ru3029ur3qef
    enableTenant: True
    enableSitebyIP: True
    enableRoles: True
    enableDescriptions: True
    enableVlan: True
    enableCustomFields: True
    activeOnly: True
    email: someoneawesome@kentik.com
    token: ewjhrtefngkrbgfsdgfh4o43r523
    region: US
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
import time
try:
    import requests
except ImportError:
    HAS_ANOTHER_LIBRARY = False
import json
import logging
logging.basicConfig(level=logging.INFO)


def build_kentik_auth(module):
    '''Build the kentik auth dictionary for headers'''
    kentik_auth = {
        "X-CH-Auth-Email": module.params["email"],
        "X-CH-Auth-API-Token": module.params["token"],
        "Content-Type": "application/json",
    }
    return kentik_auth


def build_netbox_auth(module):
    '''Build the netbox auth dictionary'''
    netbox_auth = {
        "Authorization": "Token " + module.params["netboxToken"],
        "Content-Type": "application/json",
    }
    return netbox_auth


def collect_prefixes(module, headers):
    """ Collect the prefixes from Netbox """
    # Could add streaming support potentially?
    prefixes = []
    try:
        response = requests.get(f"{module.params["netboxUrl"]}/api/ipam/prefixes",
                                headers=headers,
                                timeout=30,
                                stream=True)
        for raw_data in response.iter_lines():
            if raw_data:
                data = json.loads(raw_data)
                for item in data["results"]:
                    prefix = {"prefix": item["prefix"],
                              **({"site": item["site"]["name"]}
                              if item["site"] is not None else {}),
                              **({"tenant": item["tenant"]["name"]}
                              if item["tenant"] is not None else {}),
                              **({"vlan": item["vlan"]["name"]}
                              if item["vlan"] is not None else {}),
                              **({"role": item["role"]["name"]}
                              if item["role"] is not None else {}),
                              **({f"{module.params["customFieldName"]}":
                                 item["custom_fields"][f"{module.params["customFieldName"]}"]}
                              if f"{module.params["customFieldName"]}" in item["custom_fields"]
                              else {}),
                              **({"description": item["description"]}
                              if item["description"] is not None else {})
                              }
                    prefixes.append(prefix)
        return prefixes
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
        return None


def gather_choices(module):
    '''
    This function will evaluate what the customer has set to true
    in the ansible options and execute accordingly.
    '''
    logging.info("Checking what needs to be created based off of enable statements...")
    # build_choices = [decisions.update({name: value})  if "enable" in
    # name else logging.info("Skipping...")
    # for name, value in module.params.items()]
    # List of functions to true or false decsions.
    # The dictionary keys are actually the function to execute as well.
    decisions = {
        add_to_sites: module.params["enableSitebyIP"],
        add_with_vlans: module.params["enableVlan"],
        add_with_tenants: module.params["enableTenant"],
        add_with_roles: module.params["enableRoles"],
        add_with_descriptions: module.params["enableDescriptions"],
        add_with_custom_fields: module.params["enableCustomFields"]
    }
    return decisions


def add_to_sites(module, kentik_auth, warnings, prefixes):
    '''Function to update site by ip classication'''

    # Step one is to build the paylooad based on the current option selected.
    #   - Allow customizations of the custom dimension name?
    #   - Use jinja2 templates to create a bulk upload?
    #   - How do we scale to support millions of prefixes all assigned an attribute?
    #       - We could use ijson to stream the prefixes into a local cacched database using sqlite.
    #       - Then we could read the prefixes from the database locally and stream to kentik?
    #       - Can the kentik api support streaming uploads or uploads spaced out over time?
    # Step two is to allow the
    # Gather a list of sites
    if module.params["region"] == "EU":
        url = "https://grpc.api.kentik.eu"
    else:
        url = "https://grpc.api.kentik.com"
    try:
        response = requests.request(
            "GET", f"{url}/site/v202211/sites", headers=kentik_auth, timeout=30
        )
        response.raise_for_status()
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    sites = response.json()
    site_dict = {}
    for site in sites["sites"]:
        # if the list is empty, need to clear the blank element.
        if site["addressClassification"]["otherNetworks"] == '':
            site["addressClassification"]["otherNetworks"] = []
        site_dict[site["title"]] = site
    # Create a prefix list to be used later to remove sites from being updated.
    prefix_list = []
    for prefix in prefixes:
        # Make sure the prefix has a site configured.
        if "site" in prefix:
            # Make sure that the prefixes site is a site that already exists in kentik.
            if prefix["site"] in site_dict:
                # Make sure that the prefix is not already configured in the site.
                if prefix["prefix"] not in site_dict[prefix["site"]]["addressClassification"]["otherNetworks"]:
                    site_dict[prefix["site"]]["addressClassification"]["otherNetworks"].append(
                        prefix["prefix"])
                    prefix_list.append(prefix["site"])
            else:
                warnings.append(f"Site does not exist: {prefix["site"]}")
    # Remove sites from the update list that do not need to be updated.
    if not prefix_list:
        result = {"Sites": "No Change"}
        return result
    for name, config in site_dict.items():
        if name not in prefix_list:
            logging.info("Site (%s) does not need updated", name)
            continue
        try:
            logging.info("Updating site (%s)", name)
            response = requests.request(
                "PUT",
                f"{url}/site/v202211/sites/{config["id"]}",
                headers=kentik_auth,
                data=json.dumps({"site": config}),
                timeout=30
            )
            response.raise_for_status()
        except ConnectionError as exc:
            module.fail_json(msg=to_text(exc))
    result = {"Sites": "Success"}
    return result


def build_batch_payload(prefixes, name):
    '''Function to create the batch payload and return the set of dictionaries.'''
    json_data_src = {"replace_all": True, "complete": True, "upserts": []}
    json_data_dst = {"replace_all": True, "complete": True, "upserts": []}
    for prefix in prefixes:
        if name in prefix:
            if not json_data_src["upserts"]:
                logging.info("First pass creating the payload for %s", name)
                json_data_src["upserts"] = [{"value": prefix[name],
                                            "criteria": [{"direction": "src",
                                             "addr": [prefix["prefix"]]}]}]
                json_data_dst["upserts"] = [{"value": prefix[name],
                                            "criteria": [{"direction": "dst",
                                             "addr": [prefix["prefix"]]}]}]
            else:
                # Assuming the list is not empty we will search for an existing value.
                for index, item in enumerate(json_data_src["upserts"]):
                    if prefix[name] in item.values():
                        # If a value is found we add the prefix to that populator.
                        json_data_src["upserts"][index]["criteria"].append(
                            {"direction": "src",
                             "addr": [prefix["prefix"]]})
                        json_data_dst["upserts"][index]["criteria"].append(
                            {"direction": "dst",
                             "addr": [prefix["prefix"]]})
                    elif index == len(json_data_src["upserts"]) - 1:
                        # Otherwise we will add a new item as soon
                        # as we have searched through the entire list.
                        json_data_src["upserts"].append(
                            {"value": prefix[name],
                             "criteria": [{"direction": "src",
                                           "addr": [prefix["prefix"]]}]})
                        json_data_dst["upserts"].append(
                            {"value": prefix[name],
                             "criteria": [{"direction": "dst",
                                           "addr": [prefix["prefix"]]}]})
    return json_data_src, json_data_dst


def create_custom_dimension(module, kentik_auth, name, direction):
    '''Function to create the custom dimension'''
    if module.params["region"] == "EU":
        url = "https://api.kentik.eu/api/v5/customdimension"
    else:
        url = "https://api.kentik.com/api/v5/customdimension"
    payload = {"name": f"c_{direction}_{name}",
               "type": "string",
               "display_name": name.replace("_", " ").upper()}
    try:
        logging.info("Creating the custom dimension: %s", name)
        response = requests.request("POST",
                                    url,
                                    headers=kentik_auth,
                                    data=json.dumps(payload),
                                    timeout=30)
        if response.status_code < 200 or response.status_code >= 300:
            module.fail_json(msg=response.text)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    return response.status_code


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


def run_batch_url(module, kentik_auth, warnings, json_data_src, json_data_dst, name):
    '''Function to add populators in bulk to kentik, returns success or failure.'''
    # Start with source dimension.
    if module.params["region"] == "EU":
        url = "https://api.kentik.eu/api/v5/batch"
    else:
        url = "https://api.kentik.com/api/v5/batch"
    if len(json_data_src["upserts"]) == 0:
        return "FAILED-EMPTY"
    logging.info("Adding or updating the source custom dimensions for %s", name)
    try:
        response = requests.request("POST",
                                    f"{url}/customdimensions/c_src_{name}/populators",
                                    headers=kentik_auth,
                                    data=json.dumps(json_data_src),
                                    timeout=30)
        if response.status_code != 200 and "Invalid column" in response.json()["error"]:
            logging.info("Source dimension, %s, does not exist.", name)
            warnings.append({"Source dimension does not exist.": name})
            create_custom_dimension(module, kentik_auth, name, "src")
            response = requests.request("POST",
                                        f"{url}/customdimensions/c_src_{name}/populators",
                                        headers=kentik_auth,
                                        data=json.dumps(json_data_dst),
                                        timeout=30)
        if response.status_code < 200 and response.status_code >= 300:
            module.fail_json(msg=response.json()["error"])
        guid = response.json()["guid"]
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    times = 0
    try:
        logging.info("Validating that the source custom dimension for %s has been updated.", name)
        response = requests.request("GET", f"{url}/{guid}/status",
                                    headers=kentik_auth,
                                    data=json.dumps(json_data_src),
                                    timeout=30)
        while not response.json()["is_complete"]:
            if times < 5:
                logging.info("Validating status for %s: %s times.", name, times)
                time.sleep(5)
                response = requests.request("GET",
                                            f"{url}/{guid}/status",
                                            headers=kentik_auth,
                                            data=json.dumps(json_data_src),
                                            timeout=30)
                times += 1
            else:
                module.fail_json(msg=f"TIMEOUT - failed to validate batch status for {guid}")
                break
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    # Run the same automation for the destination custom dimensions
    try:
        logging.info("Adding or updating the destination custom dimensions for %s", name)
        response = requests.request("POST",
                                    f"{url}/customdimensions/c_dst_{name}/populators",
                                    headers=kentik_auth,
                                    data=json.dumps(json_data_dst),
                                    timeout=30)
        # Checking to see if the response code failed due to the custom dimension not being created.
        if response.status_code != 200 and "Invalid column" in response.json()["error"]:
            # Create the custom dimension and try again.
            logging.info("Destination dimension, %s, does not exist.", name)
            create_custom_dimension(module, kentik_auth, name, "dst")
            response = requests.request("POST",
                                        f"{url}/customdimensions/c_dst_{name}/populators",
                                        headers=kentik_auth,
                                        data=json.dumps(json_data_dst),
                                        timeout=30)
        if response.status_code < 200 and response.status_code >= 300:
            module.fail_json(msg=response.json()["error"])
        # Captures the GUID in order to check the status of the batch.
        guid = response.json()["guid"]
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    # Setting a counter for the while loop.
    times = 0
    # Accessing the batch status url using the guid above to ensure that the job is complete.
    try:
        logging.info(
            "Validating that the destination custom dimension for %s has been updated.", name)
        response = requests.request("GET",
                                    f"{url}/{guid}/status",
                                    headers=kentik_auth,
                                    data=json.dumps(json_data_src),
                                    timeout=30)
        # Checking for the is_complete to be true and looping until it is or the counter fails.
        while not response.json()["is_complete"]:
            if times < 5:
                logging.info("Validating status for %s: %s times.", name, times)
                time.sleep(5)
                response = requests.request("GET",
                                            f"{url}/{guid}/status",
                                            headers=kentik_auth,
                                            data=json.dumps(json_data_src),
                                            timeout=30)
                times += 1
            else:
                module.fail_json(msg=f"TIMEOUT - failed to validate batch status for {guid}")
                break
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
    # Return success to be used by the calling function.
    # No failure return is done, instead the module fails.
    return "SUCCESS"


def add_with_region(module, kentik_auth, warnings, prefixes):
    '''Function to create custom dimensions based off of region'''
    dimension = "region"
    # Build the payload.
    json_data_src, json_data_dst = build_batch_payload(prefixes, dimension)
    # Attempt to add the new elements.
    status = run_batch_url(module, kentik_auth, warnings, json_data_src, json_data_dst, dimension)
    # Setting the variable outside of the if statement first.
    result = {dimension: "Failed"}
    if status == "SUCCESS":
        result = {dimension: "Success"}
    else:
        module.fail_json(msg=f"FAILED TO ADD AND UPDATE CUSTOM DIMENSIONS FOR {dimension}")
    return result


def add_with_vlans(module, kentik_auth, warnings, prefixes):
    '''Function to create custom dimensions based off of vlan'''
    # Declaring the name of the dimension.
    dimension = module.params["vlanName"]
    # Build the payload.
    json_data_src, json_data_dst = build_batch_payload(prefixes, "vlan")
    # Attempt to add the new elements.
    status = run_batch_url(module, kentik_auth, warnings, json_data_src, json_data_dst, dimension)
    # Setting the variable outside of the if statement first.
    result = {dimension: "Failed"}
    if status == "SUCCESS":
        result = {dimension: "Success"}
    elif status == "FAILED-EMPTY":
        result[dimension] = "EMPTY"
    else:
        module.fail_json(msg=f"FAILED TO ADD AND UPDATE CUSTOM DIMENSIONS FOR {dimension}")
    return result


def add_with_tenants(module, kentik_auth, warnings, prefixes):
    '''Function to create custom dimensions based off of tenants'''
    # Declaring the name of the dimension.
    dimension = module.params["tenantName"]
    # Build the payload.
    json_data_src, json_data_dst = build_batch_payload(prefixes, "tenant")
    # Attempt to add the new elements.
    status = run_batch_url(module, kentik_auth, warnings, json_data_src, json_data_dst, dimension)
    # Setting the variable outside of the if statement first.
    result = {dimension: "Failed"}
    if status == "SUCCESS":
        result = {dimension: "Success"}
    elif status == "FAILED-EMPTY":
        result[dimension] = "EMPTY"
    else:
        module.fail_json(msg=f"FAILED TO ADD AND UPDATE CUSTOM DIMENSIONS FOR {dimension}")
    return result


def add_with_roles(module, kentik_auth, warnings, prefixes):
    '''Function to create custom dimensions based off of roles'''
    # Declaring the name of the dimension.
    dimension = module.params["roleName"]
    # Build the payload.
    json_data_src, json_data_dst = build_batch_payload(prefixes, "role")
    # Attempt to add the new elements.
    status = run_batch_url(module, kentik_auth, warnings, json_data_src, json_data_dst, dimension)
    # Setting the variable outside of the if statement first.
    result = {dimension: "Failed"}
    if status == "SUCCESS":
        result = {dimension: "Success"}
    elif status == "FAILED-EMPTY":
        result[dimension] = "EMPTY"
    else:
        module.fail_json(msg=f"FAILED TO ADD AND UPDATE CUSTOM DIMENSIONS FOR {dimension}")
    return result


def add_with_descriptions(module, kentik_auth, warnings, prefixes):
    '''Function to create custom dimensions based off of descriptions'''
    # Declaring the name of the dimension.
    dimension = module.params["descriptionName"]
    # Build the payload.
    json_data_src, json_data_dst = build_batch_payload(prefixes, "description")
    # Attempt to add the new elements.
    status = run_batch_url(module, kentik_auth, warnings, json_data_src, json_data_dst, dimension)
    # Setting the variable outside of the if statement first.
    result = {dimension: "Failed"}
    if status == "SUCCESS":
        result = {dimension: "Success"}
    elif status == "FAILED-EMPTY":
        result[dimension] = "EMPTY"
    else:
        module.fail_json(msg=f"FAILED TO ADD AND UPDATE CUSTOM DIMENSIONS FOR {dimension}")
    return result


def add_with_custom_fields(module, kentik_auth, warnings, prefixes):
    '''Function to create custom dimensions based off of custom fields'''
    # Declaring the name of the dimension. TODO: Make this settable by the user.
    dimension = module.params["customFieldName"]
    # Build the payload.
    json_data_src, json_data_dst = build_batch_payload(prefixes, dimension)
    # Attempt to add the new elements.
    status = run_batch_url(module, kentik_auth, warnings, json_data_src, json_data_dst, dimension)
    # Setting the variable outside of the if statement first.
    result = {dimension: "Failed"}
    if status == "SUCCESS":
        result = {dimension: "Success"}
    elif status == "FAILED-EMPTY":
        result[dimension] = "EMPTY"
    else:
        module.fail_json(msg=f"FAILED TO ADD AND UPDATE CUSTOM DIMENSIONS FOR {dimension}")
    return result


def main():
    """
    Main function for the program.
    Gathers arguments from the ansible module.
    Executes sub functions to perform the right job
    based on user decisions.
    """
    argument_spec = dict(
        netboxUrl=dict(type="str", required=True),
        netboxToken=dict(type="str", no_log=True, required=True),
        enableTenant=dict(type="bool", required=False, default=False),
        enableSitebyIP=dict(type="bool", required=False, default=False),
        tenantName=dict(type="str", required=False, default="tenant"),
        enableRoles=dict(type="bool", required=False, default=False),
        roleName=dict(type="str", required=False, default="role"),
        enableDescriptions=dict(type="bool", required=False, default=False),
        descriptionName=dict(type="str", required=False, default="description"),
        enableVlan=dict(type="bool", required=False, default=False),
        vlanName=dict(type="str", required=False, default="vlans"),
        enableCustomFields=dict(type="bool", required=False, default=False),
        customFieldName=dict(type="str", required=False),
        activeOnly=dict(type="bool", required=False, default=True),
        email=dict(type="str", required=True),
        token=dict(type="str", no_log=True, required=True),
        region=dict(type="str", required=False, default="US", choices=["US", "EU"])
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    # Set the initial value of the ansible results.
    result = {"changed": False}
    # Create the initial warnings list. Add to this list as warnings occur.
    warnings = []
    # Build Authentication dictionariies
    kentik_auth = build_kentik_auth(module)
    netbox_auth = build_netbox_auth(module)
    # Collec the prefixes from netbox
    prefixes = collect_prefixes(module, netbox_auth)
    decisions = gather_choices(module)
    # For each choice that is true execute the corresponding key in the dictionary,
    # which is the function.
    # Going to need to build a single jinja file for each choice
    deploy_results = []
    for option, choice in decisions.items():
        if choice:
            status = option(module,
                            kentik_auth,
                            warnings,
                            prefixes)
            deploy_results.append(status)
    # Each function will be added to the deployment list with a pass or fail
    # and/or some other message.
    # We will log the deployment output and then return the deployment status
    # list back to the main function.
    for option in deploy_results:
        if "Success" in option.values():
            result["changed"] = True
    result["results"] = deploy_results
    module.exit_json(**result)


if __name__ == "__main__":
    main()
