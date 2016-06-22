# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import os
import re

from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def requirements(file_name='requirements.txt'):
    return [
        str(ir.req)
        for ir in parse_requirements(file_name, session=PipSession())
        if ir.match_markers()
    ]


def extra_requirements():
    try:
        join = os.path.join
        path = join('requirements', 'extra')
        return {
            str(file_name.rsplit('.', 1)[0]): requirements(join(path, file_name))
            for file_name in os.listdir(path)
            if file_name.endswith('.txt')
        }
    except OSError:
        return None

setup(
    name='django-rest-framework-queryset',
    version=find_version('__init__.py'),
    author='James Lin',
    author_email='james@lin.net.nz',
    long_description=read('README.md'),
    install_requires=requirements(),
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Framework :: Django",
    ],
    extras_require=extra_requirements(),
)
