-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: my_database
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `target_ranking`
--

DROP TABLE IF EXISTS `target_ranking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `target_ranking` (
  `index` int NOT NULL AUTO_INCREMENT,
  `target_name` text NOT NULL,
  `keyword` text NOT NULL,
  `platform` text NOT NULL,
  `target_ranking` int NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `target_ranking`
--

LOCK TABLES `target_ranking` WRITE;
/*!40000 ALTER TABLE `target_ranking` DISABLE KEYS */;
INSERT INTO `target_ranking` VALUES (1,'성심당','대전 맛집','Naver Search',999,'2024-05-22 22:55:48'),(2,'성심당','대전 맛집','Naver Search',999,'2024-05-22 22:57:33'),(3,'강서면옥','오산 맛집','Naver Search',999,'2024-05-22 22:58:39'),(4,'성심당','대전 맛집','Naver Search',999,'2024-05-22 23:08:07'),(5,'강서면옥','오산 맛집','Naver Search',999,'2024-05-22 23:09:14');
/*!40000 ALTER TABLE `target_ranking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `강서면옥`
--

DROP TABLE IF EXISTS `강서면옥`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `강서면옥` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `강서면옥`
--

LOCK TABLES `강서면옥` WRITE;
/*!40000 ALTER TABLE `강서면옥` DISABLE KEYS */;
INSERT INTO `강서면옥` VALUES (1,1004,'김원민','test','test','2024-05-09 21:03:37'),(2,1008,'김원민','test','tset','2024-05-09 21:05:26'),(3,1004,'김원민','123','123','2024-05-17 18:52:33'),(4,1003,'김원민','23','213','2024-05-17 18:59:37'),(5,1004,'김원민','123','123','2024-05-17 19:16:17'),(6,1004,'김원민','213','123','2024-05-17 20:13:08'),(7,1004,'김원민','213','123','2024-05-17 20:13:18'),(8,1003,'김원민','213','213','2024-05-17 20:25:54'),(9,1003,'김원민','123','123','2024-05-17 20:28:18'),(10,1003,'김원민','123','123','2024-05-17 20:28:20'),(11,1003,'김원민','123','123','2024-05-17 20:28:43'),(12,1003,'김원민','123','123','2024-05-17 20:28:44'),(13,1003,'김원민','123','123','2024-05-17 20:28:44'),(14,1003,'김원민','123','123','2024-05-17 20:28:45'),(15,1004,'김원민','123','123','2024-05-17 20:31:01'),(16,1004,'김원민','123','123','2024-05-17 20:31:02'),(17,1004,'김원민','123','123','2024-05-17 20:31:02'),(18,1004,'김원민','123','123','2024-05-17 20:31:03'),(19,1004,'김원민','123','123','2024-05-17 20:31:04'),(20,1005,'김원민','123','23','2024-05-17 20:34:05'),(21,1005,'김원민','123','23','2024-05-17 20:34:41'),(22,1005,'김원민','123','23','2024-05-17 20:35:40'),(23,1005,'김원민','123','23','2024-05-17 20:35:45'),(24,1005,'김원민','123','23','2024-05-17 20:39:49'),(25,1003,'김원민','123','123','2024-05-17 22:36:01'),(26,1006,'김원민','123','123','2024-05-17 23:21:49'),(27,1005,'김원민','123','123','2024-05-17 23:56:33'),(28,1005,'김원민','123','123','2024-05-17 23:56:38'),(29,1004,'김원민','123','123','2024-05-20 19:50:28'),(30,1004,'김원민','123','123','2024-05-21 17:52:09');
/*!40000 ALTER TABLE `강서면옥` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `명동교자`
--

DROP TABLE IF EXISTS `명동교자`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `명동교자` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `명동교자`
--

LOCK TABLES `명동교자` WRITE;
/*!40000 ALTER TABLE `명동교자` DISABLE KEYS */;
INSERT INTO `명동교자` VALUES (1,1003,'김원민','test','test','2024-05-09 20:56:02');
/*!40000 ALTER TABLE `명동교자` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `부여집`
--

DROP TABLE IF EXISTS `부여집`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `부여집` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `부여집`
--

LOCK TABLES `부여집` WRITE;
/*!40000 ALTER TABLE `부여집` DISABLE KEYS */;
INSERT INTO `부여집` VALUES (1,1005,'김원민','123','','2024-05-16 18:36:06'),(2,1005,'김원민','123','12','2024-05-16 18:37:19'),(3,1005,'김원민','123','123','2024-05-16 18:37:28'),(4,1005,'김원민','123','','2024-05-16 18:37:48'),(5,1005,'김원민','','','2024-05-16 18:37:56'),(6,1005,'김원민','','123','2024-05-16 18:38:06');
/*!40000 ALTER TABLE `부여집` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `분류`
--

DROP TABLE IF EXISTS `분류`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `분류` (
  `id` int NOT NULL,
  `name` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `분류`
--

LOCK TABLES `분류` WRITE;
/*!40000 ALTER TABLE `분류` DISABLE KEYS */;
INSERT INTO `분류` VALUES (1001,'네이버 영수증 리뷰'),(1002,'네이버 기자단'),(1003,'네이버 체험단'),(1004,'네이버 숏 기자단'),(1005,'네이버 숏 기자단(standard)'),(1006,'네이버 플레이스 찜'),(1007,'네이버 플레이스 최적화'),(1008,'네이버 퍼포먼스 마케팅'),(1101,'인스타그램 포스트'),(1102,'인스타그램 좋아요'),(1103,'인스타그램 댓글'),(1104,'인스타그램 외국인 팔로워'),(1105,'인스타그램 한국인 팔로워'),(1106,'인스타그램 계정 최적화'),(1107,'인스타그램 기자단'),(1108,'인스타그램 체험단'),(1201,'구글 찜'),(1202,'구글 리뷰'),(1203,'구글 플레이스 최적화'),(1204,'구글 퍼포먼스 마케팅');
/*!40000 ALTER TABLE `분류` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `새벽집`
--

DROP TABLE IF EXISTS `새벽집`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `새벽집` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `새벽집`
--

LOCK TABLES `새벽집` WRITE;
/*!40000 ALTER TABLE `새벽집` DISABLE KEYS */;
/*!40000 ALTER TABLE `새벽집` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `성심당`
--

DROP TABLE IF EXISTS `성심당`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `성심당` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `성심당`
--

LOCK TABLES `성심당` WRITE;
/*!40000 ALTER TABLE `성심당` DISABLE KEYS */;
INSERT INTO `성심당` VALUES (1,1004,'김원민','test','test','2024-05-13 23:12:49'),(2,1003,'김원민','231','321','2024-05-14 02:19:27');
/*!40000 ALTER TABLE `성심당` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `솔밤`
--

DROP TABLE IF EXISTS `솔밤`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `솔밤` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `솔밤`
--

LOCK TABLES `솔밤` WRITE;
/*!40000 ALTER TABLE `솔밤` DISABLE KEYS */;
/*!40000 ALTER TABLE `솔밤` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `약수순대`
--

DROP TABLE IF EXISTS `약수순대`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `약수순대` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `약수순대`
--

LOCK TABLES `약수순대` WRITE;
/*!40000 ALTER TABLE `약수순대` DISABLE KEYS */;
/*!40000 ALTER TABLE `약수순대` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `온지음`
--

DROP TABLE IF EXISTS `온지음`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `온지음` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `온지음`
--

LOCK TABLES `온지음` WRITE;
/*!40000 ALTER TABLE `온지음` DISABLE KEYS */;
INSERT INTO `온지음` VALUES (1,1001,'김원민','ㅅㅈㄷ23','321','2024-05-14 01:45:37');
/*!40000 ALTER TABLE `온지음` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `올래국수`
--

DROP TABLE IF EXISTS `올래국수`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `올래국수` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `올래국수`
--

LOCK TABLES `올래국수` WRITE;
/*!40000 ALTER TABLE `올래국수` DISABLE KEYS */;
INSERT INTO `올래국수` VALUES (1,1004,'김원민','test','test','2024-05-14 02:02:24');
/*!40000 ALTER TABLE `올래국수` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `우래옥`
--

DROP TABLE IF EXISTS `우래옥`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `우래옥` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `우래옥`
--

LOCK TABLES `우래옥` WRITE;
/*!40000 ALTER TABLE `우래옥` DISABLE KEYS */;
/*!40000 ALTER TABLE `우래옥` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `은호식당`
--

DROP TABLE IF EXISTS `은호식당`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `은호식당` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `은호식당`
--

LOCK TABLES `은호식당` WRITE;
/*!40000 ALTER TABLE `은호식당` DISABLE KEYS */;
/*!40000 ALTER TABLE `은호식당` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `을밀대`
--

DROP TABLE IF EXISTS `을밀대`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `을밀대` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `을밀대`
--

LOCK TABLES `을밀대` WRITE;
/*!40000 ALTER TABLE `을밀대` DISABLE KEYS */;
/*!40000 ALTER TABLE `을밀대` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `을지면옥`
--

DROP TABLE IF EXISTS `을지면옥`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `을지면옥` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `을지면옥`
--

LOCK TABLES `을지면옥` WRITE;
/*!40000 ALTER TABLE `을지면옥` DISABLE KEYS */;
/*!40000 ALTER TABLE `을지면옥` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `이문설농탕`
--

DROP TABLE IF EXISTS `이문설농탕`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `이문설농탕` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `이문설농탕`
--

LOCK TABLES `이문설농탕` WRITE;
/*!40000 ALTER TABLE `이문설농탕` DISABLE KEYS */;
/*!40000 ALTER TABLE `이문설농탕` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `자하손만두`
--

DROP TABLE IF EXISTS `자하손만두`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `자하손만두` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `자하손만두`
--

LOCK TABLES `자하손만두` WRITE;
/*!40000 ALTER TABLE `자하손만두` DISABLE KEYS */;
/*!40000 ALTER TABLE `자하손만두` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `작업자`
--

DROP TABLE IF EXISTS `작업자`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `작업자` (
  `index` int NOT NULL AUTO_INCREMENT,
  `name` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `id` varchar(60) NOT NULL,
  `pw` varchar(60) NOT NULL,
  `authority` int NOT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `ID_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `작업자`
--

LOCK TABLES `작업자` WRITE;
/*!40000 ALTER TABLE `작업자` DISABLE KEYS */;
INSERT INTO `작업자` VALUES (1,'김원민','admin','$2b$12$XG7qwUaWPXNnF7D5vhvpCuo7z3Amyl.8qLfLfoAI7thLbd84e8sOa',1),(2,'박나비','test','$2b$12$FZbiA/p7fDR0WENzbaXQoOTWUZrCfd/l8KVb1KDFBPKIM/AnUA04W',2),(3,'신가명','test1','$2b$12$9d1Qw9FXa/ZpK0VRQkANFO.4zKCnb6IZJnUTO5qndwsbOEeSSg04e',2);
/*!40000 ALTER TABLE `작업자` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `잼배옥`
--

DROP TABLE IF EXISTS `잼배옥`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `잼배옥` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `잼배옥`
--

LOCK TABLES `잼배옥` WRITE;
/*!40000 ALTER TABLE `잼배옥` DISABLE KEYS */;
/*!40000 ALTER TABLE `잼배옥` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `필동면옥`
--

DROP TABLE IF EXISTS `필동면옥`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `필동면옥` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `필동면옥`
--

LOCK TABLES `필동면옥` WRITE;
/*!40000 ALTER TABLE `필동면옥` DISABLE KEYS */;
/*!40000 ALTER TABLE `필동면옥` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `하동관`
--

DROP TABLE IF EXISTS `하동관`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `하동관` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `하동관`
--

LOCK TABLES `하동관` WRITE;
/*!40000 ALTER TABLE `하동관` DISABLE KEYS */;
/*!40000 ALTER TABLE `하동관` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `한일관`
--

DROP TABLE IF EXISTS `한일관`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `한일관` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `한일관`
--

LOCK TABLES `한일관` WRITE;
/*!40000 ALTER TABLE `한일관` DISABLE KEYS */;
INSERT INTO `한일관` VALUES (1,1003,'김원민','test','test','2024-05-14 02:20:23');
/*!40000 ALTER TABLE `한일관` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `홍박사생고기`
--

DROP TABLE IF EXISTS `홍박사생고기`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `홍박사생고기` (
  `index` int NOT NULL AUTO_INCREMENT,
  `id` int DEFAULT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `홍박사생고기`
--

LOCK TABLES `홍박사생고기` WRITE;
/*!40000 ALTER TABLE `홍박사생고기` DISABLE KEYS */;
/*!40000 ALTER TABLE `홍박사생고기` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-22 23:34:14
