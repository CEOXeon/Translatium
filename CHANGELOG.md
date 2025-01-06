# Changelog of Translatium

We use this file to document all notable changes for releases of Translatium.
This file may contain more detailed information about changes in the project than the release notes on GitHub.
We may change the format of this file at any time, but we will not update the release notes for older releases to match the new format.

## Format of the Changelog

Heading 2: Version Number
Release Name: "Name of the Release"
Release Date: DD.MM.YYYY
Content/Changes

## v0.0.2

Release Name: "Alpha"
Release Date: 06.01.2025

New Features:

* Support for nested translations (pluralization)
* Support for placeholders in translations
* Added a Simple Documentation

Changes:

* Introduced get_config() method to get the current configuration.
* Introduced set_config() method to set the configuration. Instead of set_language()
* Switched from os to pathlib
* Restructured the codebase
* Moved from Planning to Pre-Alpha

Breaking Changes:

* The method set_language() will be removed in v0.0.3. Use set_config() instead.

## v0.0.1

Release Name: "First Release"
Release Date: 31.12.2024

Translatium has now basic i18n functionality:

* Loading Language files (.yaml)
* Setting your preferred Language
* Setting up a Fallback Language
* Do simple checks on loaded Language Files
