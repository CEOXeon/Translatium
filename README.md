# Translatium

Translatium is a pure Python library for managing translations in your application. It provides a simple and flexible way to handle translations, with support for YAML and JSON file formats.

## Features

- **Translations**: Translatium allows you to define translations for your application, with support for simple strings and complex, nested translations.
- **Freedom to Choose**: You have complete control over how you structure your translation data, and Translatium provides the tools to make it work.
- **Explicit Error Handling**: Translatium throws errors as soon as possible, so you can catch and handle issues before they reach production.
- **Flexible File Formats**: Translatium supports both YAML and JSON file formats, so you can choose the one that works best for you.
- **Pure Python**: Translatium is written in pure Python.

## Installation

```bash
pip install translatium
```

## Quick Start

```python
from pathlib import Path
from translatium import Translator

# Define a locale directory with pathlib.Path
LOCALE_DIR = Path("locales")

# Initialize the Library with the Locale Directory and the Fallback Locale
translator = Translator(LOCALE_DIR, language="en", fallback_language="en")

# Gives the translation for the key 'hello_message' in the preferred language if available, else in the fallback language
translatium.translation('hello_message')
```

### Documentation

For more information, check out the Documentation.

## Roadmap

- [x] Switching to an Object Oriented Programming approach (Next Release)
- [ ] Add proper pluralization support
- [ ] Numeral Converter
- [ ] Date/Time Converter
- [x] Add Ruff linting
- [ ] Add uv Python Environment
- [ ] More to come...

## License

This project is licensed under the Apache-2.0 Software License - see the [LICENSE](LICENSE) file for details.
