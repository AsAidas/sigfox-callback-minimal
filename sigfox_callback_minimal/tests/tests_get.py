#! /usr/bin/env python3

__author__ = 'hbuyse'

import requests
import pytest
import time
import configparser

# Configuration Part
# All datas can be configured in the file `config.ini`
c = configparser.ConfigParser()
c.optionxform = str
c.read("./sigfox_callback_minimal/config.ini")
addr = c.get("client_config", "address")
port = c.getint("client_config", "port")

def test_get():
    r = requests.get(url="http://{}:{}/test".format(addr, port),
                      verify=False)
    assert r.status_code == 404

    r = requests.get(url="http://{}:{}/".format(addr, port),
                      verify=False)
    assert r.status_code == 200