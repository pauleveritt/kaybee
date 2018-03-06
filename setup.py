from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kaybee',
    version='0.1.10',
    description='Knowledgebase system for Sphinx',
    long_description=long_description,
    url='https://github.com/pauleveritt/kaybee',
    author='Paul Everitt',
    author_email='pauleveritt@me.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='sphinx blog website',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'sphinx',
        'dectate',
        'ruamel.yaml',
        'pydantic',
        'importscan',
        'pydash',
    ],
)
