import yaml
import json
from pathlib import Path
from .errors import TranslationError
from .config import set_translations, get_translations, set_config, get_config
from .utils import deprecated

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

def translation(translation_key: str, **kwargs) -> str:
    '''
    Gets the translation for a specific key in the selected language.
    If the translation is not found in the selected language, the fallback language is used.

    Parameters:
    - translation_key: The key for the translation

    Returns: A string with the translation
    '''
    # Helper function to get translation from a specific language
    def get_translation(language, keys):
        translation = get_translations().get(language, {})
        for key in keys:
            if isinstance(translation, dict):
                translation = translation.get(key)
            else:
                return None
        return translation
    keys = translation_key.split('.')
    translation = get_translation(get_config()["language"], keys) or get_translation(get_config()["fallback_language"], keys)
    if translation:
        return translation.format(**kwargs)
    else:
        raise TranslationError(
            f"Translation key '{translation_key}' not found in selected language '{get_config()["language"]}' or fallback language '{get_config()["fallback_language"]}'", translation_key)

def load_translations(path: Path) -> dict:
    '''
    Loads translations from the specified directory.

    Parameters:
    - path: Path to the directory containing the translation files

    Returns: A dictionary with the translations
    '''
    translations = {}
    ## YAML Support
    for file in path.glob('*.yaml'):
        lang_code = file.stem  # Extract the language code from the filename
        with file.open('r') as f:
            translations[lang_code] = yaml.safe_load(f)
    for file in path.glob('*.yml'):
        lang_code = file.stem  # Extract the language code from the filename
        with file.open('r') as f:
            translations[lang_code] = yaml.safe_load(f)
    ## JSON Support
    for file in path.glob('*.json'):
        lang_code = file.stem  # Extract the language code from the filename
        with file.open('r') as f:
            translations[lang_code] = json.load(f)
    return translations
