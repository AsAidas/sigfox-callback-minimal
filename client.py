#! /usr/bin/env python3

__author__ = 'hbuyse'

import requests
import configparser
import time
import threading
import ssl

# Configuration Part
# All datas can be configured in the file `config.ini`
c = configparser.ConfigParser()
c.read("./config.ini")
ack = c.get("client_data", "ack")
addr = c.get("client_config", "address")
api_path = c.get("client_config", "api_path")
port = c.getint("client_config", "port")
data = c.get("client_data", "data")
device = c.get("client_data", "device")
snr = c.get("client_data", "snr")
station = c.get("client_data", "station")
tm = int(time.time())
threads = c.get("client_data", "threads")


class ClientThreadManager:

    """
    Manager of the threads
    """

    def __init__(self):
        pass

    def start(self, threads):
        thread_refs = list()

        for i in range(int(threads)):
            t = ClientThread(i)
            t.daemon = True
            print("[ClientThreadManager.start] Starting thread {}".format(i))
            thread_refs.append(t)
            t.start()

        for t in thread_refs:
            t.join()


class ClientThread(threading.Thread):

    """
    Thread that connects itself to the server defined by :addr:
    """

    def __init__(self, threadID):
        """
        Constructor
        """
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        """
        Multithreaded function
        """
        frame = "device={}&time={}&snr={}&station={}&data={}&ack={}&threadID={}".format(device, tm, snr, station, data,
                                                                                        ack, self.threadID)
        r = requests.post(url="http://{}:{}/{}".format(addr, port, api_path),
                          data=bytes(frame, 'UTF-8'),
                          verify=False)

        print("{} ({}) > {}".format(str(r.status_code), self.threadID, r.text))


def main():
    manager = ClientThreadManager()
    manager.start(threads)


if __name__ == "__main__":
    main()
