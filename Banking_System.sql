-- Create the database if it doesn't exist, using utf8mb4 character set and collation
CREATE DATABASE IF NOT EXISTS `banking_system`
    /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */
    /*!80016 DEFAULT ENCRYPTION='N' */;

-- Use the newly created database
USE `banking_system`;

-- Set the session variables for character set and timezone handling
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;

-- Disable unique and foreign key checks temporarily to prevent issues during data insertion
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Table structure for `login` table
DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
    `user_id` INT NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`user_id`),
    CONSTRAINT `login_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting sample data into the `login` table
LOCK TABLES `login` WRITE;
INSERT INTO `login` (`user_id`, `password`) 
VALUES 
    (1, 'Shreya@123'), 
    (2, 'Ram@123'), 
    (3, 'Baanu@5101990');
UNLOCK TABLES;

-- Table structure for `transaction` table
DROP TABLE IF EXISTS `transaction`;

CREATE TABLE `transaction` (
    `transaction_id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `type` VARCHAR(50) DEFAULT NULL,
    `amount` DECIMAL(10, 2) DEFAULT NULL,
    `date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`transaction_id`),
    KEY `user_id` (`user_id`),
    CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting sample data into the `transaction` table
LOCK TABLES `transaction` WRITE;
INSERT INTO `transaction` (`transaction_id`, `user_id`, `type`, `amount`, `date`) 
VALUES 
    (1, 2, 'Transfer Out', 500.00, '2024-12-27 17:50:51'), 
    (2, 1, 'Transfer In', 500.00, '2024-12-27 17:50:51');
UNLOCK TABLES;

-- Table structure for `users` table
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `account_number` VARCHAR(10) NOT NULL,
    `dob` DATE DEFAULT NULL,
    `city` VARCHAR(255) DEFAULT NULL,
    `contact_number` VARCHAR(15) DEFAULT NULL,
    `email` VARCHAR(255) DEFAULT NULL,
    `address` TEXT DEFAULT NULL,
    `balance` DECIMAL(10, 2) NOT NULL,
    `status` VARCHAR(10) DEFAULT 'Active',
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `account_number` (`account_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting sample data into the `users` table
LOCK TABLES `users` WRITE;
INSERT INTO `users` (`user_id`, `name`, `account_number`, `dob`, `city`, `contact_number`, `email`, `address`, `balance`, `status`) 
VALUES 
    (1, 'Shreya', '1132576048', '2004-11-06', 'Rewa', '9039107855', 'shreya@gmail.com', 'patel Nagar', 3000.00, 'Active'), 
    (2, 'Ram', '7525977446', '2000-10-10', 'Ujjain', '9868357918', 'Ram@123gmail.com', 'Jai Mahakal', 2500.00, 'Deactive'), 
    (3, 'Baanu', '4788599145', '1990-10-05', 'Panvel', '9039561856', 'baanu5@gmail.com', 'saket Nagar', 50000.00, 'Active');
UNLOCK TABLES;

-- Revert back to original session settings
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
 /*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
 /*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
 /*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
 /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
 /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
 /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
 /*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
