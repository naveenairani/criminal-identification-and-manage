-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 04, 2023 at 07:17 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `criminaldb`
--

-- --------------------------------------------------------

--
-- Table structure for table `criminaldata`
--

CREATE TABLE `criminaldata` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `father name` varchar(25) DEFAULT NULL,
  `mother name` varchar(25) DEFAULT NULL,
  `gender` varchar(6) NOT NULL,
  `dob` varchar(10) DEFAULT NULL,
  `blood group` varchar(5) DEFAULT NULL,
  `identity mark` varchar(30) NOT NULL,
  `nationality` varchar(15) NOT NULL,
  `religion` varchar(15) NOT NULL,
  `crimes_done` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `criminaldata`
--

INSERT INTO `criminaldata` (`id`, `name`, `father name`, `mother name`, `gender`, `dob`, `blood group`, `identity mark`, `nationality`, `religion`, `crimes`) VALUES
(3, 'vijay mallya', 'vittal  mallya', 'lalitha mallya', 'male', '1955-12-18', 'b+', 'white hair', 'india', 'brahmin hindu', 'money laundering'),
(4, 'osama bin laden', 'mohammed bin awad bin lad', 'alia ghanem', 'male', '1957-03-10', 'o -ve', 'black beard', 'saudi', 'muslim', 'murder,attacks'),
(6, 'dawood ibrahim', 'ibrahim kaskar', 'amina bi', 'male', '1955-12-26', 'ab+', 'black coat', 'india', 'konkani muslim', 'gold smuggling,extortion,drug trafficing');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `criminaldata`
--
ALTER TABLE `criminaldata`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `criminaldata`
--
ALTER TABLE `criminaldata`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
