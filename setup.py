"""
Setup script for VictorUno package.
This file provides backward compatibility for systems that require setup.py.
For modern packaging, prefer pyproject.toml.
"""

from setuptools import setup, find_packages

# Read the contents of README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="victoruno",
    version="0.1.0",
    author="Cole Barbes",
    author_email="your.email@example.com",
    description="Personalized Agent to Research, Develop, and Optimize",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cbarbes1/VictorUno",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "victoruno=victoruno.cli:main",
        ],
    },
)