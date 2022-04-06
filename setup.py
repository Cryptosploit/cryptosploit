from pathlib import Path
from pkg_resources import parse_requirements
from setuptools import setup
from os import walk, path


install_requires = []
path_list = [path.join(root, filename) for root, _, filenames in walk('.')
             for filename in filenames if filename == "requirements.txt"]

for path_to_file in path_list:
    with Path(path_to_file).open() as requirements_txt:
        install_requires.extend(str(requirement) for requirement in parse_requirements(requirements_txt))

setup(
    install_requires=install_requires,
)
