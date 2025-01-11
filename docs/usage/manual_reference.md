# Library Endpoints

[TOC]

## Endpoints

### init_translatium(path: Path, fallback: str) -> None

Initializes the Library and set basic configurations.

It takes two arguments:

* path: Which is the path to the locale directory. Its type is Path from the pathlib module.
* fallback: Which is the fallback language. Its type is str.

### set_config(config_key: str, config_value: str) -> None

With that function, you can some of the configurations in the library.

It takes two arguments:

* config_key: Which is the key of the configuration. Its type is str.
* config_value: Which is the value your setting of this configuration. Its type is str.

Following Settings are of significant interest:

* language: Which is the language you want to use. Its type is str.
* fallback_language: Which is the fallback language. Its type is str.

### get_config() -> dict

You can use this to get all the configurations in the library as a dictionary. Its return type is dict.

### translation(translation_key: str, **kwargs) -> str

This the most important function in the library. You will use this function the most. It is to get the translation of a specific translation_key.

It takes two arguments:

* translation_key: Which is the key of the translation you want to get. You can use dots to have nested translations therefore supporting partially pluralization. Its type is str.
* **kwargs: Which are the arguments you want to pass to the translation. Note thatthe variable names should be the same as the placeholders in the translation.

## Basic Example

```python
import translatium # import the library
from pathlib import Path # import the Path class from the pathlib module

translatium.init_translatium(Path("path/to/locales"), "en") # initializes the library with the path to the locales and the fallback language "en"
translatium.set_config("language", "de") # sets the language to "de"

translatium.translation("hello_world") # returns "Hallo Welt" or "Hello World" if not found in "de"
```
