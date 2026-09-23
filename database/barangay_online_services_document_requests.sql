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
-- Table structure for table `document_requests`
--

DROP TABLE IF EXISTS `document_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `document_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `document_type` varchar(50) NOT NULL,
  `surname` varchar(100) NOT NULL,
  `given_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `address` text NOT NULL,
  `contact_no` varchar(20) NOT NULL,
  `civil_status` varchar(50) NOT NULL,
  `age` int NOT NULL,
  `dob` date NOT NULL,
  `precinct_no` varchar(50) NOT NULL,
  `place_of_birth` varchar(100) NOT NULL,
  `length_of_stay` varchar(50) NOT NULL,
  `residency_type` varchar(50) NOT NULL,
  `lessor_name` varchar(100) NOT NULL,
  `lessor_address` text NOT NULL,
  `rep_position` varchar(100) DEFAULT NULL,
  `father_name` varchar(100) NOT NULL,
  `mother_name` varchar(100) NOT NULL,
  `spouse_name` varchar(100) DEFAULT NULL,
  `occupation` varchar(100) NOT NULL,
  `emergency_name` varchar(100) NOT NULL,
  `emergency_number` varchar(20) NOT NULL,
  `ref1_name` varchar(100) NOT NULL,
  `ref1_address` text NOT NULL,
  `ref2_name` varchar(100) NOT NULL,
  `ref2_address` text NOT NULL,
  `purpose` text NOT NULL,
  `printed_name` varchar(100) NOT NULL,
  `signature_date` date NOT NULL,
  `reference_number` varchar(50) NOT NULL,
  `queuing_number` varchar(20) DEFAULT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `admin_remarks` text,
  `document_path` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reference_number` (`reference_number`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `document_requests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document_requests`
--

LOCK TABLES `document_requests` WRITE;
/*!40000 ALTER TABLE `document_requests` DISABLE KEYS */;
INSERT INTO `document_requests` VALUES (1,9,'indigency','GOYON','JIREH','BALASA','BLK 5 LOT 12 BERNABE COMPOUND','09613843567','Married',21,'2005-09-02','123-456-789','LPC','10 YEARS','Owner','JIREH','BLOCK 5','','ANTHONY','JOY','KYLE','YOHOO','1234567891','12345678901','JIREH','LPC','KYLE','LPC','JAIRAH','JAIRAH','2026-09-07','DOC-20260907-4898','Q-196','pending',NULL,NULL,'2026-09-07 12:41:24','2026-09-07 12:41:24'),(2,9,'proof_residency','SANCHEZ','JENICA','C','MUNTINLUPA CITY','09613843598','Widowed',21,'2004-10-07','123-4567','MUNTINLUPA CITY','10 YEARS','Owner','JENICA','MUNTINLUPA CITY','sk_chairman','JULIUS SANCHEZ','LEONIDA SANCHEZ','',' MANAGER','LEONIDA SANCHEZ','12345678901','MUNTINLUPA CITY','MUNTINLUPA CITY','MUNTINLUPA CITY','MUNTINLUPA CITY','proof or residency','JENICA SANCHEZ','2026-09-14','DOC-20260914-9527','Q-632','approved','','pacute.jpg','2026-09-14 05:40:01','2026-09-14 09:06:54'),(3,9,'indigency','Oliva','Kristine Joy','I','paranaque city','09613843598','Separated',21,'2005-05-10','123-4567','LPC','10 YEARS','Renter','kristine joy oliva','paranaque city','','Angelica ann Alcantara','Jenica Sanchez','ash batumbakal jr','cook','LEONIDA SANCHEZ','12345678901','caryll ybanez','paranaque city','jireh goyon','imus cavite','for fun','kristine joy oliva','2026-09-23','DOC-20260923-2622','Q-001','pending',NULL,NULL,'2026-09-23 08:08:06','2026-09-23 08:08:06'),(4,9,'clearance','Jenica ','Bughaw','C','Muntinlupa city','09260093242','Married',20,'2005-10-20','123-4589','MUNTINLUPA CITY','10 YEARS','Owner','JENICA SANCHEZ','MUNTINLUPA CITY','','julius sanchez','leonida sanchez','karl benjamin bughaw','linux god','Michael Jordan','12345678901','caryll ybanez','paranaque city','jireh goyon','LPC','para sa cenomar','JENICA SANCHEZ','2026-09-23','DOC-20260923-5653','Q-002','pending',NULL,NULL,'2026-09-23 08:13:11','2026-09-23 08:13:11');
/*!40000 ALTER TABLE `document_requests` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-23 18:29:20
