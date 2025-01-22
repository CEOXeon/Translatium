from pathlib import Path

from typeguard import typechecked

from .config import get_config, get_translations, set_config, set_translations
from ..helpers.errors import TranslationError
from ..helpers.utils import deprecated
from ..helpers.file_io import load_translations


@typechecked
def init_translatium(path: Path, fallback: str) -> None:
    '''
    Initialize translatium. It does automatically load the translations and checks for errors.

    Parameters:
    - path: Path to the directory containing the translation files
    - fallback: The fallback language to use when a translation is not found in the selected language

    Returns: None
    '''
    set_translations(load_translations(path))
    set_config("fallback_language", fallback)
    checks()
    return None

@typechecked
def checks() -> None:
    '''
    Check if the translations are valid and if the fallback language is available.

    Returns: None
    '''
    # Check if fallback language is available
    def check_fallback_language():
        if get_config()["fallback_language"] not in get_translations():
            raise TranslationError("Fallback Language not found", get_config()["fallback_language"])
    # Check if all keys in the languages (except the fallback language) are present in the fallback language
    def check_translation_keys():
        fallback_keys = set(get_translations()[get_config()["fallback_language"]].keys())
        for lang, translations in get_translations().items():
            if lang == get_config()["fallback_language"]:
                continue
            missing_keys = set(translations.keys()) - fallback_keys
            if missing_keys:
                raise TranslationError(f"Translation keys {missing_keys} in language '{lang}' not found in fallback language", missing_keys)
    check_fallback_language()
    check_translation_keys()
    return None

@deprecated("Use set_config instead", "v0.3.0")
@typechecked
def set_language(language: str) -> None:
    '''
    Sets the preferred language for translations.
    If the language is not available, an error is raised.
    If the language is set to "invalid", the laguage is changed to the string invalid. This doen for testing purposes.

    Parameters:
    - language: The language code to set as the preferred language

    Returns: None
    '''
    # Check if the language is available
    if language == "invalid":
        set_config("language", language)
    elif language not in get_translations():
        raise TranslationError("Language not found", language)
    else:
        set_config("language", language)
    return None
