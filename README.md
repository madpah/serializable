# py-serializable

[![shield_pypi-version]][link_pypi]
[![shield_conda-forge-version]][link_conda-forge]
[![shield_rtfd]][link_rtfd]
[![shield_gh-workflow-test]][link_gh-workflow-test]
[![shield_license]][license_file]
[![shield_twitter-follow]][link_twitter]

----

This Pythonic library provides a framework for serializing/deserializing Python classes to and from JSON and XML.

It relies upon the use of 
[Python Properties](https://docs.python.org/3/library/functions.html?highlight=property#property) in your Python
classes.

Read the full [documentation][link_rtfd] for more details.

## Installation

Install this from [PyPi.org][link_pypi] using your preferred Python package manager.

Example using `pip`:

```shell
pip install py-serializable
```

Example using `poetry`:

```shell
poetry add py-serializable
```

## Usage

See the full [documentation][link_rtfd] or our [unit tests][link_unit_tests] for usage and details.

## Python Support

We endeavour to support all functionality for all [current actively supported Python versions](https://www.python.org/downloads/).
However, some features may not be possible/present in older Python versions due to their lack of support.

## Contributing

Feel free to open issues, bugreports or pull requests.  
See the [CONTRIBUTING][contributing_file] file for details.

## Copyright & License

`py-serializable` is Copyright (c) Paul Horton 2022. All Rights Reserved.

Permission to modify and redistribute is granted under the terms of the Apache 2.0 license.  
See the [LICENSE][license_file] file for the full license.

[license_file]: https://github.com/madpah/serializable/blob/main/LICENSE
[contributing_file]: https://github.com/madpah/serializable/blob/main/CONTRIBUTING.md
[link_rtfd]: https://py-serializable.readthedocs.io/

[shield_gh-workflow-test]: https://img.shields.io/github/actions/workflow/status/madpah/serializable/python.yml?branch=main "build"
[shield_rtfd]: https://img.shields.io/readthedocs/py-serializable?logo=readthedocs&logoColor=white
[shield_pypi-version]: https://img.shields.io/pypi/v/py-serializable?logo=Python&logoColor=white&label=PyPI "PyPI"
[shield_conda-forge-version]: https://img.shields.io/conda/vn/conda-forge/py-serializable?logo=anaconda&logoColor=white&label=conda-forge "conda-forge"
[shield_license]: https://img.shields.io/github/license/madpah/serializable?logo=open%20source%20initiative&logoColor=white "license"
[shield_twitter-follow]: https://img.shields.io/badge/Twitter-follow-blue?logo=Twitter&logoColor=white "twitter follow"
[link_gh-workflow-test]: https://github.com/madpah/serializable/actions/workflows/python.yml?query=branch%3Amain
[link_pypi]: https://pypi.org/project/py-serializable/
[link_conda-forge]: https://anaconda.org/conda-forge/conda-forge
[link_twitter]: https://twitter.com/madpah
[link_unit_tests]: https://github.com/madpah/serializable/blob/main/tests
