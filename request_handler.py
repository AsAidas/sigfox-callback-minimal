__author__ = 'hbuyse'

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


l = list()


class RequestHandler(BaseHTTPRequestHandler, object):

    def do_HEAD(self):
        self.send_response(200)

        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)

        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(bytes("{}".format(json.dumps(l, indent=4, sort_keys=True)), 'UTF-8'))

    def do_POST(self):
        d = dict()
        length = int(self.headers['Content-length'])
        requete = str(self.rfile.read(length).decode('UTF-8'))

        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes("Received", 'UTF-8'))

        print("{}\n{}".format(self.path, requete))

        for i in requete.split("&"):
            d[i.split("=")[0]] = i.split("=")[1]

        l.append(d)
        print("{}".format(json.dumps(d, indent=4, sort_keys=True)))
