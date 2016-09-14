# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='emotrix',
    version='0.0.1',
    description='BCI api for handling human emotions',
    long_description=readme,
    author='Henzer G., César L., Freddy M., Matías V., Pablo S. and Jackeline G.',
    author_email='',
    url='https://github.com/henzer/EMOTRIX',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
