import yaml
from pathlib import Path
import warnings
import functools


def deprecated(message, version):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated and will be removed in {version}. {message}",
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator


class TranslationError(Exception):
    def __init__(self, message, value=""):
        self.message = message
        self.value = value
        super().__init__(self.message)
    def __str__(self):
        return f'{self.message} -> {self.value}'


# Global variables to store translations and fallback language
_translations = {}
_config = {
    "silent_kwargs": False,
    "language": "",
    "fallback_language": "",
}

def init_translatium(path: Path, fallback: str) -> None:
    '''
    Initialize translatium. It does automatically load the translations and checks for errors.

    Parameters:
    - path: Path to the directory containing the translation files
    - fallback: The fallback language to use when a translation is not found in the selected language

    Returns: None
    '''
    global _translations, _config
    _translations = load_translations(path)
    _config["fallback_language"] = fallback
    checks()
    return None

def checks() -> None:
    '''
    Check if the translations are valid and if the fallback language is available.

    Returns: None
    '''
    global _translations, _config
    # Check if fallback language is available
    def check_fallback_language():
        if _config["fallback_language"] not in _translations:
            raise TranslationError("Fallback Language not found", _config["fallback_language"])
    # Check if all keys in the languages (except the fallback language) are present in the fallback language
    def check_translation_keys():
        fallback_keys = set(_translations[_config["fallback_language"]].keys())
        for lang, translations in _translations.items():
            if lang == _config["fallback_language"]:
                continue
            missing_keys = set(translations.keys()) - fallback_keys
            if missing_keys:
                raise TranslationError(
                    f"Translation keys {missing_keys} in language '{lang}' not found in fallback language",
                    missing_keys)
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
    global _translations, _config
    # Check if the language is available
    if language == "invalid":
        _config["language"] = language
    elif language not in _translations:
        raise TranslationError("Language not found", language)
    else:
        _config["language"] = language
    return None

def translation(translation_key: str, **kwargs) -> str:
    '''
    Gets the translation for a specific key in the selected language.
    If the translation is not found in the selected language, the fallback language is used.

    Parameters:
    - translation_key: The key for the translation

    Returns: A string with the translation
    '''
    global _translations, _config
    # Helper function to get translation from a specific language
    def get_translation(language, keys):
        translation = _translations.get(language, {})
        for key in keys:
            if isinstance(translation, dict):
                translation = translation.get(key)
            else:
                return None
        return translation
    keys = translation_key.split('.')
    translation = get_translation(_config["language"], keys) or get_translation(_config["fallback_language"], keys)
    if translation:
        return translation.format(**kwargs)
    else:
        raise TranslationError(
            f"Translation key '{translation_key}' not found in selected language '{_config["language"]}' or fallback language '{_config["fallback_language"]}'", translation_key)

def load_translations(path: Path) -> dict:
    '''
    Loads translations from the specified directory.

    Parameters:
    - path: Path to the directory containing the translation files

    Returns: A dictionary with the translations
    '''
    translations = {}
    for file in path.glob('*.yaml'):
        lang_code = file.stem  # Extract the language code from the filename
        with file.open('r') as f:
            translations[lang_code] = yaml.safe_load(f)
    for file in path.glob('*.yml'):
        lang_code = file.stem  # Extract the language code from the filename
        with file.open('r') as f:
            translations[lang_code] = yaml.safe_load(f)
    return translations

def set_config(config_key: str, value: str) -> None:
    '''
    Gives write access to the configuration of translatium.

    Parameters:
    - config_key: The key of the configuration to change
    - value: The value to set

    Returns: None
    '''
    global _config
    _config[config_key] = value
    return None

def get_config() -> dict:
    '''
    Gives read access to the configuration of translatium.

    Returns: A dictionary with the configuration
    '''
    global _config
    return _config
