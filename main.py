#! /usr/bin/env python3

__author__ = 'hbuyse'

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import configparser

from request_handler import RequestHandler

c = configparser.ConfigParser()
c.read("./config.ini")
addr = c.get("server_config", "address")
port = c.get("server_config", "port")


def main():
    httpd = HTTPServer((addr, int(port)), RequestHandler)
    print("{} Server Starts - {}:{}".format(time.asctime(), addr, str(port)))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt as e:
        pass

    httpd.server_close()

    print("{} Server Stops - {}:{}".format(time.asctime(), addr, str(port)))

if __name__ == "__main__":
    main()
