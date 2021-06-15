CREATE DATABASE  IF NOT EXISTS `smartpccase` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `smartpccase`;
-- MySQL dump 10.13  Distrib 8.0.20, for macos10.15 (x86_64)
--
-- Host: localhost    Database: smartpccase
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `slug` varchar(45) NOT NULL,
  `icon` varchar(100) DEFAULT NULL,
  `input` tinyint NOT NULL,
  `output` tinyint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Power','power','power_settings_new',0,1),(2,'Ventilatoren','fan','air',0,1),(3,'Ledstrips','ledstrip','lightbulb',0,1),(4,'Temperatuur','temperature','thermostat',1,0),(5,'Verbruik','consumption','electrical_services',1,0);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `output`
--

DROP TABLE IF EXISTS `output`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `output` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(100) NOT NULL,
  `icon` varchar(100) NOT NULL,
  `output_num` int NOT NULL,
  `is_pwm` tinyint NOT NULL DEFAULT '0',
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `fk_output_category1_idx` (`category_id`),
  CONSTRAINT `fk_output_category1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `output`
--

LOCK TABLES `output` WRITE;
/*!40000 ALTER TABLE `output` DISABLE KEYS */;
INSERT INTO `output` VALUES (1,'Power button','Computer opstarten','power_settings_new',12,0,1),(2,'Fan 1','Vooraan, bovenste van 2','air',21,1,2),(3,'Fan 2','Vooraan, onderste van 2','air',20,1,2),(4,'Fan 3','Achteraan','air',16,1,2),(5,'Ledstrip 1','Voorraan','lightbulb',24,1,3),(6,'Ledstrip 2','Achteraan','lightbulb',23,1,3);
/*!40000 ALTER TABLE `output` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `output_history`
--

DROP TABLE IF EXISTS `output_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `output_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `output_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `value` int NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_output_history_output1_idx` (`output_id`),
  KEY `fk_output_history_user1_idx` (`user_id`),
  CONSTRAINT `fk_output_history_output1` FOREIGN KEY (`output_id`) REFERENCES `output` (`id`),
  CONSTRAINT `fk_output_history_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `output_history`
--

LOCK TABLES `output_history` WRITE;
/*!40000 ALTER TABLE `output_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `output_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor`
--

DROP TABLE IF EXISTS `sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `unit` varchar(5) DEFAULT NULL,
  `input_bus` varchar(10) NOT NULL,
  `input_pin` varchar(20) NOT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `index_input_pin` (`input_pin`),
  KEY `fk_sensor_category1_idx` (`category_id`),
  CONSTRAINT `fk_sensor_category1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor`
--

LOCK TABLES `sensor` WRITE;
/*!40000 ALTER TABLE `sensor` DISABLE KEYS */;
INSERT INTO `sensor` VALUES (1,'Temperatuur','°C','one_wire','28-3c01d6071f78',4),(2,'Stroomverbruik','A','serial','1',5),(3,'Spanning bron','V','serial','2',5);
/*!40000 ALTER TABLE `sensor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_history`
--

DROP TABLE IF EXISTS `sensor_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sensor_id` int NOT NULL,
  `value` float NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_sensor_history_sensor_idx` (`sensor_id`),
  CONSTRAINT `fk_sensor_history_sensor` FOREIGN KEY (`sensor_id`) REFERENCES `sensor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_history`
--

LOCK TABLES `sensor_history` WRITE;
/*!40000 ALTER TABLE `sensor_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensor_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` text,
  `enabled` tinyint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'system','System',NULL,NULL,0),(2,'guillaume','Guillaume','guillaume.deplancke@student.howest.be',NULL,1),(3,'demo','Demo',NULL,NULL,1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-15 16:11:59
