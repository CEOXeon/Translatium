import yaml
from pathlib import Path


class TranslationError(Exception):
    def __init__(self, message, value=""):
        self.message = message
        self.value = value
        super().__init__(self.message)
    def __str__(self):
        return f'{self.message} -> {self.value}'


# Global variables to store translations and fallback language
_translations = {}
_fallback_language = None
_language = None

def init_translatium(path: Path, fallback: str) -> None:
    '''
    Initialize translatium. It does automatically load the translations and checks for errors.

    Parameters:
    - path: Path to the directory containing the translation files
    - fallback: The fallback language to use when a translation is not found in the selected language

    Returns: None
    '''
    global _translations, _fallback_language, _language
    _translations = load_translations(path)
    _fallback_language = fallback
    checks()
    return None

def checks() -> None:
    '''
    Check if the translations are valid and if the fallback language is available.

    Returns: None
    '''
    global _translations, _fallback_language
    # Check if fallback language is available
    def check_fallback_language():
        if _fallback_language not in _translations:
            raise TranslationError("Fallback Language not found", _fallback_language)
    # Check if all keys in the languages (except the fallback language) are present in the fallback language
    def check_translation_keys():
        fallback_keys = set(_translations[_fallback_language].keys())
        for lang, translations in _translations.items():
            if lang == _fallback_language:
                continue
            missing_keys = set(translations.keys()) - fallback_keys
            if missing_keys:
                raise TranslationError(
                    f"Translation keys {missing_keys} in language '{lang}' not found in fallback language",
                    missing_keys)
    check_fallback_language()
    check_translation_keys()
    return None

def set_language(language: str) -> None:
    '''
    Sets the preferred language for translations.
    If the language is not available, an error is raised.
    If the language is set to "invalid", the laguage is changed to the string invalid. This doen for testing purposes.

    Parameters:
    - language: The language code to set as the preferred language

    Returns: None
    '''
    global _translations, _language
    # Check if the language is available
    if language == "invalid":
        _language = language
    elif language not in _translations:
        raise TranslationError("Language not found", language)
    else:
        _language = language
    return None

def translation(translation_key: str) -> str:
    '''
    Gets the translation for a specific key in the selected language.
    If the translation is not found in the selected language, the fallback language is used.

    Parameters:
    - translation_key: The key for the translation

    Returns: A string with the translation
    '''
    global _translations, _language, _fallback_language
    # Helper function to get translation from a specific language
    def get_translation(language):
        return _translations.get(language, {}).get(translation_key)
    translation = get_translation(_language) or get_translation(_fallback_language)
    if translation:
        return translation
    else:
        raise TranslationError(
            f"Translation key '{translation_key}' not found in selected language '{_language}' or fallback language '{_fallback_language}'", translation_key)

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
