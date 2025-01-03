import sys
import os
import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from translatium import translatium

# Get absolute path to locales directory
LOCALES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'locales'))



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
    translatium.set_language('de_DE')
    assert translatium._language == 'de_DE'

@pytest.mark.dependency(depends=["test_set_language"])
def test_translations():
    """Test that translations work correctly"""
    # Initialize first
    translatium.init_translatium(LOCALES_PATH, 'en_US')
    translatium.set_language('de_DE')
    
    # Test German translation
    assert translatium.translation('hello_message') == 'Hallo Welt!'
    
    # Test fallback to English
    translatium.set_language('invalid')
    assert translatium.translation('hello_message') == 'Hello World! %{name}'
