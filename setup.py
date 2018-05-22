from setuptools import setup, find_packages
from zadarapy import __version__

setup(
    name='zadarapy',
    version=__version__,
    packages=find_packages(),
    install_requires=['configparser>=3.5.0', 'future>=0.15.2',
                      'terminaltables>=2.1.0'],
    url='https://github.com/zadarastorage/zadarapy',
    license='Apache License 2.0',
    author='Jeremy Brown',
    author_email='jeremy@zadarastorage.com',
    description='Python module and command line interface with Zadara REST '
                'APIs',
    entry_points={
        'console_scripts': ['zadarapy=zadarapy.bin.command_line:main'],
    },
    zip_safe=False,
)
