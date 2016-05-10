from setuptools import (
    setup,
    find_packages
)

from gopy import __version__

with open('README.rst', 'r') as f:
    long_description = f

setup(
    name="gopy",
    version=__version__,
    author="importcjj",
    author_email="importcjj@gmail.com",
    description="Mock some golang Syntactic sugar in python",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
)
