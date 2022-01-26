from pathlib import Path
from typing import List, Union

from setuptools import setup


def get_requirements(path: Union[str, Path]) -> List[str]:
    with open(Path(__file__).parent / path, encoding="utf8") as file:
        content = file.readlines()
    return content


setup(install_requires=get_requirements("requirements.txt"))
