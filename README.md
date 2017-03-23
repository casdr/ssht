# ssht
SSH client wrapper for easily connecting to hosts

[![Build Status](https://travis-ci.org/hkraal/ssht.svg?branch=master)](https://travis-ci.org/hkraal/ssht)
[![Coverage Status](https://coveralls.io/repos/github/hkraal/ssht/badge.svg?branch=master)](https://coveralls.io/github/hkraal/ssht?branch=master)


This wrapper for the well known `ssh` client makes it possible to connect to the right server with just typing a part of the host name. The external sources are queried using the search term and those matching the string will be presented as an option.

Current supported sources:

* JSON file
* MySQL database

# Installation

Install ssht using pip:

    pip install ssht

or if you want the latest version:

    pip install https://github.com/hkraal/ssht/archive/master.zip

Create ssht folder in home directory

    mkdir ~/.ssht

Configure sources in ~/.ssht:

**Define servers in JSON format**:

    {
    	"hosts": [
    	  {
    		"port": "2222",
    		"hostname": "host01.example.com",
    		"ipv4": "192.168.0.1",
    		"user": "root"
    	  },
    	  {
    		"port": "2222",
    		"hostname": "host02.example.org",
    		"ipv4": "192.168.0.2",
    	  }
    	]
    }

**Define servers in MySQL**:

    {
      "config": {
        "host": "localhost",
        "user": "username",
        "password": "passeword",
        "database": "infra"
      },
      "query": "SELECT hostname, port, ipv4, ipv6, user FROM servers"
    }

# Usage

    ssht [-h] name [-4] [-6] 
    
    positional arguments:
      name        name of the host to connect to
    
    optional arguments:
      -h, --help  show this help message and exit
      -4          connect using ipv4 (skip dns if ipv4 address is defined)
      -6          connect using ipv6 (skip dns of ipv6 address is defined)

## Examples

### Find host based on a part of the hostname or IP

    $ ssht host01
    Connecting to "host01.example.com" (192.168.0.1)

### Select a host when multiple results have been found

    $ ssht 192.168
    1) host01.example.com
	2) host02.example.org
	Connect to: 2
    Connecting to "host02.example.org" (192.168.0.2)

### Use Linux style filename matching

    $ ssht host*.example.org
    Connecting to "host02.example.org"

