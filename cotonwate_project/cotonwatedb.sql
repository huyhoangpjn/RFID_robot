-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : dim. 11 déc. 2022 à 12:11
-- Version du serveur : 5.7.40
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `cotonwatedb`
--

-- --------------------------------------------------------

--
-- Structure de la table `vetements`
--

DROP TABLE IF EXISTS `vetements`;
CREATE TABLE IF NOT EXISTS `vetements` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NUID` varchar(30) NOT NULL,
  `intitule` varchar(100) NOT NULL,
  `couleur` varchar(100) NOT NULL,
  `taille` varchar(30) NOT NULL,
  `marque` varchar(100) NOT NULL,
  `prix` int(11) NOT NULL,
  `enStock` varchar(30) NOT NULL DEFAULT 'oui',
  `date_ajout` date NOT NULL,
  `date_modif` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `vetements`
--

INSERT INTO `vetements` (`id`, `NUID`, `intitule`, `couleur`, `taille`, `marque`, `prix`, `enStock`, `date_ajout`, `date_modif`) VALUES
(1, 'test', 'test', 'update', 'test', 'test', 50, 'non', '2022-12-01', '2022-12-06');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
