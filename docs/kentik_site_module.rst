.. Document meta

:orphan:
:github_url: https://github.com/kentik/kentik_ansible_collection/edit/main/plugins/modules/kentik_site.py?description=%23%23%23%23%23%20SUMMARY%0A%3C!---%20Your%20description%20here%20--%3E%0A%0A%0A%23%23%23%23%23%20ISSUE%20TYPE%0A-%20Docs%20Pull%20Request%0A%0A%2Blabel:%20docsite_pr

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.16.3

.. Anchors

.. _ansible_collections.kentik.kentik_config.kentik_site_module:

.. Anchors: short name for ansible.builtin

.. Title

kentik.kentik_config.kentik_site module -- This is a module that will perform idempotent operations on kentik site management.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `kentik.kentik_config collection <https://galaxy.ansible.com/ui/repo/published/kentik/kentik_config/>`_ (version 1.2.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install kentik.kentik\_config`.

    To use it in a playbook, specify: :code:`kentik.kentik_config.kentik_site`.

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

- The module will gather the current list of sites from Kentik and create the site if it is not in the list.


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
        <div class="ansibleOptionAnchor" id="parameter-email"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-email:

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
        <div class="ansibleOptionAnchor" id="parameter-infrastructureNetworks"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-infrastructurenetworks:

      .. rst-class:: ansible-option-title

      **infrastructureNetworks**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-infrastructureNetworks" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Network subnets that connect to other network devices.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-lat"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-lat:

      .. rst-class:: ansible-option-title

      **lat**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-lat" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`float`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The latitude of the site.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`0.0`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-lon"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-lon:

      .. rst-class:: ansible-option-title

      **lon**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-lon" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`float`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The longitude of the site.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`0.0`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-otherNetworks"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-othernetworks:

      .. rst-class:: ansible-option-title

      **otherNetworks**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-otherNetworks" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Network subnets that connect to something other then what is noted above.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-postalAddress"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-postaladdress:

      .. rst-class:: ansible-option-title

      **postalAddress**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-postalAddress" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The physicall address of the site.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-region"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-region:

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
        <div class="ansibleOptionAnchor" id="parameter-siteMarket"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-sitemarket:

      .. rst-class:: ansible-option-title

      **siteMarket**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-siteMarket" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of the Site Market this site belongs to.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-state:

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

      States whether to delete or create.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"present"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"absent"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-title"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-title:

      .. rst-class:: ansible-option-title

      **title**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-title" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The site name to be displayed and referenced going forward.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-token"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-token:

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
        <div class="ansibleOptionAnchor" id="parameter-type"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-type:

      .. rst-class:: ansible-option-title

      **type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The type of site this is, see choices for options.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"SITE\_TYPE\_DATA\_CENTER"`
      - :ansible-option-choices-entry:`"SITE\_TYPE\_CLOUD"`
      - :ansible-option-choices-entry:`"SITE\_TYPE\_BRANCH"`
      - :ansible-option-choices-entry:`"SITE\_TYPE\_CONNECTIVITY"`
      - :ansible-option-choices-entry:`"SITE\_TYPE\_CUSTOMER"`
      - :ansible-option-choices-entry-default:`"SITE\_TYPE\_OTHER"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-userAccessNetworks"></div>

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__parameter-useraccessnetworks:

      .. rst-class:: ansible-option-title

      **userAccessNetworks**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-userAccessNetworks" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Network subnets that connect to end users ot servers.


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
    - name: Create a Site
      kentik_site:
        title: LA1
        postalAddress:
                address: 600 W 7th Street,
                city: Los Angeles,
                country: US
        type: SITE_TYPE_DATA_CENTER
    - name: Create a Site in EU Cluster
      kentik_site:
        title: LA1
        postalAddress:
                address: 600 W 7th Street,
                city: Los Angeles,
                country: US
        type: SITE_TYPE_DATA_CENTER
        region: EU

    # fail the module
    - name: Test failure of the module
      create_kentik_site:
        title: fail me because site type not included



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

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__return-message:

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

      .. _ansible_collections.kentik.kentik_config.kentik_site_module__return-original_message:

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
