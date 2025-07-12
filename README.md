<div align="center">
  
[![CI](https://github.com/sr-murthy/fs-register-api-client/actions/workflows/ci.yml/badge.svg)](https://github.com/sr-murthy/fs-register-api-client/actions/workflows/ci.yml)
[![CodeQL](https://github.com/sr-murthy/fs-register-api-client/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/sr-murthy/fs-register-api-client/actions/workflows/codeql-analysis.yml)
[![codecov](https://codecov.io/github/sr-murthy/fs-register-api-client/graph/badge.svg?token=F41VZIHT2K)](https://codecov.io/github/sr-murthy/fs-register-api-client)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
[![License: MPL
2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Docs](https://readthedocs.org/projects/fs-register-api-client/badge/?version=latest)](https://fs-register-api-client.readthedocs.io/en/latest/?badge=latest)
<a href="https://trackgit.com">
<img src="https://us-central1-trackgit-analytics.cloudfunctions.net/token/ping/m45fbfbm6zgkqmfudv6m" alt="trackgit-views" />
</a>
[![PyPI version](https://img.shields.io/pypi/v/fs-register-api-client?logo=python&color=41bb13)](https://pypi.org/project/fs-register-api-client)
![PyPI Downloads](https://static.pepy.tech/badge/fs-register-api-client)

</div>

# fs-register-api-client

A lightweight Python client library for the UK [Financial Services Register](https://register.fca.org.uk/s/) [RESTful API](https://register.fca.org.uk/Developer/s/).

The [PyPI package](https://pypi.org/project/fs-register-api-client) is currently at version `0.5.1`.

The Financial Services Register, or FS Register, is a **public** database of all firms, individuals, funds, and other entities, that are either currently, or have been previously, authorised and/or regulated by the UK [Financial Conduct Authority (FCA)](https://www.fca.org.uk) and/or the [Prudential Regulation Authority (PRA)](http://bankofengland.co.uk/pra).

> [!NOTE]
> The FS Register API is free to use but accessing it, including via this library, requires [registration](https://register.fca.org.uk/Developer/ShAPI_LoginPage?ec=302&startURL=%2FDeveloper%2Fs%2F#). Registration involves a free sign up with an email, which is used as the API username in requests, and basic personal information. Once registered an API key is available from your registration profile.

See the [Sphinx documentation](https://fs-register-api-client.readthedocs.io) for more details on:

* [understanding the FS Register API](https://fs-register-api-client.readthedocs.io/sources/fs-register-api.html)
* [usage](https://fs-register-api-client.readthedocs.io/sources/usage.html)
* [contributing](https://fs-register-api-client.readthedocs.io/sources/contributing.html)
* [API reference](https://fs-register-api-client.readthedocs.io/sources/api-reference.html)
