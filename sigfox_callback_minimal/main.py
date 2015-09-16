#! /usr/bin/env python3

__author__ = 'hbuyse'

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import configparser
import ssl
import sqlite3

from frame import Frame
from request_handler import RequestHandler, ThreadedHTTPServer

# Configuration Part
# All datas can be configured in the file `config.ini`
c = configparser.ConfigParser()
c.read("./config.ini")
addr = c.get("server_config", "address")
port = c.get("server_config", "port")


def create_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS raws (
        `idraws` INTEGER PRIMARY KEY,
        `time` INTEGER,
        `device` TEXT,
        `snr` REAL,
        `station` TEXT,
        `ack` TEXT,
        `data` TEXT,
        `duplicate` TEXT,
        `avgSignal` REAL,
        `rssi` REAL,
        `longPolling` TEXT,
        `seqNumber` INTEGER
    )''')
    conn.commit()
    conn.close()



def main():
    create_database()

    print("{} Starting HTTP(S) Server - {}:{}".format(time.asctime(), addr, str(port)))

    # Create a multi-threaded HTTPS webservice
    httpd = ThreadedHTTPServer((addr, int(port)), RequestHandler)
    # httpd.socket = ssl.wrap_socket(httpd.socket,
    #                                certfile="./certs/localhost.crt",
    #                                server_side=True,
    #                                keyfile="./certs/localhost.key")

    # Start the webservice
    try:
        httpd.serve_forever()
    except KeyboardInterrupt as e:
        pass

    # Stop the webservice
    httpd.server_close()

    print("{} Server Stops - {}:{}".format(time.asctime(), addr, str(port)))

if __name__ == "__main__":
    main()
