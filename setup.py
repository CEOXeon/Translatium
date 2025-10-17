from pathlib import Path

import setuptools
import subprocess

class CleanCommand(setuptools.Command):
    description = "Clean up the files using .gitignore"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.run(["git", "clean", "-Xdf"])

class TestCommand(setuptools.Command):
    description = "Run the tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.run(["pytest"])

class InstallDevCommand(setuptools.Command):
    description = "Install the development dependencies"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.run(["pip", "install", "typeguard", "pyyaml", "pytest", "pytest-cov", "pytest-dependency"])

class InstallProdCommand(setuptools.Command):
    description = "Install the production dependencies"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.run(["pip", "install", "typeguard", "pyyaml"])


setuptools.setup(
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",

    # Add custom commands
    cmdclass={'clean_dev': CleanCommand,
            'test': TestCommand,
            'install_dev': InstallDevCommand,
            'install_prod': InstallProdCommand},
)
