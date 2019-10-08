#!/usr/bin/python3

# Copyright 2015-2017 IONOS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Setup script for the IONOS Enterprise API Python client.

"""
from __future__ import print_function

import codecs
import os
import re
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r', 'utf-8').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


if os.path.isfile("README.md"):
    long_desc = read('README.md')
else:
    long_desc = "Ionos Enterprise API Client Library for Python"


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True  # pylint: disable=attribute-defined-outside-init

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='ionosenterprise',
    version=find_version('ionosenterprise', '__init__.py'),
    description='IonosEnterprise API Client Library for Python',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Ionos Enterprise',
    author_email='sdk@cloud.ionos.com',
    url='https://github.com/ionos-enterprise/ionos-enterprise-sdk-python',
    install_requires=['requests>=2.0.0', 'six>=1.10.0', 'appdirs>=1.4.3'],
    # include_package_data=True,
    packages=['ionosenterprise', 'ionosenterprise.requests', 'ionosenterprise.items'],
    platforms='any',
    test_suite='ionosenterprise.test.test_ionosenterprise',
    cmdclass={'test': PyTest},
    tests_require=['pytest'],
    license='Apache 2.0',
    keywords='ionos enterprise api client cloud',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Natural Language :: English',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Operating System :: POSIX',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Software Development :: Libraries :: Application Frameworks',
                 'Topic :: Internet :: WWW/HTTP'],
    extras_require={
        'testing': ['pytest'],
    }
)
