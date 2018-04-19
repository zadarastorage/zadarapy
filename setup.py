from setuptools import setup, find_packages

setup(
    name='zadarapy',
    version='0.1',
    packages=find_packages(),
    install_requires=['configparser>=3.5.0', 'future>=0.15.2',
                      'ipaddress>=1.0.17', 'terminaltables>=2.1.0'],
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
