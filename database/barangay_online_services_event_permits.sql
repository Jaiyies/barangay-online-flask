-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: barangay_online_services
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `event_permits`
--

DROP TABLE IF EXISTS `event_permits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_permits` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `event_name` varchar(255) NOT NULL,
  `event_description` text,
  `event_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time DEFAULT NULL,
  `estimated_attendees` int DEFAULT '0',
  `venue` varchar(255) DEFAULT NULL,
  `status` enum('pending','reviewing','approved','rejected') DEFAULT 'pending',
  `requirements_file` varchar(255) DEFAULT NULL,
  `admin_remarks` text,
  `applied_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `approved_at` timestamp NULL DEFAULT NULL,
  `requested_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `reference_number` varchar(50) DEFAULT NULL,
  `queuing_number` varchar(20) DEFAULT NULL,
  `purpose` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `contact_person` varchar(255) DEFAULT NULL,
  `contact_phone` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `event_permits_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_permits`
--

LOCK TABLES `event_permits` WRITE;
/*!40000 ALTER TABLE `event_permits` DISABLE KEYS */;
INSERT INTO `event_permits` VALUES (1,9,'baskte','yohoo','2026-09-30','10:00:00','15:00:00',88,'Sto.Niño Sports Complex','pending','G2_CV.pdf (1).png',NULL,'2026-09-09 11:28:07',NULL,'2026-09-09 11:28:07','BP-20260909-5980','Q-775','123','2026-09-21 03:54:26',NULL,NULL),(2,9,'baskte','yohooo','2026-10-08','10:00:00','17:00:00',194,'Sto.Niño Basketball Court','pending','admin-structure.pdf',NULL,'2026-09-09 11:32:52',NULL,'2026-09-09 11:32:52','BP-20260909-1896','Q-541','adnamnla','2026-09-21 03:54:26',NULL,NULL),(3,9,'baskte','yohooo','2026-10-08','10:00:00','17:00:00',194,'Sto.Niño Basketball Court','pending','admin-structure.pdf',NULL,'2026-09-09 11:42:10',NULL,'2026-09-09 11:42:10','BP-20260909-1866','Q-273','adnamnla','2026-09-21 03:54:26',NULL,NULL),(4,9,'baskte','YOHOO','2026-10-11','10:00:00','15:00:00',281,'Sto.Niño Sports Complex','pending','799439823_1619295619801934_3031222376199053929_n.png',NULL,'2026-09-09 11:42:47',NULL,'2026-09-09 11:42:47','BP-20260909-3717','Q-116','YOHOO','2026-09-21 03:54:26',NULL,NULL),(5,9,'baskte','YOHO','2026-10-04','10:00:00','15:00:00',281,'Sto.Niño Sports Complex','pending','794292844_1607965414321037_7667161609149147542_n.jpg',NULL,'2026-09-09 11:48:30',NULL,'2026-09-09 11:48:30','BP-20260909-8585','Q-466','YOHO','2026-09-21 03:54:26',NULL,NULL),(6,9,'basketball tournament','basketball play','2026-10-11','10:00:00','16:00:00',84,'Sto.Niño Sports Complex','pending','ATM.jpg',NULL,'2026-09-09 12:05:45',NULL,'2026-09-09 12:05:45','BP-20260909-8568','Q-293','play','2026-09-21 03:54:26',NULL,NULL),(7,9,'basketball tournament','basketball','2026-10-11','10:00:00','16:03:00',100,'Sto.Niño Sports Complex','pending','SIG.jpg',NULL,'2026-09-14 10:40:19',NULL,'2026-09-14 10:40:19','BP-20260914-6501','Q-023','basketball','2026-09-21 03:54:26',NULL,NULL),(8,9,'basketball tournament','basketball test','2026-10-02','08:00:00','22:00:00',185,'Sto. Nino Sports Complex','pending','GOYON.pdf',NULL,'2026-09-22 15:05:05',NULL,'2026-09-22 15:05:05','BP-20260922-6119','Q-716','basketball liga','2026-09-22 15:05:05',NULL,NULL),(9,9,'zumba dance','zumba tournament','2026-10-10','10:00:00','13:00:00',78,'Sto. Nino Sports Complex','approved','mermaid-diagram (2).png','','2026-09-22 15:22:43',NULL,'2026-09-22 15:22:43','BP-20260922-6667','Q-536','zumba dance tournament','2026-09-22 15:22:43',NULL,NULL),(10,9,'zumba dance','zumba tournament','2026-10-10','10:00:00','13:00:00',78,'Sto. Nino Sports Complex','pending','mermaid-diagram (2).png',NULL,'2026-09-22 15:26:02',NULL,'2026-09-22 15:26:02','BP-20260922-2071','Q-048','zumba dance tournament','2026-09-22 15:26:02',NULL,NULL);
/*!40000 ALTER TABLE `event_permits` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-23 18:29:21
