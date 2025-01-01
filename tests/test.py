import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from translatium import translatium

# Use an absolute path for the locales directory
locales_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'locales'))
translatium.init_translatium(locales_path, 'en_US')
translatium.set_language('de_DE')

print(translatium.translation('hello_message'))
