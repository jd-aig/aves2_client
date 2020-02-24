#!/usr/bin/env python


from setuptools import setup, find_packages
from aves2_client.version import aves2_version


setup(
    name='aves2',
    version=aves2_version(),
    description='Command Line Interface for Aves2',
    author='Yang Haibo',
    author_email='yanghaibo1@jd.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'simplejson',
        'requests>=2.1.8',
        'configobj>=5.0',
        'pyyaml>=3.12',
        'prettytable',
    ],
    # setup_requires = ['distribute>=0.6.21'],
    entry_points={'console_scripts': [
        'aves2=aves2_client.scripts._common:aves2_main',
    ]},
    data_files=[
        ('/etc/aves2/', ['aves2.cfg']),
    ],
)
