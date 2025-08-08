#!/usr/bin/env python
 
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import dirname, join

setup(
    name="mplus",
    version="0.0.1",
    description="https://www.mplusonline.com.my/macsecos/index.asp related function.",
    long_description=open(join(dirname(__file__), "README.md"), "r").read(),
    long_description_content_type="text/markdown",
    author="Chin Kim Keat",
    author_email="kim.keat.chin@outlook.com",
    maintainer="Chin Kim Keat",
    maintainer_email="kim.keat.chin@outlook.com",
    url="https://github.com/kimkeatc/MplusMalaccaSecurities",
    packages=find_packages(),
    classifiers=[
        # Specify the Development Status here.
        "Development Status :: 1 - Planning",
        # Specify the Operating System you support here.
        "Operating System :: OS Independent",
        # Specify the Python versions you support here.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        # Specify the Topic.
        "Topic :: Software Development",
    ],
    install_requires=[
        "bs4",
        "build",
        "pandas",
        "pytest",
        "requests",
        "selenium",
        "twine",
    ],
    python_requires=">=3.6",
)
