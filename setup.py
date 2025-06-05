from setuptools import setup
from pathlib import Path

requirements = Path("src/whitepyges/requirements.txt").read_text().splitlines()

setup(install_requires=requirements)