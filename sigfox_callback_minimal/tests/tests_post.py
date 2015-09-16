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


# This function formats the data that is sent.
def format_data(d):
    frame = "time={}".format(int(time.time()))
    for k, v in d.items():
        frame = frame + "&{}={}".format(k, v)

    return frame


# Can not post on /raws, /devices, /events
def test_post_on_wrong_path():
    r = requests.post(url="http://{}:{}/{}".format(addr, port, "raws"),
                      verify=False)

    assert r.status_code == 404

    r = requests.post(url="http://{}:{}/{}".format(addr, port, "devices"),
                      verify=False)

    assert r.status_code == 404

    r = requests.post(url="http://{}:{}/{}".format(addr, port, "events"),
                      verify=False)

    assert r.status_code == 404


# Testing the callback
def test_callback():
    l = [
        {
            "data": "3794a01820348220590d000f",
            "device": "153FF",
            "duplicate": "false",
            "rssi": "-123.10",
            "snr": "23.67",
            "station": "E4BE",
            "seqNumber": "2"
        },
        {
            "avgSignal": "21.73",
            "data": "3794a01820348220590d000f",
            "device": "153FF",
            "duplicate": "false",
            "rssi": "-123.10",
            "snr": "23.67",
            "station": "E4BE",
            "seqNumber": "2"
        },
    ]

    r = requests.post(url="http://{}:{}/".format(addr, port),
                      data=bytes(format_data(l[0]), 'UTF-8'),
                      verify=False)

    assert r.status_code == 400

    r = requests.post(url="http://{}:{}/".format(addr, port),
                      data=bytes(format_data(l[1]), 'UTF-8'),
                      verify=False)

    assert r.status_code == 204


# Testing the downlink
def test_downlink():
    l = [
        {
            "avgSignal": "21.73",
            "data": "3794a01820348220590d000f",
            "device": "153FF",
            "duplicate": "false",
            "rssi": "-123.10",
            "snr": "23.67",
            "station": "E4BE",
            "seqNumber": "2",
            "ack": "false",
            "longPolling": "false"
        },
        {
            "avgSignal": "21.73",
            "data": "3794a01820348220590d000f",
            "device": "153FF",
            "duplicate": "false",
            "rssi": "-123.10",
            "snr": "23.67",
            "station": "E4BE",
            "seqNumber": "2",
            "ack": "false",
            "longPolling": "true"
        },
        {
            "avgSignal": "21.73",
            "data": "3794a01820348220590d000f",
            "device": "153FF",
            "duplicate": "false",
            "rssi": "-123.10",
            "snr": "23.67",
            "station": "E4BE",
            "seqNumber": "2",
            "ack": "true",
            "longPolling": "false"
        },
        {
            "avgSignal": "21.73",
            "data": "3794a01820348220590d000f",
            "device": "153FF",
            "duplicate": "false",
            "rssi": "-123.10",
            "snr": "23.67",
            "station": "E4BE",
            "seqNumber": "2",
            "ack": "true",
            "longPolling": "true"
        },
    ]

    r = requests.post(url="http://{}:{}/".format(addr, port),
                      data=bytes(format_data(l[0]), 'UTF-8'),
                      verify=False)

    assert r.status_code == 204

    r = requests.post(url="http://{}:{}/".format(addr, port),
                      data=bytes(format_data(l[1]), 'UTF-8'),
                      verify=False)

    assert r.status_code == 204

    r = requests.post(url="http://{}:{}/".format(addr, port),
                      data=bytes(format_data(l[2]), 'UTF-8'),
                      verify=False)

    assert r.status_code == 200
    assert r.text == '{"153FF": {"downlinkData": "3794a01820348220"}}'

    r = requests.post(url="http://{}:{}/".format(addr, port),
                      data=bytes(format_data(l[3]), 'UTF-8'),
                      verify=False)

    assert r.status_code == 200
    assert r.text == '{"153FF": {"downlinkData": "3794a01820348220"}}'
