import os
from setuptools import setup, find_packages

ROOT = os.path.abspath(os.path.dirname(__file__))

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open("requirements.txt", "r") as fh:
    require = fh.readlines()
require= [x.strip() for x in require]

setup(
    name='django-zxcvbn-password-validator',
    version='1.1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=require,
    license='MIT License',
    description='A password validator for django, based on zxcvbn-python.',
    long_description=open(os.path.join(ROOT, 'README.md')).read(),
    url='https://github.com/Pierre-Sassoulas/django-zxcvbn-password-validator',
    author='Pierre Sassoulas',
    author_email='pierre.sassoulas@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
)
