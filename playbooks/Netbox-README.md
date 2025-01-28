

# Kentik Netbox Ansible Integration



- [Installing the Kentik Netbox Integration](#installing-the-kentik-netbox-integration)
	- [Tested Distributions](#tested-distributions)
	- [Example Debian 12 installation](#example-debian-12-installation)
	- [Python Virtual Environment Install](#python-virtual-environment-install)
- [Understanding the main Playbook](#understanding-the-main-playbook)
- [Building the dynamic Netbox inventory](#building-the-dynamic-netbox-inventory)
<br/>


## Installing the Kentik Netbox integration

### Requirements

The Kentik Netbox integration playbooks require Ansible v2.14.2 or later. 

A full list of Python modules can be found in the requirements.txt file in the root directory of the repo. To install these modules with the appropriate minimum versions you can use pip3:

````
pip3 install -r requirements.txt
````


### Tested Distributions

This integration can work on any ansible platform that meets the version requirements, but we have explicity tested using the following distributions:

#### RHEL based
**Rocky Linux** 8 - *May require using python virtual environment to meet versionm requirements*<br/>
**Rocky Linux 9** 

#### Debian Based
**Debian 11, 12**<br/>
**Ubuntu 22.04, 24.04**

If your distribution is not listed you can still install the integration using a Python virtual environment. 

### Example Debian 12 installation

From a fresh install of Debian 12, these are the steps required to run the Kentik/Netbox Ansible integration:

Install Ansible
```
sudo apt install ansible
```

install the Kentik galaxy collection
```
ansible-galaxy collection install kentik.kentik_config
```

install the Netbox galaxy collection
```
ansible-galaxy collection install netbox.netbox
```

Clone the repo:
```
git clone https://github.com/kentik/kentik_ansible_collection.git
```

Edit `playbooks/netbox_inventory.yml` and replace the hostname
```
https://mycloudinstance.cloud.netboxapp.com/
```

Create a `credentials.yml` file under `./playbooks/vars`

```
kentik_user: "bofh@corporate.com"
kentik_token: "01234DEADBEEF56789102112"
netbox_host: "mycloudinstance.cloud.netboxapp.com"
netbox_token: "lkajsdlkjSEATECASTRONOMYasdkjalsdkj"
```

Export your netbox key as an evironment variable:
```
export NETBOX_TOKEN="lkajsdlkjSEATECASTRONOMYasdkjalsdkj"
```

Finally, Execute the playbook:
```
ansible-playbook pb_netbox_sync.yml -i netbox_inventory.yml
```


### Python Virtual Environment Install

If your particular OS Distribution does not support the minimum versions of Ansible and associated Python modules you can install the integration using a Python Virtual Environment (venv).

Install the Python venv package if it is not already installed on the system *(assuming debian based, use yum for RHEL)*
```
sudo apt install python3-venv
```

Create a new python virtual environment
```
python3 -m venv venv
```

Activate your new environment 
```
source venv/bin/activate
```

Install the required modules in your new virtual environment
```
pip3 install -r requirements.txt
```

Finally, execute the playbook
```
ansible-playbook pb_netbox_sync.yml -i netbox_inventory.yml
```


If these instructions are not complete or missing items, please open a Github issue and we will try to resolve the issue. 



## Understanding the main Playbook

The main Ansible playbook for this integration is `pb_netbox_sync.yml`. 

Breaking it down by section, here is the structure of the playbook:

- Get a list of sites from Netbox
- Create the sites in Kentik
- Gather device roles, tenants and tags from Netbox
- Create Kentik labels using device roles, tenants and tags as a source
- Create the list of devices in Kentik with:
	- The appropriate Site
	- The device role (as a Kentik label)
	- The tenant (as a Kentik label)
	- The tag (as a Kentik lablel)

Where possible, we try to maintain the color of the labels from Netbox. 

Finally, when we execute the playbook, rather than specifying specific devices to run it against, we build a [[#Building the dynamic Netbox inventory|dynamic inventory]] from Netbox. 

```
ansible-playbook pb_netbox_sync.yml -i netbox_inventory.yml
```
### Adding Flow only Devices

By default, The playbook comes configured to add devices for both Kentik Flow collection and for Kentik NMS. If you have devices that should be only added for flow collection, simply comment out the NMS subsection:

```yaml
    - name: Create Device
      kentik.kentik_config.kentik_device:
        deviceName: "{{ inventory_hostname }}"
        deviceSampleRate: 10
        planName: Free Flowpak Plan
        siteName: "{{ sites[0] }}"
        sendingIps: ["{{ primary_ip4 }}"]
        deviceSnmpIp: "{{ primary_ip4 }}"
        deviceSnmpCommunity: kentik
        minimizeSnmp: false
        #nms:
        #    agentId: "27"
        #    ipAddress: "{{ primary_ip4 }}"
        #    snmp:
        #        credentialName: default
        labels: "{{ tags }}"
        email: "{{ kentik_user }}"
        token: "{{ kentik_token }}"
      delegate_to: localhost
```
<br/>

### Adding NMS only devices

If you wish to add devices to the Kentik NMS platform and not for flow collection, you can signal this by removing the flow related fields as shown below and by changing the plan name to the relevant Kentik NMS plan. 

```yaml
    - name: Create Device
      kentik.kentik_config.kentik_device:
        deviceName: "{{ inventory_hostname }}"
        #deviceSampleRate: 10
        planName: my-metrics-plan
        siteName: "{{ sites[0] }}"
        #sendingIps: ["{{ primary_ip4 }}"]
        #deviceSnmpIp: "{{ primary_ip4 }}"
        #deviceSnmpCommunity: kentik
        #minimizeSnmp: false
        nms:
            agentId: "27"
            ipAddress: "{{ primary_ip4 }}"
            snmp:
                credentialName: default
        labels: "{{ tags }}"
        email: "{{ kentik_user }}"
        token: "{{ kentik_token }}"
      delegate_to: localhost
```



## Building the dynamic Netbox inventory

 To build an inventory of devices that we wish to synchronize with Kentik. We achieve this by using the Netbox Inventory Galaxy Collection. By default we will pull all devices down, but you can un-comment one of the variable under `device_query_filters` to filter the list of devices down to something more specific. In this example, we will only select devices that have the `kentik_flow` label applied to them in Netbox. Another option would be to use a variable such as the `device role` field in Netbox. 

```yaml
plugin: netbox.netbox.nb_inventory
api_endpoint: https://mycloudinstance.cloud.netboxapp.com/
validate_certs: False
config_context: False
device_query_filters:
  - has_primary_ip: 'true'
  - tag: 'kentik_flow'
  #- role: 'edge-router'
```

<br/>

