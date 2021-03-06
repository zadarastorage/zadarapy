# zadarapy

## THIS SOFTWARE IS PRE-ALPHA QUALITY - IT IS OFFERED WITHOUT WARRANTY OF FITNESS

## Introduction

zadarapy is Python module and command line utility that utilizes the [Zadara Storage](http://www.zadarastorage.com/) REST [API](http://vpsa-api.zadarastorage.com/).  This code is provided without warranty or guarantees of fitness.

## Installation

Either from your OS or inside a virtualenv/venv:

```pip install zadarapy```

## Usage

A utility called "zadarapy" should be put in your system path:

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

* You can define the API endpoint details through the zadarapy command directly.  Check zadarapy <command> <subcommand> --help for more information.  e.g. --api-host, --api-key, --api-port, and --insecure
* You can define the environment variables ZADARA_HOST, ZADARA_KEY, and ZADARA_PORT, ZADARA_SECURE (port and secure are optional)
* You can create a file called .zadarapy in your home directory, and in that file, under the DEFAULT heading, you can define the following:

```
[DEFAULT]
; Hostname or IP of VPSA - must be routable
host = xxx.zadaravpsa.com
; API key of calling user
key = xxx
; Port number of VPSA endpoint - optional
; Set to 80 by default if "secure" is False
; Set to 443 by default if "secure" is True
port = xxx
; Whether or not to use HTTPS - optional
; If True, use HTTPS (default)
; If False, use HTTP
secure = xxx
```
