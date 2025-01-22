from .config import get_config, get_translations
from ..helpers.errors import TranslationError
from typeguard import typechecked


@typechecked
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
