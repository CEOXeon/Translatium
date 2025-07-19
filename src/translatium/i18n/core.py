from pathlib import Path

from typeguard import typechecked
import yaml
import json

from ..helpers.errors import TranslationError
from ..helpers.utils import TranslationsType

@typechecked
class Translator():
    def __init__(self, path: Path = Path(), language: str = "", fallback_language: str = "") -> None:
        self.path: Path = path
        self.language: str = language
        self.fallback_language: str = fallback_language
        self.translations: TranslationsType = {}
        self.load_translations()
        return None

    def __repr__(self):
        return f"Translator(path={self.path}, language={self.language}, fallback_language={self.fallback_language}, translations={self.translations})"

    def __str__(self):
        return self.__repr__()

############################################################
#                   # GETTERS AND SETTERS                  #
############################################################
    def set_language(self, language: str) -> None:
        if language not in self.translations:
            raise TranslationError("Language not found", language)
        self.language = language
        return None

    def set_fallback_language(self, fallback_language: str) -> None:
        if fallback_language not in self.translations and fallback_language != self.language:
            raise TranslationError("Fallback Language not found", fallback_language)
        self.fallback_language = fallback_language
        return None

    def set_path(self, path: Path) -> None:
        if not path.exists():
            raise TranslationError("Path does not exist", path)
        if not path.is_dir():
            raise TranslationError("Path is not a directory", path)
        self.path = path
        return None

    def get_language(self) -> str:
        return self.language

    def get_fallback_language(self) -> str:
        return self.fallback_language

    def get_path(self) -> Path:
        return self.path

############################################################
#                         # FILE IO                        #
############################################################
    def load_translations(self) -> None:
        self.translations = {}
        ## YAML Support
        for file in self.path.glob('*.yaml'):
            lang_code = file.stem  # Extract the language code from the filename
            with file.open('r') as f:
                self.translations[lang_code] = yaml.safe_load(f)
        for file in self.path.glob('*.yml'):
            lang_code = file.stem  # Extract the language code from the filename
            with file.open('r') as f:
                self.translations[lang_code] = yaml.safe_load(f)
        ## JSON Support
        for file in self.path.glob('*.json'):
            lang_code = file.stem  # Extract the language code from the filename
            with file.open('r') as f:
                self.translations[lang_code] = json.load(f)
        return None


############################################################
#                       # TRANSLATION                      #
############################################################

    def translate(self, translation_key: str, **kwargs) -> str:
        # Helper function to get translation from a specific language
        def get_translation(language, keys):
            translation = self.translations.get(language, {})
            for key in keys:
                if isinstance(translation, dict):
                    translation = translation.get(key)
                else:
                    return None
            return translation
        keys = translation_key.split('.')
        translation = get_translation(self.language, keys) or get_translation(self.fallback_language, keys)
        if translation:
            return translation.format(**kwargs)
        else:
            raise TranslationError(
                f"Translation key '{translation_key}' not found in selected language '{self.language}' or fallback language '{self.fallback_language}'", translation_key)

    def pluralize(self, translation_key: str, count: int) -> str:
        # Helper function to get translation from a specific language
        def get_translation(language, keys):
            translation = self.translations.get(language, {})
            for key in keys:
                if isinstance(translation, dict):
                    translation = translation.get(key)
                else:
                    return None
            return translation
        keys = translation_key.split('.')
        translation = get_translation(self.language, keys) or get_translation(self.fallback_language, keys)
        if translation:
            if count == 1:
                return translation.get('one')
            elif count > 1:
                return translation.get('many')
            elif count == 0:
                return translation.get('none')
            else:
                return translation.get('default')
        else:
            raise TranslationError(
                f"Translation key '{translation_key}' not found in selected language '{self.language}' or fallback language '{self.fallback_language}'", translation_key)
