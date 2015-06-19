__author__ = 'hbuyse'

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

import configparser
import json
import logging
import pymysql
import time

# Configuration Part
# All datas can be configured in the file `config.ini`
c = configparser.ConfigParser()
c.read("./config.ini")
api_path = c.get("server_config", "api_path")

host = c.get("mysql56", "host")
port = int(c.get("mysql56", "port"))
user = c.get("mysql56", "user")
passwd = c.get("mysql56", "passwd")
db = c.get("mysql56", "db")

# Logging configuration
logging.basicConfig(filename='tim.log',
                    format='%(asctime)s / %(levelname)s > %(message)s',
                    level=logging.DEBUG)

# Commands that are send to the database
# insert_db_events: allow us to send frames to the database
# delete_db_events: allow us to delete a row using the device ID and the timestamp
# select_db_events: allow us to get all datas of the database
insert_db_raws = "INSERT INTO `raws` (`time`, `device`, `snr`, `station`, `ack`, `data`, `duplicate`, `avgSignal`, \
                                      `rssi`, `longPolling`) \
                  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
delete_db_raws = "DELETE FROM `raws` WHERE `time` = %s AND `device` = %s"
select_db_raws  = "SELECT * FROM `raws`;"

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):

    """Handle requests in a separate thread.
    """


class RequestHandler(BaseHTTPRequestHandler, object):

    def do_HEAD(self):
        """Respond to a HEAD request.

        Equivalent to a ping on a webpage.
        We send a 200 status code/
        """
        # If the user is asking datas from a wrong url, we send him a 404 status code
        if self.path != "/{}".format(api_path):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("Error: the page does not exist.", 'UTF-8'))
            
            logging.error("(404) HEAD from {} on {}".format(self.client_address[0], self.path))
            return

        self.send_response(200)

        self.send_header("Content-type", "application/json")
        self.end_headers()

        logging.info("(200) HEAD from {} on {}".format(self.client_address[0], self.path))

    def do_GET(self):
        """Respond to a GET request.

        Allow the users to watch all the frames that are contained in the database on a web browser
        """
        l = list()

        # If the user is asking datas from a wrong url, we send him a 404 status code
        if self.path != "/{}".format(api_path):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("Error: the page does not exist.", 'UTF-8'))
            
            logging.error("(404) GET from {} on {}".format(self.client_address[0], self.path))
            return

        # Connection to the database and asking for all datas contained in the table 'events' from the
        # database 'sigfox'
        try:
            conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
            events = pymysql.cursors.DictCursor
            with conn:
                cur = conn.cursor(pymysql.cursors.DictCursor)
                cur.execute(select_db_raws)
                events = cur
                cur.close()
        except (Exception, KeyError) as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes("{}".format(repr(e)), 'UTF-8'))

            logging.error("{}".format(repr(e)))

        for e in events:
            d = dict()
            for k, v in e.items():
                if k == "snr":
                    d[k] = float(v)
                else:
                    d[k] = v
            l.append(d)

        # We send a 200 status code if the user is asking datas from the right url
        # We are sending back a JSON web page
        # Printing on the webpage
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes("{}".format(l), 'UTF-8'))
        
        logging.info("(200) GET from {} on {}".format(self.client_address[0], self.path))

    def do_POST(self):
        """Respond to a POST request.

        Stock the frames into the database
        Respond with :
        * a 404 if SigFox send the datas on a wrong URL,
        * a 400 if there is a bad request
        * a 200 if SigFox send right datas and if it asks for a Downlink,
        * a 204 if SigFox send right datas without asking for a Downlink.
        """
        d = dict()
        downlink_response = dict()

        # Get the length of the datas received
        # Get the datas
        length = int(self.headers['Content-length'])
        requete = str(self.rfile.read(length).decode('UTF-8'))

        # If the user is asking datas from a wrong url, we send him a 404 status code
        if self.path != "/{}".format(api_path):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("Error: the page does not exist.", 'UTF-8'))

            logging.error("(404) POST from {} on {}".format(self.client_address[0], self.path))
            return

        # Split the data that are send from Sigfox in order to stock them in a dictionary
        # A dictionary is :
        #       {
        #           key  : value,
        #           key2 : value2,
        #       }
        for i in requete.split("&"):
            d[i.split("=")[0]] = i.split("=")[1]

        if "ack" not in d:
            d["ack"] = "false"

        if "longPolling" not in d:
            d["longPolling"] = "false"

        # Check if the device which frame was send by SigFox is one of the device we follow
        # and the length of the frame is 24 hexadecimal characters.
        # After this, we send the datas to the database.

        try:
            v = (d["time"], d["device"], d["snr"], d["station"], d["ack"], d["data"], d["duplicate"], d["avgSignal"], d["rssi"], d["longPolling"])
            conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
            with conn:
                cur = conn.cursor()
                cur.execute(insert_db_raws, v)
                conn.commit()
                cur.close()
        except (Exception, KeyError) as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes("{}".format(repr(e)), 'UTF-8'))

            logging.error("(400) POST from {} on {}: {} ".format(self.client_address[0], self.path, repr(e)))

            return

        # If we need to send back a downlink, here is the part to alter
        # If the downlink is needed, we send a 200 status code (OK) and the data we want to send back in the dictionary
        # Else, we send a 204 status code (NO_CONTENT) to acknowledge SigFox
        try:
            if d["ack"] == "true":
                self.send_response(200)
                self.end_headers()
                # HERE BEGIN THE DOWNLINK PART
                downlink_response = {
                    d["device"]: {
                        "downlinkData": d["data"][:16]
                    }
                }
                # HERE IS THE END OF THE DOWNLINK PART
                self.wfile.write(bytes("{}".format(downlink_response), 'UTF-8'))

                logging.info("(200) POST from {} on {}: {}".format(self.client_address[0], self.path, d))
                logging.info("(200) Downlink response: {}".format(self.client_address[0], self.path, downlink_response))
            else:
                self.send_response(204)
                self.end_headers()

                logging.info("(204) POST from {} on {}: {}".format(self.client_address[0], self.path, d))
        except KeyError as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes("{}".format(repr(e)), 'UTF-8'))

            logging.error("(400) POST from {} on {}: {} ".format(self.client_address[0], self.path, repr(e)))

            return

    def do_DELETE(self):
        """Respond to a DELETE request.

        Allow the user to delete one or multiple rows on the database using the timestamp of the frame and the device
        ID that send the frame
        """
        d = dict()

        # Get the length of the datas received
        # Get the datas
        length = int(self.headers['Content-length'])
        requete = str(self.rfile.read(length).decode('UTF-8'))

        # If the user is asking datas from a wrong url, we send him a 404 status code
        if self.path != "/{}".format(api_path):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("Error: the page does not exist.", 'UTF-8'))

            logging.error("(404) DELETE from {} on {}".format(self.client_address[0], self.path))
            return

        # Split the data that are send from Sigfox in order to stock them in a dictionary
        # A dictionary is :
        #       {
        #           key  : value,
        #           key2 : value2,
        #       }
        for i in requete.split("&"):
            d[i.split("=")[0]] = i.split("=")[1]

        # Connect to the database and delete the row(s)
        try:
            v = (d["time"], d["device"])
            conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
            with conn:
                cur = conn.cursor()
                cur.execute(delete_db_raws, v)
                cur.close()
        except (Exception, KeyError) as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes("{}".format(repr(e)), 'UTF-8'))

            logging.error("(400) POST from {} on {}: {}".format(self.client_address[0], self.path, repr(e)))

        # We send a 200 status code with datas
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes("{}".format(d), 'UTF-8'))

        logging.info("(200) DELETE from {} on {}: {} ".format(self.client_address[0], self.path, d))
