# Library Endpoints

## translatium.init_translatium(path: Path, fallback_language: str) -> None

This function initializes the library with the path to the directory containing the language files and the fallback language.
The language files should be in the format `language_code.yaml`. The fallback language is used when the requested translation key is not available in the preferred language.

## translatium.set_language(language: str) -> None

This function sets the preferred language for the library. The preferred language is used to fetch the translations.

## translatium.translation(key: str) -> str

This function returns the translation for the given key in the preferred language. If the translation is not available in the preferred language, it falls back to the fallback language.
