# Ansible Playbooks for Kentik

## Setup Authentication

First step is to create a copy of the credential file and name it credentials.yml under the vars directory.

## Playbooks

The following playbooks are available today for managing Kentik with Ansible:

### [Sync Netbox to Kentik](Netbox-README.md)

This playbook synchronizes Netbox device inventory data to Kentik. It uses the Netbox Ansible Galaxy collection to dynamically build the device inventory which allows you to apply filters such as device role or label. For example, you can have only devices that have the `kentik_flow` label or only devices that have the device role of `core`, etc. 

This playbook also synchronizes sites, labels and tenants between platforms so when devices are created within Kentik they are placed within the appropriate Kentik site and have the appropriate Kentik labels applied. 

A more detailed set of instructions can be [found here](Netbox-README.md). 
<br/>

### Sync Nautobot to Kentik
  
Like the Netbox playbook, this playbook Synchronizes Nautobot inventory data with the Kentik platform. This playbook will take each of the devices from the inventory and verify that it is created in Kentik and if not create it, associate it with the correct site, and apply the right labels. It will first gather all sites, tenants, and roles from Nautobot and create them as sites and labels in Kentik. Then it will create the device assigned to the right site and associate it with the right labels. 

To use the environment variables for authentication use the following:

```
	- KENTIK_EMAIL
    - KENTIK_TOKEN
    - NAUTOBOT_TOKEN
    - KENTIK_REGION
```
   
Be sure to create the credential file with other local creds. 
<br/>


### Updating SNMP device settings
  This playbook will update SNMPv3 and SNMPv2 authentication settings for the devices listing in the inventory that the playbook is ran against. The run this playbook, the user must do the following:
    1. Create an inventory file with the list of devices that will be updated. The device names in this inventory must match the device names in Kentik. The device names will also need to be resolvable by DNS, if not the user will need to add the ip address to the inventory file with the device name like so: `device1 ansible_host=1.1.1.1` 
    2. The user will need to duplicate the template_kentik_snmp_var.yml file under the vars directory and name it credentials.yml. After duplicating it, then add all the appropriate settings to the file.
  
  To the Run the playbook, type `ansible-playbook pb_update_kentik_snmp.yml -i inventory_file`

### Sync two address based custom dimensions
  This playbook will take two custom dimension IDs as input. One ID is the "FROM" (the dimension to be copied) and the second ID is the "TO" (the dimension to sync/copy the FROM).
  
  - To use this playbook all you need are those two dimensions handy and the credential file.
    - The user will need to duplicate the template_kentik_snmp_var.yml file under the vars directory and name it credentials.yml. After duplicating it, then add all the appropriate settings to the file.
  - Limitions
    - Only values with one address to value mapping is supported.
    - Only ip address values are supported. 
    - The maximum number of populators is unknown for this playbook and may be something you run into.


  
-- happy automating
