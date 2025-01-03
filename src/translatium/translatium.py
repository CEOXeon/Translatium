import yaml
import os


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

def init_translatium(path, fallback):
    global _translations, _fallback_language, _language
    _translations = load_translations(path)
    _fallback_language = fallback
    checks()

def checks():
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

def set_language(language):
    global _translations, _language
    # Check if the language is available
    if language == "invalid":
        _language = language
    elif language not in _translations:
        raise TranslationError("Language not found", language)
    else:
        _language = language

def translation(translation_key):
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

def load_translations(path):
    translations = {}
    for filename in os.listdir(path):
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            lang_code = filename.split('.')[0]  # Extract the language code from the filename
            with open(os.path.join(path, filename), 'r') as file:
                translations[lang_code] = yaml.safe_load(file)
    return translations
