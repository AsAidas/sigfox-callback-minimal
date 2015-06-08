#! /usr/bin/env python3

__author__ = 'hbuyse'

import http.client
import configparser
import time


def main():
    c = configparser.ConfigParser()
    c.read("./config.ini")
    ack = c.get("client_config", "ack")
    addr = c.get("client_config", "address")
    port = c.getint("client_config", "port")
    data = c.get("client_config", "data")
    device = c.get("client_config", "device")
    snr = c.get("client_config", "snr")
    station = c.get("client_config", "station")
    tm = int(time.time())

    frame = "device={}&time={}&snr={}&station={}&data={}&ack={}".format(device, tm, snr, station, data, ack)

    conn = http.client.HTTPConnection(addr, port)
    conn.request("POST", "/sigfox", bytes(frame, 'UTF-8'))
    response = conn.getresponse()
    conn.close()

    print(
        "{}\n{} > {}".format(frame, str(response.status), response.read().decode('UTF-8')))

if __name__ == "__main__":
    main()
