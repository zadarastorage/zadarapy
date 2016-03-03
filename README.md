# zadarapy

## Introduction

zadarapy is Python module and command line utility that utilizes the [Zadara Storage](http://www.zadarastorage.com/) REST [API](http://vpsa-api.zadarastorage.com/).

## Usage

The eventual goal will be to publish this module as installable by pip, and everything will be seemless (e.g. pip install zadarapy).  But that will wait until the full module has testing.

For now, this module only supports Python 3.  Work is being done to make it work with Python 2.

For now, to try this module/script out, you can do:

```
cd /path/to/where/you/want/code
git clone git@github.com:zadarastorage/zadarapy.git
cd /usr/local/lib/python3.5/site-packages # or wherever your Python 3 include path is
sudo ln -s /path/to/zadarapy/zadarapy
cd /usr/local/bin
ln -s /path/to/zadarapy/bin/zadarapy
```

Now that the zadarapy module is in the global include path, you should be able to run it directly:

```
zadarapy --help
```

Every section of the API has a "subcommand" - so for example, to see all commands related to pools:

```
zadarapy pools --help
```

The rest of the command should hopefully be self explanatory - please report any bugs.

## API Settings

You need to tell the script how to reach the API server.  There are a few different ways to do this:

* You can define the API endpoint details through the zadarapy command directly.  Check zadarapy <command> <subcommand> --help for more information.  e.g. --api-host, --api-key, and --api-port
* You can define the environment variables ZADARA_HOST, ZADARA_KEY, and ZADARA_PORT (port is optional)
* You can create a file called .zadarapy in your home directory, and in that file, under the DEFAULT heading, you can define the following:

```
[DEFAULT]
host = xxx.zadaravpsa.com
key = xxx
```
