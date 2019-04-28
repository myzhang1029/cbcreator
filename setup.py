#!/usr/bin/env python
# setup.py - easy_install script for cbcreator
#
# Copyright 2018 Zhang Maiyun
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

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
try:
    import py2exe
except:
    pass

setup(
    name="cbcreator",
    description="Automatic class band creator",
    version="1.0",
    url="https://github.com/myzhang1029/cbcreator",
    download_url="https://github.com/myzhang1029/cbcreator",
    author="Zhang Maiyun",
    author_email="myzhang1029@hotmail.com",
    packages=["cbcreator"],
    package_data={"cbcreator": ["resources/fonts/*.*"]},
    install_requires=["pillow"],
    scripts=[],
    entry_points={
        "console_scripts": [
            "cbCreator = cbcreator.cbCreator:start"
        ]
    }
)
