import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import translatium

# Get absolute path to locales directory
LOCALES_PATH = Path(__file__).resolve().parent / 'locales'



def change_translations_module_scope(monkeypatch, data: dict):
    monkeypatch.setattr(translatium.i18n.config, '_translations', data)



############################################################
#                      # ACTUAL TESTS                      #
############################################################

@pytest.mark.dependency()
def test_import():
    """Test that the module can be imported"""
    assert translatium is not None

@pytest.mark.dependency(depends=["test_import"])
def test_init():
    """Test initializing with locales path and fallback language"""
    translatium.init_translatium(LOCALES_PATH, 'en_US')
    
@pytest.mark.dependency(depends=["test_init"])
def test_set_language():
    """Test setting the active language"""
    translatium.set_config('language', 'de_DE')
    assert translatium.get_config()["language"] == 'de_DE'

@pytest.mark.dependency(depends=["test_set_language"])
def test_translations():
    """Test that translations work correctly"""
    # Initialize first
    translatium.init_translatium(LOCALES_PATH, 'en_US')
    translatium.set_config('language', 'de_DE')
    
    # Test German translation
    assert translatium.translation('hello_message', name="Louis") == 'Hallo Welt! Louis'
    
    # Test fallback to English
    translatium.set_config("language", 'invalid')
    assert translatium.translation('hello_message', name="Louis") == 'Hello World! Louis'

@pytest.mark.dependency(depends=["test_translations"])
def test_more_depth_in_translations(monkeypatch):
    translatium.init_translatium(LOCALES_PATH, 'en_US')
    translatium.set_config('language', 'de_DE')
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
    change_translations_module_scope(monkeypatch, data)
    assert translatium.translation('mail.one') == 'Sie haben eine neue E-Mail'
    assert translatium.translation('mail.many') == 'Sie haben viele neue E-Mails'
    translatium.set_config("language", 'invalid')
    assert translatium.translation('mail.one') == 'You have one new mail'
    assert translatium.translation('mail.many') == 'You have many new mails'

@pytest.mark.dependency(depends=["test_more_depth_in_translations"])
def test_pluralize(monkeypatch):
    translatium.init_translatium(LOCALES_PATH, 'en_US')
    translatium.set_config('language', 'de_DE')
    translatium.set_config('fallback_language', 'de_DE')
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
    change_translations_module_scope(monkeypatch, data)
    assert translatium.pluralize('mail', 1) == 'Sie haben eine neue E-Mail'
    assert translatium.pluralize('mail', 2) == 'Sie haben viele neue E-Mails'
    assert translatium.pluralize('mail', 3) == 'Sie haben viele neue E-Mails'
    assert translatium.pluralize('mail', 0) == 'Sie haben keine E-Mails'
    assert translatium.pluralize('mail', -1) == "Sie haben neue E-Mails"
    translatium.set_config("language", 'en_US')
    assert translatium.pluralize('mail', 1) == 'You have one new mail'
    assert translatium.pluralize('mail', 2) == 'You have many new mails'
    assert translatium.pluralize('mail', 3) == 'You have many new mails'
    assert translatium.pluralize('mail', 0) == 'You have no new mails'
    assert translatium.pluralize('mail', -1) == "You have new mails"



############################################################
#                 # DO NOT DELETE THIS TEST                #
############################################################

EASTER_EGGS_PATH = Path(__file__).resolve().parent.parent / "easter_eggs.hidden"
if EASTER_EGGS_PATH.exists():
    def test_stupid_easter_eggs():
        import antigravity
        antigravity.fly()
