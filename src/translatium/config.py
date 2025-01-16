from typeguard import typechecked

from .utils import ConfigType, TranslationsType

# Global variables to store translations and fallback language
_translations: TranslationsType = {}
_config: ConfigType = {
    "silent_kwargs": False,
    "language": "",
    "fallback_language": "",
}


@typechecked
def set_config(config_key: str, value: str) -> None: # FIXME: Value should be Union[str, bool, int]
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

@typechecked
def get_config() -> ConfigType:
    '''
    Gives read access to the configuration of translatium.

    Returns: A dictionary with the configuration
    '''
    global _config
    return _config

@typechecked
def set_translations(translations: TranslationsType) -> None:
    '''
    Sets the translations for translatium.

    Parameters:
    - translations: A dictionary with the translations

    Returns: None
    '''
    global _translations
    _translations = translations
    return None

@typechecked
def get_translations() -> TranslationsType:
    '''
    Gets the translations for translatium.

    Returns: A dictionary with the translations
    '''
    global _translations
    return _translations
