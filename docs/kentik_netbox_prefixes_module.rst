.. Document meta

:orphan:
:github_url: https://github.com/kentik/kentik_ansible_collection/edit/main/plugins/modules/kentik_netbox_prefixes.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.16.3

.. Anchors

.. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module:

.. Anchors: short name for ansible.builtin

.. Title

kentik.kentik_config.kentik_netbox_prefixes module -- This is a module that will perform idempotent operations to synchronize netbox prefixes.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `kentik.kentik_config collection <https://galaxy.ansible.com/ui/repo/published/kentik/kentik_config/>`_ (version 1.2.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install kentik.kentik\_config`.

    To use it in a playbook, specify: :code:`kentik.kentik_config.kentik_netbox_prefixes`.

.. version_added

.. rst-class:: ansible-version-added

New in kentik.kentik\_config 1.2.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- The module will gather the list of prefixes from netbox and then proceed to create kentik elements with them depending on the users selection.


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
        <div class="ansibleOptionAnchor" id="parameter-activeOnly"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-activeonly:

      .. rst-class:: ansible-option-title

      **activeOnly**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-activeOnly" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Only add prefixes that are active in Netbox.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-customFieldName"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-customfieldname:

      .. rst-class:: ansible-option-title

      **customFieldName**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-customFieldName" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Custom Field to add as a custom dimension.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-descriptionName"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-descriptionname:

      .. rst-class:: ansible-option-title

      **descriptionName**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-descriptionName" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The custom dimension name to be used for description.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"description"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-email"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-email:

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
        <div class="ansibleOptionAnchor" id="parameter-enableCustomFields"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-enablecustomfields:

      .. rst-class:: ansible-option-title

      **enableCustomFields**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-enableCustomFields" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Creat custom dimensions based on the prefix Custom Fields.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-enableDescriptions"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-enabledescriptions:

      .. rst-class:: ansible-option-title

      **enableDescriptions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-enableDescriptions" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Create custom dimensions based on the prefix Descriptions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-enableRoles"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-enableroles:

      .. rst-class:: ansible-option-title

      **enableRoles**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-enableRoles" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Create custom dimensions based on the prefix Role.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-enableSitebyIP"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-enablesitebyip:

      .. rst-class:: ansible-option-title

      **enableSitebyIP**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-enableSitebyIP" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Add the IP addresses to the Site.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-enableTenant"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-enabletenant:

      .. rst-class:: ansible-option-title

      **enableTenant**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-enableTenant" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Create custom dimensions based on the prefix Tenant.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-enableVlan"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-enablevlan:

      .. rst-class:: ansible-option-title

      **enableVlan**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-enableVlan" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Create custom dimensions based on the prefix Vlan.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-netboxToken"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-netboxtoken:

      .. rst-class:: ansible-option-title

      **netboxToken**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-netboxToken" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The Netbox Token to use for authentication.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-netboxUrl"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-netboxurl:

      .. rst-class:: ansible-option-title

      **netboxUrl**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-netboxUrl" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The Netbox Url to collect the prefixes from.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-region"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-region:

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
        <div class="ansibleOptionAnchor" id="parameter-roleName"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-rolename:

      .. rst-class:: ansible-option-title

      **roleName**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-roleName" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The custom dimension name to be used for roles.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"role"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-tenantName"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-tenantname:

      .. rst-class:: ansible-option-title

      **tenantName**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-tenantName" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The custom dimension name to be used for tenants.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"tenant"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-token"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-token:

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
        <div class="ansibleOptionAnchor" id="parameter-vlanName"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__parameter-vlanname:

      .. rst-class:: ansible-option-title

      **vlanName**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-vlanName" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The custom dimension name to be used for vlans.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"vlans"`

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

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__return-message:

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

      .. _ansible_collections.kentik.kentik_config.kentik_netbox_prefixes_module__return-original_message:

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
