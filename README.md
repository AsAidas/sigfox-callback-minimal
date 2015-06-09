# SIGFOX CALLBACK MINIMAL #

Sigfox callback minimal HTTP server


## Prerequisites ##

* [Git](https://git-scm.com/downloads)
* [Python 3](https://www.python.org/downloads/release/python-343/)


## Installation ##

Clone the repository
```
$ git clone https://github.com/hbuyse/sigfox-callback-minimal
```


## Callback data formatting ##

In the Callback part, create a new callback :

* Type : DATA, UPLINK
* Channel : URL
* URL Pattern : http://*address*:*port*/*path*?device={device}&time={time}&station={station}&snr={snr}&data={data}&ack={ack}
* Use HTTP Post : checked


## Start the server ##

* Configure the config.ini

* Start the server
  ```
  $ python3 main.py
  ```


## Start the client ##

* Configure the config.ini

* Start the client
  ```
  $ python3 client.py
  ```

## Contributors ##

* [Henri Buyse](mailto:henri.buyse.pro@gmail.com)
