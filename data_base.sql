/*
SQLyog Enterprise - MySQL GUI v8.02 RC
MySQL - 5.5.5-10.3.16-MariaDB : Database - pyproject
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`pyproject` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `pyproject`;

/*Table structure for table `admindata` */

DROP TABLE IF EXISTS `admindata`;

CREATE TABLE `admindata` (
  `name` varchar(100) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `mobileno` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `admindata` */

insert  into `admindata`(`name`,`department`,`address`,`mobileno`,`email`) values ('admin','cse','Pathankot','9888442233','admin@gmail.com');

/*Table structure for table `feesdata` */

DROP TABLE IF EXISTS `feesdata`;

CREATE TABLE `feesdata` (
  `name` varchar(100) DEFAULT NULL,
  `roll_no` varchar(100) DEFAULT NULL,
  `branch` varchar(100) DEFAULT NULL,
  `mobile_no` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `acc_no` varchar(100) DEFAULT NULL,
  `transfer_to` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `feesdata` */

insert  into `feesdata`(`name`,`roll_no`,`branch`,`mobile_no`,`email`,`amount`,`acc_no`,`transfer_to`) values ('student','1000','cse','9876543210','student@gmail.com','47000','859034895849','349048932840809'),('vikram','1222','cse','8934893289489','vikram@gmail.com','50000','4789327842897','37487238478927');

/*Table structure for table `logindata` */

DROP TABLE IF EXISTS `logindata`;

CREATE TABLE `logindata` (
  `userid` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `logindata` */

insert  into `logindata`(`userid`,`password`,`usertype`) values ('admin@gmail.com','admin','admin'),('karan@gmail.com','300','student'),('manpreet@gmail.com','manpreet','student'),('shagun@gmail.com','shagun','student'),('student@gmail.com','student','student'),('Vikram@gmail.com','300','student');

/*Table structure for table `photodata` */

DROP TABLE IF EXISTS `photodata`;

CREATE TABLE `photodata` (
  `userid` varchar(100) NOT NULL,
  `photoname` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `photodata` */

insert  into `photodata`(`userid`,`photoname`) values ('student@gmail.com','1592495316.jpg');

/*Table structure for table `questiondata` */

DROP TABLE IF EXISTS `questiondata`;

CREATE TABLE `questiondata` (
  `q_id` int(11) NOT NULL AUTO_INCREMENT,
  `question` text DEFAULT NULL,
  `question_date` varchar(100) DEFAULT NULL,
  `subject` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `roll_no` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`q_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `questiondata` */

insert  into `questiondata`(`q_id`,`question`,`question_date`,`subject`,`name`,`roll_no`,`email`) values (3,'what is Trignometry ?','1587220249','math','student','1108','student@gmail.com'),(4,'What is software ?','1587223631','computer science','karan','1212','karan@gmail.com'),(5,'What is physics?','1587896626','physics','Manpreet','1121','manpreet@gmail.com'),(6,'national bird of india ?','1587896779','gk','Manpreet','1121','manpreet@gmail.com'),(7,'How are you ?','1587977229','testing','vikram','1111','vikram@gmail.com');

/*Table structure for table `solutiondata` */

DROP TABLE IF EXISTS `solutiondata`;

CREATE TABLE `solutiondata` (
  `s_id` int(11) NOT NULL AUTO_INCREMENT,
  `q_id` int(100) DEFAULT NULL,
  `solution` text DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `question` text DEFAULT NULL,
  PRIMARY KEY (`s_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;

/*Data for the table `solutiondata` */

insert  into `solutiondata`(`s_id`,`q_id`,`solution`,`name`,`question`) values (14,4,'by vikram','vikram','What is software ?'),(15,3,'by vikram','vikram','what is Trignometry ?'),(16,4,'by student','student','What is software ?'),(17,5,'by manpreet','vikram','What is physics?'),(18,6,'by manpreet','vikram','national bird of india ?'),(19,4,'by manpreet','vikram','What is software ?'),(20,3,'by manpreet','vikram','what is Trignometry ?');

/*Table structure for table `studentdata` */

DROP TABLE IF EXISTS `studentdata`;

CREATE TABLE `studentdata` (
  `name` varchar(100) DEFAULT NULL,
  `rollno` varchar(100) DEFAULT NULL,
  `branch` varchar(100) DEFAULT NULL,
  `year` varchar(100) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `mobileno` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `studentdata` */

insert  into `studentdata`(`name`,`rollno`,`branch`,`year`,`address`,`mobileno`,`email`) values ('karan','1212','cse','3rd','jalander','9800000000','karan@gmail.com'),('Manpreet','1121','cse','3rd','Mukerian','9876543210','manpreet@gmail.com'),('Shagun','1123','cse','3rd','Himachal','9876512340','shagun@gmail.com'),('student','1108','cse','2017','Pathankot','9888709028','student@gmail.com'),('vikram','1111','cse','4th','madhopur','9888709028','Vikram@gmail.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
