# SIGFOX CALLBACK MINIMAL #

Sigfox callback minimal HTTP server


## Prerequisites ##

### System ###

* [Git](https://git-scm.com/downloads)
* [Python 3](https://www.python.org/downloads/release/python-343/)
* [MySQL 5.6](http://dev.mysql.com/downloads/windows/installer/5.6.html)
* [Pip](https://pypi.python.org/pypi/pip)


### Python (Using Pip3 for Python 3.x) ###

* [Requests](https://pypi.python.org/pypi/requests/2.7.0)
* [PyMySQL](https://pypi.python.org/pypi/PyMySQL/0.6.6)


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


## Create the database ##

Script that creates the database and the table used by this program.

```
CREATE SCHEMA 'sigfox';

CREATE TABLE 'sigfox.events' (
  'idevents' int(11) NOT NULL AUTO_INCREMENT,
  'time' int(11) NOT NULL,
  'device' varchar(8) NOT NULL,
  'snr' decimal(4,2) NOT NULL,
  'station' varchar(8) NOT NULL,
  'ack' varchar(5) NOT NULL,
  'data' varchar(24) NOT NULL,
  PRIMARY KEY ('idevents')
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

CREATE USER 'sigfox'@'localhost' IDENTIFIED BY 'sigfox1234';
GRANT ALL PRIVILEGES ON 'sigfox.events' TO 'sigfox'@'localhost';
FLUSH PRIVILEGES;
```


## Start the server ##

* Configure the config.ini

* Start the server

```
$ python3 main.py
```


## Stop the server ##

While the server is running, you can stop it using the keyboard combinaison **Ctrl**+**C**


## Start the client ##

* Configure the config.ini

* Start the client

```
$ python3 client.py
```


## Contributors ##

* [Henri Buyse](mailto:henri.buyse.pro@gmail.com)