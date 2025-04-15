# Kentik Collection for Ansible
The Kentik Collection for using Ansible to manage the Kentik portal configuration elements such as sites, devices, and labels. 

## Code of Conduct
We follow the Ansible Code of Conduct in all our interactions within this project.

If you encounter abusive behavior, please refer to the policy violations section of the Code for information on how to raise a complaint.

## Communication
Join us on:

- Email: 
    - [Support email](support@kentik.com): Email alias for opening tickets and requesting support from Kentik
- Slack: 
    - [Kentik Users](https://www.kentik.com/go/offer/kentik-community-slack-signup/): Slack workspace for all Kentik users to colloborate

For more information about communication with the Ansible community, refer to the Ansible communication guide.

## Contributing to this collection
The content of this collection is made by people like you, a community of individuals collaborating on making the world better through developing automation software.

We are actively accepting new contributors and all types of contributions are very welcome.

Don't know how to start? Refer to the Ansible community guide!

If you find problems, please open an issue or create a PR against the Kentik collection repository.

See CONTRIBUTING.md for more details.

We also use the following guidelines:
- Collection review checklist
- Ansible development guide
- Ansible collection development guide

## Tested with Ansible
Tested with Ansible Core >= 2.14.2 versions, and the current development version of Ansible. Ansible Core versions prior to 2.14.2 are not supported.

## External requirements
- [Kentik portal account](https://portal.kentik.com)

## Example playbook
    ---
    - name: "Create Kentik Device"
    hosts: all
    gather_facts: false
    vars_files:
        - ./vars/credentials.yml

    - name: Create Device
        kentik_device:
            device_name: "access_switch_01"
            device_sample_rate: 10
            plan_name: Free Flowpak Plan
            site_name: "Seattle"
            sending_ips: ["192.0.2.100"]
            device_snmp_ip: "192.0.2.100"
            device_snmp_community: kentik
            nms:
                agentId: "183" # random agent id.
                ipAddress: "192.0.2.100"
                snmp:
                    credentialName: snmp_v2_read_only
            labels: ["access switch", "end users"]
        delegate_to: localhost

## Installing the Collection from Ansible Galaxy
Before using this collection, you need to install it with the Ansible Galaxy command-line tool:

    ansible-galaxy collection install kentik.kentik_config
    
You can also include it in a requirements.yml file and install it with ansible-galaxy collection install -r requirements.yml, using the format:

    ---
    collections:
    - name: kentik.kentik_config

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the ansible package. To upgrade the collection to the latest available version, run the following command:

    ansible-galaxy collection install kentik.kentik_config --upgrade

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version 0.1.0:

    ansible-galaxy collection install kentik.kentik_config:==1.0.0

See using Ansible collections for more details.

## Release notes
See the changelog.

## Licensing
GNU General Public License v3.0 or later.

See LICENSE to see the full text.

## Additional Questions/Remarks
If you do have additional questions/remarks, feel free to reach out to Kentik support, via email.

If you think this template did not solve all your problems, please also let us know, either with a message or a pull request. Together we can improve this template to make it easier for our future projects.
