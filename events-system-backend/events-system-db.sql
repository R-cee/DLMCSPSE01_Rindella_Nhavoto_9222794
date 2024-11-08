-- MySQL dump 10.13  Distrib 9.0.1, for Win64 (x86_64)
--
-- Host: localhost    Database: events-system-db
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_details`
--

DROP TABLE IF EXISTS `admin_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_details` (
  `admin_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `surname` varchar(100) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `country` varchar(100) NOT NULL,
  PRIMARY KEY (`admin_id`),
  CONSTRAINT `admin_details_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_details`
--

LOCK TABLES `admin_details` WRITE;
/*!40000 ALTER TABLE `admin_details` DISABLE KEYS */;
INSERT INTO `admin_details` VALUES (4,'Kora','Menete','844578202','Mozambique'),(5,'Salomão ','Chiule','869852222','Mozambique');
/*!40000 ALTER TABLE `admin_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `host_id` int NOT NULL,
  `event_name` varchar(100) NOT NULL,
  `event_description` text,
  `event_category` varchar(100) NOT NULL,
  `event_country` varchar(100) NOT NULL,
  `event_location` varchar(100) NOT NULL,
  `event_date` datetime NOT NULL,
  `event_price` float NOT NULL,
  `event_capacity` int DEFAULT NULL,
  `event_poster` varchar(200) DEFAULT NULL,
  `event_status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `host_id` (`host_id`),
  CONSTRAINT `events_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,2,'Jazz Festival','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s,','Music','Mozambique','Poetas, Matola','2024-10-21 16:30:00',1500,42,'kyle-head-p6rNTdAPbuk-unsplash.jpg','Approved','2024-10-12 23:34:10'),(3,2,'Soccer Leagues','Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker','Sports','Mozambique','Chiango, Marracuene','2024-10-26 10:30:00',350,94,'1_KY59FfitwkNmxoBfJFbaKw.webp','Approved','2024-10-19 18:29:09'),(4,2,'Halloween Party','Curabitur quis sem sed est auctor varius. Aliquam scelerisque massa a scelerisque dictum.','Other','Mozambique','AIS','2024-10-31 19:42:00',649,42,'hall.jpg','Canceled','2024-10-20 02:42:53'),(5,7,'Roots Theater','Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit','Arts','Mozambique','Jardim Tonduro, Baixa','2024-11-15 15:30:00',300,56,'1_KY59FfitwkNmxoBfJFbaKw.webp','Approved','2024-11-01 16:37:23'),(6,7,'Food Fair','Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. ','Food','Mozambique','FA - Parque Dos Poetas','2024-12-02 11:40:00',90,298,'prosciutto-stuffed-chicken-with-mushroom-sauce-51122430.jpg','Approved','2024-11-01 16:42:52');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `likes` (
  `like_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `event_id` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`like_id`),
  KEY `user_id` (`user_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES (1,3,1,'2024-10-19 14:01:55'),(2,3,3,'2024-10-19 20:16:04');
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `notification_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`notification_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (2,2,'Your profile has been approved.',1,'2024-10-10 23:25:12'),(3,2,'Jazz Festival has been approved.',1,'2024-10-16 06:20:21'),(4,2,'Jazz Festival has been approved.',1,'2024-10-16 06:31:40'),(5,3,'Jazz Festival is approaching on 2024-10-21 16:30',1,'2024-10-19 14:53:20'),(6,2,'Soccer Leagues has been approved.',1,'2024-10-19 18:36:29'),(11,3,'Soccer Leagues is approaching on 2024-10-20 10:30',1,'2024-10-19 20:41:39'),(12,2,'Halloween Party has been approved.',1,'2024-10-20 02:43:21'),(15,3,'Event \'Halloween Party\' has been canceled, and your payment has been refunded.',0,'2024-10-20 17:11:02'),(16,3,'Event \'Halloween Party\' has been canceled, and your payment has been refunded.',0,'2024-10-20 17:11:03'),(17,7,'Your profile has been approved.',1,'2024-11-01 16:24:36'),(18,7,'Food Fair has been approved.',1,'2024-11-01 17:01:35'),(19,7,'Roots Theater has been approved.',1,'2024-11-01 17:01:40');
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_accounts`
--

DROP TABLE IF EXISTS `payment_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_accounts` (
  `payment_account_id` int NOT NULL AUTO_INCREMENT,
  `host_id` int NOT NULL,
  `stripe_account_id` varchar(50) DEFAULT NULL,
  `mpesa_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`payment_account_id`),
  KEY `host_id` (`host_id`),
  CONSTRAINT `payment_accounts_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_accounts`
--

LOCK TABLES `payment_accounts` WRITE;
/*!40000 ALTER TABLE `payment_accounts` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles`
--

DROP TABLE IF EXISTS `profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profiles` (
  `profile_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `host_type` varchar(20) NOT NULL,
  `document_id` varchar(200) DEFAULT NULL,
  `business_certificate` varchar(200) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`profile_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles`
--

LOCK TABLES `profiles` WRITE;
/*!40000 ALTER TABLE `profiles` DISABLE KEYS */;
INSERT INTO `profiles` VALUES (1,2,'Rindella','Nhavoto','844867585','Avenida Angola','Individual','android.png',NULL,'Approved'),(2,6,'Emmanuel','Cuambe','855471033','Avenida Angola','Organization','android.png','androiid.png','Pending'),(3,7,'Shaggy','Jones','869870050','Versalhes','Individual','database_logo.jpg',NULL,'Approved');
/*!40000 ALTER TABLE `profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `user_id` int NOT NULL,
  `transaction_date` datetime DEFAULT NULL,
  `payment_status` varchar(20) NOT NULL,
  `amount_paid` float NOT NULL,
  `quantity` int NOT NULL,
  `stripe_payment_intent_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `event_id` (`event_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`),
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,1,3,'2024-10-14 23:58:52','Success',4500,3,NULL),(2,1,3,'2024-10-17 21:10:55','Success',6000,4,NULL),(3,3,3,'2024-10-19 21:18:51','Success',1400,4,NULL),(4,1,3,'2024-10-20 00:41:52','Success',9000,6,NULL),(5,3,3,'2024-10-20 02:38:38','Success',700,2,'pi_3QBp2CP5Lv2xb3IZ16TgFfnh'),(6,4,3,'2024-10-20 02:44:47','Success',3894,6,'pi_3QBp7YP5Lv2xb3IZ1UPvzPpe'),(7,4,3,'2024-10-20 02:45:37','Success',1298,2,'pi_3QBp8hP5Lv2xb3IZ0KtPhSfM'),(8,4,3,'2024-10-20 17:11:02','Refunded',3894,6,'pi_3QBp7YP5Lv2xb3IZ1UPvzPpe'),(9,4,3,'2024-10-20 17:11:03','Refunded',1298,2,'pi_3QBp8hP5Lv2xb3IZ0KtPhSfM'),(10,6,8,'2024-11-01 17:26:46','Success',180,2,NULL),(11,5,8,'2024-11-02 22:01:44','Success',300,4,NULL);
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_interactions`
--

DROP TABLE IF EXISTS `user_interactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_interactions` (
  `interaction_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `action` varchar(255) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `event_id` int DEFAULT NULL,
  PRIMARY KEY (`interaction_id`),
  KEY `user_id` (`user_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `user_interactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `user_interactions_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_interactions`
--

LOCK TABLES `user_interactions` WRITE;
/*!40000 ALTER TABLE `user_interactions` DISABLE KEYS */;
INSERT INTO `user_interactions` VALUES (1,1,'admin','Profile_approved','2024-10-10 23:25:12',NULL),(2,2,'HostOne','Event_created','2024-10-13 00:05:02',NULL),(3,2,'HostOne','Event_updated','2024-10-13 21:46:45',NULL),(4,1,'admin','Event_approved','2024-10-14 21:25:06',NULL),(5,1,'admin','Event_approved','2024-10-14 21:31:27',NULL),(6,3,'UserUno','Liked','2024-10-14 23:10:58',1),(7,1,'admin','User_blocked','2024-10-15 20:49:41',NULL),(8,1,'admin','User_unblocked','2024-10-15 20:50:02',NULL),(9,1,'admin','Event_approved','2024-10-16 06:20:21',NULL),(10,1,'admin','Event_approved','2024-10-16 06:31:40',NULL),(11,2,'HostOne','Event_created','2024-10-19 18:29:09',NULL),(12,2,'HostOne','Event_updated','2024-10-19 18:29:57',NULL),(13,1,'admin','Event_approved','2024-10-19 18:36:29',NULL),(14,2,'HostOne','Event_created','2024-10-20 02:42:53',NULL),(15,1,'admin','Event_approved','2024-10-20 02:43:21',NULL),(16,2,'UserUno','Refund issued for UserUno after event \'Halloween Party\' was canceled','2024-10-20 17:11:03',NULL),(17,2,'UserUno','Refund issued for UserUno after event \'Halloween Party\' was canceled','2024-10-20 17:11:03',NULL),(18,6,'HostTwo','Profile_submitted','2024-10-21 22:57:23',NULL),(19,7,'HostThree','Profile_submitted','2024-10-22 00:52:50',NULL),(20,1,'admin','Profile_approved','2024-11-01 16:24:36',NULL),(21,7,'HostThree','Event_created','2024-11-01 16:37:23',NULL),(22,7,'HostThree','Event_created','2024-11-01 16:42:52',NULL),(23,7,'HostThree','Event_updated','2024-11-01 16:43:41',NULL),(24,1,'admin','Event_approved','2024-11-01 17:01:35',NULL),(25,1,'admin','Event_approved','2024-11-01 17:01:40',NULL);
/*!40000 ALTER TABLE `user_interactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` varchar(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','pbkdf2:sha256:260000$YBOpNgUlCY5vuDbG$0fe3dbbd9f1b38a0b713ab30cfb2cfa250d93c9dea9a5a2da3afd9a87a941652','admin@example.com','Admin','2024-10-10 21:21:03','active'),(2,'HostOne','pbkdf2:sha256:260000$zJFeB6Q3ZAIqudRq$351f0cf386a0fbe7054552fdfa368d567aafb0cf4d19f298deaa170ba73855a0','userone@gmail.com','EventHost','2024-10-10 21:42:05','active'),(3,'UserUno','pbkdf2:sha256:260000$GIX20fShztcFuFNr$f2a439ea1f40922992a93643ec2face53a4ed319d8aed0cc41f2bfde43eec9bd','useruno@gmail.com','Attendee','2024-10-14 22:34:53','active'),(4,'adminKM','pbkdf2:sha256:260000$dRB97VuxiVPY73Lw$b7d3ca80c215b7feea5a534e483ce41183c9fec96b3b4f36f149276b265dac49','kora.menete@gmail.com','Admin','2024-10-16 05:06:54','active'),(5,'adminSC','pbkdf2:sha256:260000$GGGOtQZOuG12zrKl$4c08fd9755b6ffe5095b5a87198e1f6b43c458313d32acddcde6df2fc53b7a1c','schaule@yahoo.com','Admin','2024-10-16 05:23:17','active'),(6,'HostTwo','pbkdf2:sha256:260000$Uk7hKnHvXviNYoRk$b89d5b6417d9f99b40ef392adc1ce03ba17d11d0f751f93aa0981822853f68e3','hosttwo@gmail.com','EventHost','2024-10-21 21:39:06','active'),(7,'HostThree','pbkdf2:sha256:260000$elhwFpz1yXsEeFOd$0f05de231023fe1508b3de12519468beb70f93416db1ebc3b2b173d0a0a80b47','hostthree@gmail.com','EventHost','2024-10-22 00:43:39','active'),(8,'UserDuo','pbkdf2:sha256:260000$A5SpqDykFB4SfIHh$ea924b9dc4634c1a5f4bab5ba97769ea4812a20f1e76f6d3bcc557393b7f1ddd','userduo@gmail.com','Attendee','2024-11-01 17:16:05','active');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-08 18:23:51
