.. meta::

   :google-site-verification: 3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

============
Contributing
============

Contributors and contributions are welcome. Please read these guidelines first.

.. _contributing.git:

Git :fab:`github`
=================

The project homepage is on `GitHub <https://github.com/sr-murthy/financial-services-register-api>`_.

Contributors can open pull requests from a fork targeting the parent `main branch <https://github.com/sr-murthy/financial-services-register-api/tree/main>`_. But it may be a good first step to create an `issue <https://github.com/sr-murthy/financial-services-register-api/issues>`_ or open
a `discussion topic <https://github.com/sr-murthy/financial-services-register-api/discussions>`_.

.. _contributing.repo:

Repo :fas:`folder`
==================

Setting up the project should be fairly simply once you're cloned the repo. A minimum of Python 3.10 is recommended.

It is necessary to have an API username and key from the `FCA developer portal <https://register.fca.org.uk/Developer/ShAPI_LoginPage?ec=302&startURL=%2FDeveloper%2Fs%2F#>`_ first.

.. _contributing.dependencies-and-pdm:

Dependencies :fas:`cubes`
=========================

The only external dependency is `requests <https://requests.readthedocs.io/en/latest/>`_.

Development dependencies are specified in the ``[tool.pdm.dev-dependencies]`` section of the `project TOML <https://github.com/sr-murthy/financial-services-register-api/blob/main/pyproject.toml>`_, but these are purely indicative.

.. _contributing.tests:

Tests :fas:`microscope`
=======================

Tests are located in the ``tests`` folder and can be run directly or via there `Makefile <https://github.com/sr-murthy/financial-services-register-api/blob/main/Makefile>`_ which provides a ``unittests`` target. Linting is done via Ruff (``make lint``) and there are also doctests (``make doctests``).

The unit and doctests require the API username (``API_USERNAME``) and key (``API_KEY``) to be available in the environment.

.. _contributing.documentation:

Documentation :fas:`book`
=========================

This documentation site is written, built and deployed using `reStructuredText <https://docutils.sourceforge.io/rst.html>`_, `Sphinx <https://www.sphinx-doc.org/en/master/>`_, and `Read the Docs (RTD) <https://readthedocs.org/>`_ respectively. The Sphinx theme used is `Furo <https://github.com/pradyunsg/furo>`_.

.. _contributing.ci:

CI :fas:`circle-play`
=====================

The CI workflows are defined `here <https://github.com/sr-murthy/financial-services-register-api/blob/main/.github/workflows/ci.yml>`_ and there is also a separate `CodeQL workflow <https://github.com/sr-murthy/financial-services-register-api/blob/main/.github/workflows/codeql-analysis.yml>`_.

.. _contributing.versioning-and-releases:

Releases :fas:`upload`
======================

The `package <https://pypi.org/project/financial-services-register-api/>`_ is currently at version ``1.2.0``.

Releases are created and published (to PyPI and GitHub) manually.
