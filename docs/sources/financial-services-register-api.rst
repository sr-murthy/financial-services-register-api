.. meta::

   :google-site-verification: 3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

=================================================
Understanding the Financial Services Register API
=================================================

The package functionality reflects the current version (``V0.1``) of the `Financial Services Register <https://www.fca.org.uk/firms/financial-services-register>`_ `API <https://register.fca.org.uk/Developer/s/>`_. The API is documented but access requires registration.

The base URL for all API requests is:

.. code:: shell

   https://register.fca.org.uk/services/V0.1

.. _fs-register-api.resources-and-request-types:

Resources and Endpoints
=======================

There are three main categories of resource about which information can be requested from the register via API endpoints:

- **firms** - authorised and/or regulated firms (either current or past) involved with the provision of regulated products and/or services. Firms in the register have unique **firm reference numbers (FRN)** and their endpoints usually take these as one of the parameters. They are described in more detail :ref:`here <fs-register-api.firm-requests>`.
- **individuals** - individuals associated with the type of firms described above, either current or past.  Individuals in the register have unique **individual reference numbers (IRN)** and their endpoints usually take these as one of the parameters. They are described in more detail :ref:`here <fs-register-api.individual-requests>`.
- **funds** - investment funds or collective investment schemes (CIS),including subfunds of funds. Funds in the register have unique **product reference numbers (PRN)** and their endpoints usually take these as one of the parameters. They are described in more detail :ref:`here <fs-register-api.fund-requests>`.

There are also search endpoints that allow a search for *(a)* any of these resources by a name substring and a corresponding type specification (firm, individual, or fund), or *(b)* `regulated markets <https://www.handbook.fca.org.uk/handbook/glossary/G978.html?date=2007-01-20>`_. These are described in more detail :ref:`here <fs-register-api.common-search-requests>`.

.. _fs-register-api.request-headers:

Request Headers
===============

For developers and end users the API, and this Python client library, is read-only - all requests must use ``GET``, and include headers containing the API username and key:

.. code:: shell

   ACCEPT: application/json
   X-AUTH-EMAIL: <signup email / API username>
   X-AUTH-KEY: <API key>

.. _fs-register-api.rate-limiting:

Rate Limiting
=============

According to the `API documentation <https://register.fca.org.uk/Developer/s/>`_ **rate limiting** is applied to set a **maximum of 50 requests per 10 seconds per user**, and **breaches** lead to `(HTTP 429) errors <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429>`__ and **requests being blocked for 1 minute**.

.. warning::

   Please use the API and this library responsibly, and do not make excessive requests or use it in an otherwise inappropriate way.

.. _fs-register-api.firm-requests:

Firm Requests
=============

Firms in the Register are identified by unique firm reference numbers (FRN). The following table summarises firm-specific API endpoints. For further details consult the `API documentation <https://register.fca.org.uk/Developer/s/>`_.

.. list-table::
   :align: left
   :widths: 75 15 30
   :header-rows: 1

   * - API Endpoint
     - Request Method
     - Resource Parameters
   * - ``/V0.1/Firm/{FRN}``
     - GET
     - FRN (str)
   * - ``/V0.1/Firm/{FRN}/Address``
     - GET
     - FRN (str)
   * - ``/V0.1/Firm/{FRN}/AR``
     - GET
     - FRN (str)
   * - ``/V0.1/Firm/{FRN}/CF``
     - GET
     - FRN (str)
   * - ``/V0.1/Firm/{FRN}/DisciplinaryHistory``
     - GET
     - FRN (str)
   * - ``/V0.1/Firm/{FRN}/Exclusions``
     - GET
     - FRN (str)
   * - ``/V0.1/Firm/{FRN}/Individuals``
     - GET
     - FRN (str)
   * - ``/V0.1/Firm/{FRN}/Names``
     - GET
     - FRN (str)
   * - ``/V0.1/Firm/{FRN}/Passports``
     - GET
     - FRN (str)
   * - ``/V0.1/Firm/{FRN}/Passports/{Country}/Permission``
     - GET
     - FRN (str), Country (str)
   * - ``/V0.1/Firm/{FRN}/Permissions``
     - GET
     - FRN (str)
   * - ``/V0.1/Firm/{FRN}/Regulators``
     - GET
     - FRN (str)
   * - ``/V0.1/Firm/{FRN}/Requirements``
     - GET
     - FRN (str)
   * - ``/V0.1/Firm/{FRN}/Requirements/{Requirement Reference}/InvestmentTypes``
     - GET
     - FRN (str), Requirement Reference (str)
     

.. note::

   The abbreviations “CF” and “AR” refer to “controlled functions” and “appointed representatives” respectively.

For details and examples on calling these endpoints via this library see :ref:`this <usage.firms>`.

.. _fs-register-api.individual-requests:

Individual Requests
===================

Individuals associated with firms in the Register are identified by unique individual reference numbers (IRN). The following table summarises individual-specific API endpoints.

.. list-table::
   :align: left
   :widths: 75 15 30
   :header-rows: 1

   * - API Endpoint
     - Request Method
     - Resource Parameters
   * - ``/V0.1/Individuals/{IRN}``
     - GET
     - IRN (str)
   * - ``/V0.1/Individuals/{IRN}/CF``
     - GET
     - IRN (str)
   * - ``/V0.1/Individuals/{IRN}/DisciplinaryHistory`` 
     - GET
     - IRN (str)

.. note::

   The abbreviation “CF” refers to “controlled functions”.

For how to call these endpoints see :ref:`this <usage.individuals>`.

.. _fs-register-api.fund-requests:

Fund Requests
=============

Funds, also referred to as collective investment schemes (CIS) in the Register, are identified by unique product reference numbers (PRN). The following table summarises fund-specific API endpoints.

.. list-table::
   :align: left
   :widths: 75 15 30
   :header-rows: 1

   * - API Endpoint
     - Request Method
     - Resource Parameters
   * - ``/V0.1/CIS/{PRN}``
     - GET
     - PRN (str)
   * - ``/V0.1/CIS/{PRN}/Names``
     - GET
     - PRN (str)
   * - ``/V0.1/CIS/{PRN}/Subfund``
     - GET
     - PRN (str)

For details and examples of calling these endpoints via this library see :ref:`this <usage.funds>`.

.. _fs-register-api.common-search-requests:

Common Search Requests
======================

The common search API endpoint is a parameterised search endpoint which is summarised below.

.. list-table::
   :align: left
   :widths: 75 15 30
   :header-rows: 1

   * - API Endpoint
     - Request Method
     - Search Parameters
   * - ``/V0.1/Search``
     - GET
     - ``q`` (resource name), ``type`` (resource type - ``'firm'``, ``'individual'``, or ``'fund'``)

Requests should be of the form:

.. code:: http

   GET https://register.fca.org.uk/services/V0.1/Search?q=resource_name&type=resource_type HTTP/1.1

For example, here are a few valid common search requests.

* Common search for Barclays Bank Plc (FRN #122702):

.. code:: http

   GET https://register.fca.org.uk/services/V0.1/Search?q=Barclays+Bank+plc&type=firm HTTP/1.1

* Common search for Hastings Insurance Services Limited (FRN #311492)

.. code:: http
   
   GET https://register.fca.org.uk/services/V0.1/Search?q=hastings+insurance+services&type=firm HTTP/1.1

* Common search for all Natwest-related firms:

.. code:: http
   
   GET https://register.fca.org.uk/services/V0.1/Search?q=Natwest&type=firm HTTP/1.1

* Common search for a specific individual, Mark Carney (IRN #MXC29012):

.. code:: http
   
   GET https://register.fca.org.uk/services/V0.1/Search?q=mark+carney&type=individual HTTP/1.1

* Common search for a generic individual name "John Smith", with multiple results:

.. code:: http
   
   GET https://register.fca.org.uk/services/V0.1/Search?q=John+Smith&type=individual HTTP/1.1

* Common search for a specific fund, Jupiter Asia Pacific Income (PRN #635641):

.. code:: http
   
   GET https://register.fca.org.uk/services/V0.1/Search?q=jupiter+asia+pacific+income&type=fund HTTP/1.1

* Common search for a specific fund, abrdn Multi-Asset Fund (PRN #637980):

.. code:: http
   
   GET https://register.fca.org.uk/services/V0.1/Search?q=abrdn+multi-asset+fund&type=fund HTTP/1.1

One particular type of common search-based endpoint that the API provides separately is for `regulated markets <https://www.handbook.fca.org.uk/handbook/glossary/G978.html?date=2007-01-20>`_. These are special markets which are regulated by UK and/or EU/EEA financial legislation. API requests for regulated markets should look as below:

.. code:: http

   GET https://register.fca.org.uk/services/V0.1/CommonSearch?q=RM HTTP/1.1

For details and examples on calling these endpoint via this library see :ref:`this <usage.common-search>`.
