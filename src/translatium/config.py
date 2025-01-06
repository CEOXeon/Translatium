

# Global variables to store translations and fallback language
_translations = {}
_config = {
    "silent_kwargs": False,
    "language": "",
    "fallback_language": "",
}


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

def set_translations(translations: dict) -> None:
    '''
    Sets the translations for translatium.

    Parameters:
    - translations: A dictionary with the translations

    Returns: None
    '''
    global _translations
    _translations = translations
    return None

def get_translations() -> dict:
    '''
    Gets the translations for translatium.

    Returns: A dictionary with the translations
    '''
    global _translations
    return _translations
