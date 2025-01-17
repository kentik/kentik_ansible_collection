#!/bin/bash

###############################
###### EXECUTION SCRIPT ######
###############################

# This script will execute the entire netbox workflow. 
# It will install ansible and ask for appropriate variables.

######
# Step 1: Create a Python Virtual Environment
#####

echo "############################################"
echo " THIS SCRIPT WILL PREPARE YOUR ENVIRONMENT FOR EXECUTING THE KENITK <> NETBOX PLAYBOOKS"
echo "############################################"
read -p "Would you like to continue? (y or n) - " user_confirm

if [ "$user_confirm" = "n" ]; then 
    echo "NO SELECTED, EXITING THE PROGRAM"
    exit 0
fi

echo "CREATING THE VIRTUAL ENVIRONMENT"

python3 -m venv ../ansible-venv

######
# Step 2: Enter the Virtual Environment
#####

echo "ENTERING THE VIRTUAL ENVIRONMENT"

source ../ansible-venv/bin/activate

######
# Step 2: Install required python modules, including ansible
#####

echo "INSTALLING REQUIRED PYTHON MODULES"

pip install -r ../requirements.txt

echo "INSTALL COMPLETED"

######
# Step 3: Gather user environment information
#####

if [ -f "../playbooks/vars/credentials.yml" ]; then
    echo "A Credential File already exists."
    echo "If you continue, the file will be deleted"
    read -p "Would you like to continue? (y or n) " user_confirm
    if [ "$user_confirm" = "y" ]; then
        echo "Confirmed. Deleting file."
        rm ../playbooks/vars/credentials.yml
        echo "File deleted"
    else
        echo "Not confirmed. Closing program"
        exit 0
    fi
fi

read -p "Enter Kentik User Email: " kentik_email
read -s -p "Enter Kentik API Token: " kentik_token
read -p $'\n'"Enter Netbox URL: " netbox_url
read -s -p "Enter Netbox Token: " netbox_token
read -p $'\n'"Enter the SNMP Version (V2 or V3) for Flow Enrichment: " snmp_version

if [ "$snmp_version" = "V2" ]; then
    read -s -p "Enter the SNMP community: " snmp_community
else
    read -p "Enter the SNMPv3 Username: " snmp_username
    read -s -p $'\n'"Enter the SNMPv3 Auth Password: " snmp_auth
    read -s -p $'\n'"Enter the SNMPv3 Priv Password: " snmp_priv
fi
read -p $'\n'"Enter the SNMP Credential for NMS Polling: " nms_credential

echo "BUILDING ENVIRONMENT FILE"

echo "kentik_user: $kentik_email" >> ../playbooks/vars/credentials.yml
echo "kentik_token: $kentik_token" >> ../playbooks/vars/credentials.yml
if snmp_version="V2"
then
    echo "snmp_version: $snmp_version" >> ../playbooks/vars/credentials.yml
    echo "snmp_community: $snmp_community" >> ../playbooks/vars/credentials.yml
else
    echo "snmp_version: $snmp_version" >> ../playbooks/vars/credentials.yml
    echo "snmp_auth_protocol: MD5" >> ../playbooks/vars/credentials.yml
    echo "snmp_auth_password: $snmp_auth" >> ../playbooks/vars/credentials.yml
    echo "snmp_priv_protocol: AES" >> ../playbooks/vars/credentials.yml
    echo "snmp_priv_password: $snnp_priv" >> ../playbooks/vars/credentials.yml
fi
echo "netbox_token: $netbox_token" >> ../playbooks/vars/credentials.yml
echo "netbox_host: $netbox_url" >> ../playbooks/vars/credentials.yml
echo "kentik_nms_credential: $nms_credential" >> ../playbooks/vars/credentials.yml

echo "EXPORTING TOKEN"

export NETBOX_TOKEN=$netbox_token

######
# Step 4: BEGIN RUNNING PLAYBOOKS
#####

echo "YOU ARE NOW READY TO RUN THE SYNC PLAYBOOK FOR NETBOX"
echo "GO TO THE PLAYBOOKS DIRECTORY AND EDIT PLAYBOOKS TO SUIT YOUR NEEDS"
echo "IMPORTANT REMINDER"
echo "RUN ALL ANSIBLE COMMANDS USING THE PYTHON VIRTUAL ENVIRONMENT LIBRARY"
echo "../ansible-venv/bin/ansible-playbook <playbook name> -i <netbox inventory>"

exit 0