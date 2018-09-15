-- phpMyAdmin SQL Dump
-- version 4.6.6deb4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 21, 2018 at 11:24 AM
-- Server version: 10.1.23-MariaDB-9+deb9u1
-- PHP Version: 7.0.30-0+deb9u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Dados`
--

-- --------------------------------------------------------

--
-- Table structure for table `Configuracao`
--

CREATE TABLE `Configuracao` (
  `id` int(7) NOT NULL,
  `confiabilidade` float DEFAULT NULL,
  `tempo_processo` float DEFAULT NULL,
  `tempo_gravacao` float DEFAULT NULL,
  `num_tentativas` int(11) DEFAULT NULL,
  `modo` int(11) DEFAULT NULL,
  `recalibracao` tinyint(1) DEFAULT NULL,
  `carroMin` int(11) DEFAULT NULL,
  `carroMax` int(11) DEFAULT NULL,
  `motoMin` int(11) DEFAULT NULL,
  `motoMax` int(11) DEFAULT NULL,
  `caminhaoMin` int(11) DEFAULT NULL,
  `up` int(1) DEFAULT NULL,
  `data` datetime DEFAULT NULL,
  `data2` varchar(25) DEFAULT NULL,
  `equipamento` int(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Equipamento`
--

CREATE TABLE `Equipamento` (
  `id` int(11) NOT NULL,
  `nome` varchar(7) NOT NULL,
  `descricao` text NOT NULL,
  `cod_estacionamento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Estacionamento`
--

CREATE TABLE `Estacionamento` (
  `id` int(11) NOT NULL,
  `nome` varchar(7) NOT NULL,
  `descricao` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Registro`
--

CREATE TABLE `Registro` (
  `id` int(11) NOT NULL,
  `data` datetime DEFAULT NULL,
  `tipo_entrada` int(1) DEFAULT NULL,
  `tipo_vei` varchar(20) DEFAULT NULL,
  `placa` varchar(7) DEFAULT NULL,
  `processado` int(1) DEFAULT NULL,
  `id_foto` varchar(45) DEFAULT NULL,
  `foto` longblob,
  `equipamento` int(11) DEFAULT NULL,
  `estacionamento` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Removidos`
--

CREATE TABLE `Removidos` (
  `id` int(11) NOT NULL,
  `nome` varchar(7) NOT NULL,
  `descricao` text NOT NULL,
  `cod_estacionamento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Usuario`
--

CREATE TABLE `Usuario` (
  `nome` varchar(15) NOT NULL,
  `nivel` int(1) NOT NULL,
  `senha` varchar(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Configuracao`
--
ALTER TABLE `Configuracao`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Registro`
--
ALTER TABLE `Registro`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Configuracao`
--
ALTER TABLE `Configuracao`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `Registro`
--
ALTER TABLE `Registro`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
