# coding: utf-8
import sys

from setuptools import setup, find_packages

install_requires = [
    'jinja2',
    'aiohttp',
    'aiohttp_jinja2',
]

if sys.version_info < (2, 7):
    install_requires.append('importlib')
    install_requires.append('logutils')
    install_requires.append('ordereddict')

with open('README.md') as f:
    long_description = f.read()

setup(
    name='trunklucator',
    python_requires='>3.6.0',
    version='1.1.3',
    url='https://github.com/Dumbris/trunklucator',
    license='Apache License 2.0',
    description=('Easy plugable UI for your experiments with data and machine learning'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
    },
    zip_safe=False,
    platforms='any',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ),
    test_suite='tests',
)
