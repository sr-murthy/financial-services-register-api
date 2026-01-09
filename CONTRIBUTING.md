# Contributing

Contributors and contributions are welcome. Please read these guidelines first.

## Git `github`

The project homepage is on [GitHub](https://github.com/sr-murthy/financial-services-register-api).

Contributors can open pull requests from a fork targeting the parent [main branch](https://github.com/sr-murthy/financial-services-register-api/tree/main). But it may be a good first step to create an [issue](https://github.com/sr-murthy/financial-services-register-api/issues) or open a [discussion topic](https://github.com/sr-murthy/financial-services-register-api/discussions).

## Repo `folder`

Setting up the project should be fairly simply once you're cloned the repo. A minimum of Python 3.10 is recommended.

It is necessary to have an API username and key from the [FCA developer portal](https://register.fca.org.uk/Developer/ShAPI_LoginPage?ec=302&startURL=%2FDeveloper%2Fs%2F#) first.

## Dependencies `cubes`

The only external dependency is [requests](https://requests.readthedocs.io/en/latest/).

Development dependencies are specified in the `[tool.pdm.dev-dependencies]` section of the [project TOML](https://github.com/sr-murthy/financial-services-register-api/blob/main/pyproject.toml), but these are purely indicative.

## Tests `microscope`

Tests are located in the `tests` folder and can be run directly or via there [Makefile](https://github.com/sr-murthy/financial-services-register-api/blob/main/Makefile) which provides a `unittests` target. Linting is done via Ruff (`make lint`) and there are also doctests (`make doctests`).

The unit and doctests require the API username (`API_USERNAME`) and key (`API_KEY`) to be available in the environment.

## Documentation `book`

This documentation site is written, built and deployed using [reStructuredText](https://docutils.sourceforge.io/rst.html), [Sphinx](https://www.sphinx-doc.org/en/master/), and [Read the Docs (RTD)](https://readthedocs.org/) respectively. The Sphinx theme used is
[Furo](https://github.com/pradyunsg/furo).

## CI `circle-play`

The CI workflows are defined [here](https://github.com/sr-murthy/financial-services-register-api/blob/main/.github/workflows/ci.yml)
and there is also a separate [CodeQL workflow](https://github.com/sr-murthy/financial-services-register-api/blob/main/.github/workflows/codeql-analysis.yml).

## Releases `upload`

The [package](https://pypi.org/project/financial-services-register-api/) is currently at version `1.3.0`.

Releases are created and published (to PyPI and GitHub) manually.
