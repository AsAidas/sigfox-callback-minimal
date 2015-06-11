#! /usr/bin/env python3

__author__ = 'hbuyse'

import http.client
import configparser
import time
import threading

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
threads = c.get("client_config", "threads")


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

        conn = http.client.HTTPConnection(addr, port)
        conn.request("POST", "/sigfox", bytes(frame, 'UTF-8'))
        response = conn.getresponse()
        conn.close()

        print("{} ({}) > {}".format(str(response.status), self.threadID, response.read().decode('UTF-8')))


def main():
    manager = ClientThreadManager()
    manager.start(threads)


if __name__ == "__main__":
    main()
