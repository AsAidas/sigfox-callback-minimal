-- CREATION OF THE DATABASE SIGFOX AND ITS TABLES WITH SOME DATA

--
-- Creation of the database
--
CREATE DATABASE  IF NOT EXISTS `sigfox`;
USE `sigfox`;


--
-- Creation of sigfox user
--
CREATE USER 'sigfox'@'localhost' IDENTIFIED BY 'sigfox1234';
GRANT ALL PRIVILEGES ON `sigfox`.* TO 'sigfox'@'localhost';


-- Delete the tables if they exists
DROP TABLE IF EXISTS `raws`;
DROP TABLE IF EXISTS `events`;
DROP TABLE IF EXISTS `devices`;


--
-- Create 'raws' table
--
CREATE TABLE `raws` (
  `idraws` int(11) NOT NULL AUTO_INCREMENT,
  `time` int(11) NOT NULL,
  `device` varchar(8) NOT NULL,
  `snr` decimal(5,2) NOT NULL,
  `station` varchar(8) NOT NULL,
  `ack` varchar(5) DEFAULT NULL,
  `data` varchar(24) NOT NULL,
  `duplicate` varchar(5) NOT NULL,
  `avgSignal` decimal(5,2) NOT NULL,
  `rssi` decimal(5,2) NOT NULL,
  `longPolling` varchar(5) DEFAULT NULL,
  `seqNumber` int(11) NOT NULL,
  PRIMARY KEY (`idraws`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


--
-- Create 'events' table
--
CREATE TABLE `events` (
  `idevents` int(11) NOT NULL AUTO_INCREMENT,
  `idmodem` varchar(8) NOT NULL,
  `time` int(11) NOT NULL,
  `event_type` int(11) NOT NULL,
  `temperature` decimal(5,2) NOT NULL,
  `longitude` int(11) NOT NULL,
  `latitude` int(11) NOT NULL,
  `altitude` int(11) NOT NULL,
  `sign_longitude` int(11) NOT NULL,
  `sign_latitude` int(11) NOT NULL,
  `sign_altitude` int(11) NOT NULL,
  `satellite` int(11) NOT NULL,
  `precision` int(11) NOT NULL,
  `battery` int(11) NOT NULL,
  PRIMARY KEY (`idevents`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


--
-- Create 'devices' table
--
CREATE TABLE `devices` (
  `iddevices` int(11) NOT NULL AUTO_INCREMENT,
  `idmodem` varchar(8) COLLATE utf8_bin NOT NULL,
  `attribution` int(11) DEFAULT NULL,
  `timestamp_attribution` int(11) DEFAULT NULL,
  PRIMARY KEY (`iddevices`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `devices`
--
LOCK TABLES `devices` WRITE;
INSERT INTO `devices` VALUES (1,'1545F',NULL,NULL),(2,'153FF',NULL,NULL),(3,'E521',NULL,NULL);
UNLOCK TABLES;