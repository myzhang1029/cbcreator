#!/use/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
        description = "Automatic class band creator",
        author = "Zhang Maiyun",
        url = "https://github.com/myzhang1029/cbcreator",
        download_url = "https://github.com/myzhang1029/cbcreator",
        author_email = "myzhang1029@hotmail.com",
        version = "0.1",
        install_requires = ["pillow"],
        packages = ["cbcreator"],
        scripts = [],
        name = "cbcreator",
        entry_points = {
            "console_scripts": [
                "cbCreator = cbcreator.cbCreator:start"
            ]
        }
)
