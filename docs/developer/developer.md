# Developer Guide

[TOC]

## Testing

To run the tests, you need to install the development dependencies. You can do this by running:

```bash
pip install pyyaml pytest pytest-dependency
```

Then, you have to cd into the `tests` directory:

```bash
cd tests
```

Then, you can run the tests with:

```bash
pytest test.py -v
```

## Mkdocs

To host the documentation on localhost for testing, you need to install the development dependencies. You can do this by running:

```bash
pip install mkdocs
```

```bash
pip install mkdocstrings-python
```

Then, you have to run the following command:

```bash
mkdocs serve
```
