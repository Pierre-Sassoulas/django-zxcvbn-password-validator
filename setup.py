import os
from setuptools import setup, find_packages

ROOT = os.path.abspath(os.path.dirname(__file__))

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-zxcvbn-password-validator',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django', 'zxcvbn-python'],
    license='MIT License',
    description='This is a custom password validator based on zxcvbn-python for easy use in Django projects.',
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
        'Programming Language :: Python :: 3',
    ],
)
