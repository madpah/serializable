# Contributing

Pull requests are welcome, but please read this guidelines first.

## Setup

This project uses [poetry]. Have it installed and setup first.

Attention:
Even though this library is designed to be runnable on python>=3.8.0
some development-tools require python>=3.8.1

To install dev-dependencies and tools:

```shell
poetry install
```

## Code style

This project loves latest python features.
This project uses [PEP8] Style Guide for Python Code.  
This project loves sorted imports.

Get it all applied via:

```shell
poetry run -- tox r -e pyupgrade -- --exit-zero-even-if-changed
poetry run -- tox r -e isort
poetry run -- tox r -e autopep8
```

This project prefers `f'strings'` over `'string'.format()`.  
This project prefers `'single quotes'` over `"double quotes"`.  

## Documentation

This project uses [Sphinx] to generate documentation which is automatically published to [RTFD][link_rtfd].

Source for documentation is stored in the `docs` folder in [RST] format.

You can generate the documentation locally by running:

```shell
cd docs
pip install -r requirements.txt
make html
```

## Testing

```shell
poetry run tox
```

## Sign your commits

Please sign your commits,
to show that you agree to publish your changes under the current terms and licenses of the project.

```shell
git commit --signed-off ...
```

[poetry]: https://python-poetry.org
[PEP8]: https://www.python.org/dev/peps/pep-0008/
[Sphinx]: https://www.sphinx-doc.org/
[link_rtfd]: https://py-serializable.readthedocs.io/
[RST]: https://en.wikipedia.org/wiki/ReStructuredText
