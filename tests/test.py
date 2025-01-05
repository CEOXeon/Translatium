import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from translatium import translatium

# Get absolute path to locales directory
LOCALES_PATH = Path(__file__).resolve().parent / 'locales'



def change_translations_module_scope(monkeypatch, data: dict):
    monkeypatch.setattr(translatium, '_translations', data)



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
    assert translatium._config["language"] == 'de_DE'

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
