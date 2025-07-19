import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from translatium import Translator

# Get absolute path to locales directory
LOCALES_PATH = Path(__file__).resolve().parent / 'locales'


def change_translations_module_scope(monkeypatch, translator, data: dict):
    monkeypatch.setattr(translator, 'translations', data) # type: ignore


def test_import():
    """Test that the module can be imported"""
    assert Translator is not None

def test_init():
    """Test initializing with locales path and fallback language"""
    translator = Translator(LOCALES_PATH, 'de_DE', "en_US")
    assert translator is not None

def test_set_language():
    """Test setting the active language"""
    translator = Translator(LOCALES_PATH, 'de_DE', "en_US")
    translator.set_language('de_DE')
    assert translator.get_language() == 'de_DE'

def test_simple_translation(monkeypatch):
    """Test that simple translations work correctly"""
    translator = Translator(LOCALES_PATH, 'de_DE', "en_US")
    data= {
        "en_US": {
            "hello_message": "Hello World! {name}"
        },
        "de_DE": {
            "hello_message": "Hallo Welt! {name}"
        }
    }
    change_translations_module_scope(monkeypatch, translator, data)
    assert translator.translate('hello_message', name="Louis") == 'Hallo Welt! Louis'

def test_complex_translation(monkeypatch):
    """Test that complex translations with nested keys work correctly"""
    translator = Translator(LOCALES_PATH, 'de_DE', "en_US")
    data= {
        "en_US": {
            "mail": {
                "one": "You have one new mail",
                "many": "You have many new mails"
            }
        },
        "de_DE": {
            "mail": {
                "one": "Sie haben eine neue E-Mail",
                "many": "Sie haben viele neue E-Mails"
            }
        }
    }
    change_translations_module_scope(monkeypatch, translator, data)
    assert translator.translate('mail.one') == 'Sie haben eine neue E-Mail'
    assert translator.translate('mail.many') == 'Sie haben viele neue E-Mails'

def test_pluralize_translation(monkeypatch):
    """Test that pluralization works correctly"""
    translator = Translator(LOCALES_PATH, 'de_DE', "en_US")
    data= {
        "en_US": {
            "mail": {
                "default": "You have new mails",
                "one": "You have one new mail",
                "many": "You have many new mails",
                "none": "You have no new mails"
            }
        },
        "de_DE": {
            "mail": {
                "default": "Sie haben neue E-Mails",
                "one": "Sie haben eine neue E-Mail",
                "many": "Sie haben viele neue E-Mails",
                "none": "Sie haben keine E-Mails"
            }
        }
    }
    change_translations_module_scope(monkeypatch, translator, data)
    assert translator.pluralize('mail', 1) == 'Sie haben eine neue E-Mail'
    assert translator.pluralize('mail', 2) == 'Sie haben viele neue E-Mails'
    assert translator.pluralize('mail', 3) == 'Sie haben viele neue E-Mails'
    assert translator.pluralize('mail', 0) == 'Sie haben keine E-Mails'
    assert translator.pluralize('mail', -1) == "Sie haben neue E-Mails"
    translator.set_language('en_US')
    assert translator.pluralize('mail', 1) == 'You have one new mail'
    assert translator.pluralize('mail', 2) == 'You have many new mails'
    assert translator.pluralize('mail', 3) == 'You have many new mails'
    assert translator.pluralize('mail', 0) == 'You have no new mails'
    assert translator.pluralize('mail', -1) == "You have new mails"

def test_fallback_translation(monkeypatch):
    """Test that fallback translations work correctly"""
    translator = Translator(LOCALES_PATH, 'de_DE', "en_US")
    data= {
        "en_US": {
            "hello_message": "Hello World! {name}"
        },
        "de_DE": {
            
        }
    }
    change_translations_module_scope(monkeypatch, translator, data)
    assert translator.translate('hello_message', name="Louis") == 'Hello World! Louis'
