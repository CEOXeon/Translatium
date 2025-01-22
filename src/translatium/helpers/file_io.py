import json
from pathlib import Path
import yaml
from typeguard import typechecked
from .utils import TranslationsType

@typechecked
def load_translations(path: Path) -> TranslationsType:
    '''
    Loads translations from the specified directory.

    Parameters:
    - path: Path to the directory containing the translation files

    Returns: A dictionary with the translations
    '''
    translations: TranslationsType = {}
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
