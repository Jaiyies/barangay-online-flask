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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `contact_number` varchar(15) DEFAULT NULL,
  `address` text,
  `role` varchar(50) DEFAULT 'resident',
  `is_verified` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (4,'Jireh','Goyon','headadmin@barangay.com','scrypt:32768:8:1$wKXNqEpT15uA1dKx$719b4990ea3170ac58aae7e693db0ef177096ee1febde5e087040b1753b248862339211268ad31fe5b98926daad7df1d3e6051ff61cb2d15de7ad7da4e2597db','09123456789','Barangay Sto. Niño, Parañaque City','head_admin',1,'2026-08-29 04:32:12'),(9,'Jireh','Goyon','jirehgoyon02@gmail.com','scrypt:32768:8:1$A0RWAOi3jhLBtC52$74ed48443eb0a0bbe1b946d5ed2979504d16518cf510eb99561ecfc1509c7fed19e626a21500c83839c44ed75950f0395bcd92c98422a2163d1d7dad7331d590','09613743567','BLK 5 LOT 12 BERNABE COMPOUND','resident',1,'2026-09-04 12:14:56'),(10,'Admin','Barangay','admin@barangay.com','scrypt:32768:8:1$Vwc4St8CdTXhke4C$2799676aef2309c4ac478a269e8f8aa0b640ec209758491c24ce9dd6b2b2acc7a49a34cdd69a97e00683f417e912ffd878d509573f745806898125785d916596','09123456788','Barangay Sto. Niño, Parañaque City','admin_documents',1,'2026-09-05 06:16:42'),(12,'Angelica Ann','Alcantara','admin1@gmail.com','scrypt:32768:8:1$syQOzSrwvyq0x0Xq$38e3eb3266f38c9efd308f156e572d0deb099ba37524c93fd11cfcc8d347859d0603397d5a93afc3b4a18d9f04e53d12db58f71e3209e5b614e8692aa622f0a1',NULL,NULL,'admin_court_1',1,'2026-09-14 09:44:34'),(13,'Jenica','Sanchez','admin2@gmail.com','scrypt:32768:8:1$O6R0z7tCPBVNTxV9$fb15623befc20fe46fcd2f7cdf0344df21333d8616dabdd5121900b1e341910c792a9977f11e05ff399930c9c947fb741c63d9c29a73b8e79e251fa47e5f0d81',NULL,NULL,'admin_court_2',1,'2026-09-22 08:51:23'),(14,'Caryll','Ybanez','admin3@gmail.com','scrypt:32768:8:1$nmmLmFRAWqQVIu95$1072e77083b59783fd2a03eb1e82b3c46e613156eca89a2c687d0af4ed94933d1dcd2a93b705b9478348ecccfb954af0715ddcf940cc776146b38cd46a8280e3',NULL,NULL,'admin_court_3',1,'2026-09-22 14:20:38'),(15,'Kristine Joy','Oliva','admin4@gmail.com','scrypt:32768:8:1$9jo5UdfuAD35Hg0O$7f8bcfefdcfa7e16dca840cc44500963df684bd506978a9dd82630d422e98c327374655af5390cf879a447903af71887c0b065587dbae358a449c701d3db1709',NULL,NULL,'admin_court_4',1,'2026-09-22 14:27:19');
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

-- Dump completed on 2026-09-23 18:29:21
