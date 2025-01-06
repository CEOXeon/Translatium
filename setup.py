from pathlib import Path

import setuptools

VERSION = "0.0.2"  # PEP-440
NAME = "translatium"
DESCRIPTION = "A pure Python i18n library for your Python projects."
URL="https://github.com/CEOXeon/Translatium"
PROJECT_URLS = {
    "Source Code": "https://github.com/CEOXeon/Translatium",
}
AUTHOR = "Louis Zimmermann (@CEOXeon)"
AUTHOR_EMAIL = "louis-github@tutanota.com"
LICENSE = "Apache-2.0"
CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
]
INSTALL_REQUIRES = [
    "pyyaml",
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    project_urls=PROJECT_URLS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    #python_requires=">=3.8",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
)
