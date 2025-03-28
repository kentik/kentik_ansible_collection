.. Document meta

:orphan:
:github_url: https://github.com/kentik/kentik_ansible_collection/edit/main/plugins/modules/kentik_device.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.16.3

.. Anchors

.. _ansible_collections.kentik.kentik_config.kentik_device_module:

.. Anchors: short name for ansible.builtin

.. Title

kentik.kentik_config.kentik_device module -- This is a module that will perform idempotent operations on kentik device management
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `kentik.kentik_config collection <https://galaxy.ansible.com/ui/repo/published/kentik/kentik_config/>`_ (version 1.2.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install kentik.kentik\_config`.

    To use it in a playbook, specify: :code:`kentik.kentik_config.kentik_device`.

.. version_added

.. rst-class:: ansible-version-added

New in kentik.kentik\_config 1.0.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- The module will gather the current list of devices from Kentik and create or update the device if it is not in the list.


.. Aliases


.. Requirements






.. Options

Parameters
----------

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cdnAttr"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-cdnattr:

      .. rst-class:: ansible-option-title

      **cdnAttr**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cdnAttr" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      If this is a DNS server, you can contribute its queries to Kentik's CDN attribution database.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"none"`
      - :ansible-option-choices-entry:`"y"`
      - :ansible-option-choices-entry:`"n"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceBgpFlowspec"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicebgpflowspec:

      .. rst-class:: ansible-option-title

      **deviceBgpFlowspec**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceBgpFlowspec" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Toggle BGP Flowspec Compatibility for device.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceBgpNeighborAsn"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicebgpneighborasn:

      .. rst-class:: ansible-option-title

      **deviceBgpNeighborAsn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceBgpNeighborAsn" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The valid AS number (ASN) of the autonomous system that this device belongs to.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceBgpNeighborIp"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicebgpneighborip:

      .. rst-class:: ansible-option-title

      **deviceBgpNeighborIp**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceBgpNeighborIp" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Your IPv4 peering address.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceBgpNeighborIp6"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicebgpneighborip6:

      .. rst-class:: ansible-option-title

      **deviceBgpNeighborIp6**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceBgpNeighborIp6" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Your IPv6 peering address.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceBgpPassword"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicebgppassword:

      .. rst-class:: ansible-option-title

      **deviceBgpPassword**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceBgpPassword" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Optional BGP MD5 password.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceBgpType"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicebgptype:

      .. rst-class:: ansible-option-title

      **deviceBgpType**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceBgpType" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      BGP (device\_bgp\_type) - Device bgp type.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"none"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"device"`
      - :ansible-option-choices-entry:`"other\_device"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceDescription"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicedescription:

      .. rst-class:: ansible-option-title

      **deviceDescription**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceDescription" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The device description.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"Added by Ansible"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceName"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicename:

      .. rst-class:: ansible-option-title

      **deviceName**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceName" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name of the device.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceSampleRate"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicesamplerate:

      .. rst-class:: ansible-option-title

      **deviceSampleRate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceSampleRate" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The rate at which the device is sampling flows.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`1`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceSnmpCommunity"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicesnmpcommunity:

      .. rst-class:: ansible-option-title

      **deviceSnmpCommunity**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceSnmpCommunity" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The SNMP community to use when polling the device.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceSnmpIp"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicesnmpip:

      .. rst-class:: ansible-option-title

      **deviceSnmpIp**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceSnmpIp" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      IP address from which the device is listening on snmp.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceSnmpV3Conf"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicesnmpv3conf:

      .. rst-class:: ansible-option-title

      **deviceSnmpV3Conf**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceSnmpV3Conf" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A dictionary with all snmpv3 attributes.

      Reference Kentik API Documentation for exact dictionary format.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-deviceSubtype"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-devicesubtype:

      .. rst-class:: ansible-option-title

      **deviceSubtype**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-deviceSubtype" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The device subtype.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"router"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"host-nprobe-dns-www"`
      - :ansible-option-choices-entry:`"aws-subnet"`
      - :ansible-option-choices-entry:`"azure\_subnet"`
      - :ansible-option-choices-entry:`"cisco\_asa"`
      - :ansible-option-choices-entry:`"gcp-subnet"`
      - :ansible-option-choices-entry:`"istio\_beta"`
      - :ansible-option-choices-entry:`"open\_nms"`
      - :ansible-option-choices-entry:`"paloalto"`
      - :ansible-option-choices-entry:`"silverpeak"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-email"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-email:

      .. rst-class:: ansible-option-title

      **email**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-email" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The Kentik API Email used to authenticate.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-labels"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-labels:

      .. rst-class:: ansible-option-title

      **labels**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-labels" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Labels that get assigned to the device.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-minimizeSnmp"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-minimizesnmp:

      .. rst-class:: ansible-option-title

      **minimizeSnmp**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-minimizeSnmp" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      IP addresses from which the device is sending flow.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-nms"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-nms:

      .. rst-class:: ansible-option-title

      **nms**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-nms" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A dictionary for adding NMS SNMP or streaming telemetry to a device.

      Reference Kentik API Documentation for exact dictionary format.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-planName"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-planname:

      .. rst-class:: ansible-option-title

      **planName**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-planName" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The ID of the plan to which this device is assigned.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-region"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-region:

      .. rst-class:: ansible-option-title

      **region**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-region" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The reqion that your Kentik portal is located in.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"US"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"EU"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-sendingIps"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-sendingips:

      .. rst-class:: ansible-option-title

      **sendingIps**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-sendingIps" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      IP addresses from which the device is sending flow.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-siteName"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-sitename:

      .. rst-class:: ansible-option-title

      **siteName**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-siteName" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The name of the site (if any) to which this device is assigned.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Whether to ensure the device should be present or if it should be removed.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-token"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-token:

      .. rst-class:: ansible-option-title

      **token**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-token" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The Kentik API Token used to authenticate.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-updateSnmpAuth"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-updatesnmpauth:

      .. rst-class:: ansible-option-title

      **updateSnmpAuth**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-updateSnmpAuth" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Update the SNMP Authentication.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-useBgpDeviceId"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__parameter-usebgpdeviceid:

      .. rst-class:: ansible-option-title

      **useBgpDeviceId**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-useBgpDeviceId" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The ID of the device whose BGP table should be shared with this device.


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

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



.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-message"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__return-message:

      .. rst-class:: ansible-option-title

      **message**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-message" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The output message that the test module generates.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"goodbye"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-original_message"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_device_module__return-original_message:

      .. rst-class:: ansible-option-title

      **original_message**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-original_message" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The original name param that was passed in.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`"hello world"`


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Ethan Angele (@kentikethan)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. ansible-links::

  - title: "Issue Tracker"
    url: "https://github.com/kentik/kentik_ansible_collection/issues"
    external: true
  - title: "Repository (Sources)"
    url: "https://github.com/kentik/kentik_ansible_collection"
    external: true
  - title: "Report an issue"
    url: "https://github.com/kentik/kentik_ansible_collection/issues/new/choose"
    external: true


.. Parsing errors
