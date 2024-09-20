CREATE DATABASE  IF NOT EXISTS `vandelay_733_747` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `vandelay_733_747`;
-- MySQL dump 10.13  Distrib 5.6.13, for Win32 (x86)
--
-- Host: localhost    Database: vandelay_733_747
-- ------------------------------------------------------
-- Server version	5.5.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `clerks`
--

DROP TABLE IF EXISTS `clerks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clerks` (
  `clerk_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `clerk_first_name` varchar(15) NOT NULL DEFAULT '',
  `clerk_last_name` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`clerk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clerks`
--

LOCK TABLES `clerks` WRITE;
/*!40000 ALTER TABLE `clerks` DISABLE KEYS */;
INSERT INTO `clerks` VALUES (1,'George','Costanza'),(2,'Elaine','Benes'),(3,'Jerry','Seinfeld'),(4,'Cosmo','Kramer'),(5,'Bob','Sacamano');
/*!40000 ALTER TABLE `clerks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customers` (
  `customer_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `customer_first_name` varchar(15) NOT NULL DEFAULT '',
  `customer_last_name` varchar(30) NOT NULL DEFAULT '',
  `customer_address` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Clark','Kent','Planet Kripton'),(2,'Bruce','Wayne','Gotham City'),(3,'Peter','Parker','New York City');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_items`
--

DROP TABLE IF EXISTS `inventory_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory_items` (
  `item_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `item_name` varchar(15) NOT NULL DEFAULT '',
  `item_description` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_items`
--

LOCK TABLES `inventory_items` WRITE;
/*!40000 ALTER TABLE `inventory_items` DISABLE KEYS */;
INSERT INTO `inventory_items` VALUES (1,'Pez Dispenser','Used for storing and dispensing Pez candy'),(2,'Junior Mint','So refreshing'),(3,'Puffy Shirt','Always in fashion'),(4,'Non-fat Yogurt','For those who watch the calories'),(5,'Label Maker','Comes in various colors'),(6,'Fusilli Figurin','Highly collectible'),(7,'Shower Head','Commando 450 - The most powerful shower head this side of Hudson'),(8,'Chicken Roaster','Must be used with eye protection');
/*!40000 ALTER TABLE `inventory_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `line_items`
--

DROP TABLE IF EXISTS `line_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `line_items` (
  `order_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `item_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `item_quantity` float unsigned NOT NULL DEFAULT '0',
  `item_unit_price` float unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`order_id`,`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `line_items`
--

LOCK TABLES `line_items` WRITE;
/*!40000 ALTER TABLE `line_items` DISABLE KEYS */;
INSERT INTO `line_items` VALUES (1,2,1,2.55),(1,3,2,5.2),(1,4,2,1.99),(2,1,1,2.99),(2,2,1,3.11),(2,5,5,9.99),(3,3,5,3.85),(3,8,1,0.99),(4,3,6,5.2),(4,6,2,2.25),(4,7,3,8.5),(5,4,4,1.99),(5,6,1,2.25),(6,1,3,2.99),(7,1,3,3.19),(8,3,2,3.99),(8,5,2,8.99),(9,2,3,2.1),(9,4,2,1.99),(9,8,1,0.99),(10,5,3,9.25),(10,7,1,8.99);
/*!40000 ALTER TABLE `line_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders` (
  `order_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `order_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `customer_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `clerk_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'2012-04-20 00:00:00',3,2),(2,'2012-04-21 00:00:00',2,3),(3,'2012-04-21 00:00:00',3,1),(4,'2012-04-22 00:00:00',2,1),(5,'2012-04-25 00:00:00',2,4),(6,'2012-04-26 00:00:00',3,4),(7,'2012-05-03 00:00:00',2,3),(8,'2012-05-11 00:00:00',3,1),(9,'2012-05-13 00:00:00',1,2),(10,'2012-05-20 00:00:00',1,4),(11,'2012-05-22 00:00:00',1,2),(12,'2012-05-27 00:00:00',2,0);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-02-07 14:02:01
