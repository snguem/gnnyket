-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 30, 2024 at 12:53 PM
-- Server version: 5.7.36
-- PHP Version: 8.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gnnyket`
--

-- --------------------------------------------------------

--
-- Table structure for table `commande`
--

DROP TABLE IF EXISTS `commande`;
CREATE TABLE IF NOT EXISTS `commande` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ref` varchar(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `montant` float DEFAULT NULL,
  `heure` int(20) DEFAULT NULL,
  `montant_paye` float DEFAULT NULL,
  `client` int(11) NOT NULL,
  `etat` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `ref` (`ref`),
  KEY `client` (`client`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `commande`
--

INSERT INTO `commande` (`id`, `ref`, `date`, `montant`, `heure`, `montant_paye`, `client`, `etat`) VALUES
(32, 'CMD00032', '2024-05-24', 68000, 753, 68000, 22, 2),
(31, 'CMD00031', '2024-05-22', 2500, 1027, 2500, 1, 1),
(30, 'CMD00030', '2024-05-22', 152000, 986, 152000, 21, 0),
(29, 'CMD00029', '2024-05-22', 36000, 875, 36000, 20, 0),
(28, 'CMD00028', '2024-05-22', 12000, 872, 12000, 20, 0),
(27, 'CMD00027', '2024-05-22', 58000, 867, 58000, 17, 2);

-- --------------------------------------------------------

--
-- Table structure for table `coupon`
--

DROP TABLE IF EXISTS `coupon`;
CREATE TABLE IF NOT EXISTS `coupon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(11) DEFAULT NULL,
  `date_crea` date DEFAULT NULL,
  `date_exp` date DEFAULT NULL,
  `reduction` float DEFAULT NULL,
  `etat` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
CREATE TABLE IF NOT EXISTS `notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(1000) DEFAULT NULL,
  `type` int(1) DEFAULT NULL,
  `action` varchar(100) DEFAULT NULL,
  `nom` varchar(30) DEFAULT NULL,
  `prenom` varchar(30) DEFAULT NULL,
  `contact` varchar(20) DEFAULT NULL,
  `mail` varchar(40) DEFAULT NULL,
  `adresse` varchar(30) DEFAULT NULL,
  `sujet` varchar(30) DEFAULT NULL,
  `etat` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`id`, `message`, `type`, `action`, `nom`, `prenom`, `contact`, `mail`, `adresse`, `sujet`, `etat`) VALUES
(29, NULL, 2, '/commandes/details/CMD00031', 'NGUEMA', 'Steeve', '771479603', 'snguemaabesolo@ism.edu.sn', 'Ouakam, comico', NULL, 1),
(28, 'salut !', 1, NULL, 'Nguema', 'steeve', NULL, 'steeve@gmail.com', NULL, 'salutation', 2),
(27, NULL, 2, '/commandes/details/CMD00030', 'Nguema', 'steeve', '781478704', 'steeve@gmail.com', 'comico', NULL, 1),
(26, NULL, 2, '/commandes/details/CMD00029', 'Bibaghan Louetsi ', 'Hulda Sagesse', '776544553', 'huldasagesse@ism.edu.sn', 'pentola, senegal', NULL, 1),
(25, NULL, 2, '/commandes/details/CMD00028', 'Bibaghan Louetsi ', 'Hulda Sagesse', '776544553', 'huldasagesse@ism.edu.sn', 'pentola, senegal', NULL, 1),
(24, NULL, 2, '/commandes/details/CMD00027', 'DUBOIS', 'Richard Antoine', '765432343', 'richarddubois2@gmail.com', 'Saly, Senegal', NULL, 2),
(30, NULL, 2, '/commandes/details/CMD00032', 'tt', 'yy', '7814799603', 'melda@ism.edu.sn', 'gg', NULL, 2),
(23, 'je viens de consulter la liste de produit et il n\'y en a aucun. Comment faire pour passer commande?', 1, NULL, 'DUBOIS', 'Richard Antoine', NULL, 'richarddubois2@gmail.com', NULL, 'informatoin', 1);

-- --------------------------------------------------------

--
-- Table structure for table `produit`
--

DROP TABLE IF EXISTS `produit`;
CREATE TABLE IF NOT EXISTS `produit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(1000) DEFAULT NULL,
  `libelle` varchar(30) DEFAULT NULL,
  `qte_stock` int(10) DEFAULT NULL,
  `qte_cmde` int(10) DEFAULT NULL,
  `categorie` varchar(50) DEFAULT NULL,
  `type_produit` int(11) NOT NULL,
  `prix` float DEFAULT NULL,
  `taille` varchar(10) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `etat` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `type_produit` (`type_produit`)
) ENGINE=MyISAM AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `produit`
--

INSERT INTO `produit` (`id`, `img`, `libelle`, `qte_stock`, `qte_cmde`, `categorie`, `type_produit`, `prix`, `taille`, `description`, `etat`) VALUES
(18, 'img/produits/prod0000000018.jpeg', 'Horo-horo', 50, 0, 'enfant', 37, 7000, 'medium', 'Horo-horo est la montre qui te permet de savoir quand il est l\'heure de faire des choses amusantes.', 1),
(17, 'img/produits/prod0000000017.jpeg', 'Supreme med', 20, 0, 'mixte', 37, 15000, 'medium', 'Suprem Med, un bijou de technologie et d\'élégance. Son design épuré et raffiné cache un mouvement suisse de précision, garant d\'une fiabilité absolue.', 1),
(16, 'img/produits/prod0000000016.jpeg', 'Nexus Synchro', 10, 0, 'mixte', 37, 15000, 'large', 'La Nexus Synchro, c\'est plus qu\'une montre, c\'est une extension de votre rythme. Son design minimaliste et élégant s\'harmonise parfaitement avec votre', 1),
(15, 'img/produits/prod0000000015.jpeg', 'couple royal', 21, 0, 'mixte', 37, 12000, 'small', 'Imaginez une montre qui incarne à la fois l\'élégance intemporelle et le dynamisme moderne. Cette montre mixte, avec son design audacieux et ses détail', 1),
(19, 'img/produits/prod0000000019.jpeg', 'Tempo', 30, 0, 'enfant', 37, 7500, 'medium', 'Tempo est ta montre préférée ! Elle est simple, pratique et t\'aide à organiser ton temps.', 1),
(20, 'img/produits/prod0000000020.jpeg', 'Hiri', 30, 0, 'enfant', 37, 5000, 'small', 'Avec Hiri, chaque heure est une heure de bonheur ! Elle a des aiguilles colorées et un design rigolo qui te met de bonne humeur.', 1),
(21, 'img/produits/prod0000000021.jpeg', 'Emperor', 20, 0, 'enfant', 37, 10000, 'small', 'Emperor est la montre des champions ! Elle te montre le chemin du succès et te permet de gérer ton temps avec précision. Elle te donne le po', 1),
(22, 'img/produits/prod0000000022.jpeg', 'Luna', 20, 0, 'femme', 37, 17000, 'medium', 'Une montre élégante et féminine, avec un cadran blanc et un bracelet en or rose. Elle représente la beauté et la féminité.', 1),
(23, 'img/produits/prod0000000023.jpeg', 'Zenith', 18, 0, 'femme', 37, 21000, 'small', 'Une montre sophistiquée et minimaliste, avec un cadran orne et un bracelet en métal brossé. Elle incarne la femme puissante et ambitieuse', 1),
(24, 'img/produits/prod0000000024.jpeg', 'Héritage', 10, 1, 'homme', 37, 23000, 'small', 'Une montre élégante et intemporelle, avec un cadran argenté et un bracelet en cuir brun foncé. Elle représente un homme raffiné et au goût sûr.', 1),
(25, 'img/produits/prod0000000025.jpeg', 'Chronographe', 20, 0, 'homme', 37, 25000, 'small', 'Un modèle chic et fonctionnel, avec un cadran en argent et des complications chronographiques. Elle est idéale pour les hommes qui aiment les montres', 1),
(26, 'img/produits/prod0000000026.jpeg', 'Éclipse', 17, 0, 'homme', 37, 20000, 'small', 'Une montre futuriste avec un cadran bleu profond et des détails en acier inoxydable. Elle incarne un style avant-gardiste et se distingue par sa moder', 1),
(27, 'img/produits/prod0000000027.jpeg', 'Ruft', 10, 2, 'homme', 41, 32000, 'small', 'Des chaussures en cuir à lacets, au style classique et moderne, parfaites pour les occasions formelles et décontractées. Elles incarnent l\'homme qui m', 1),
(28, 'img/produits/prod0000000028.jpeg', 'Élégance', 15, 1, 'homme', 41, 35000, 'large', 'Des chaussures en cuir noir verni, au style classique et raffiné. Elles incarnent l\'homme élégant et sophistiqué, qui aime les valeurs traditionnelles', 1),
(29, 'img/produits/prod0000000029.jpeg', 'Force Intérieure', 30, 0, 'femme', 41, 15000, 'small', 'Un cuir robuste et des détails en métal évoquent la force et la détermination, symbolisant une femme qui ne se laisse pas intimider.', 1),
(30, 'img/produits/prod0000000030.jpeg', 'Douceur du Vent:', 10, 3, 'femme', 41, 12000, 'small', 'Le cuir souple et léger de ces chaussures évoque la sensation du vent sur la peau, symbolisant une femme qui apprécie la liberté et la légèreté.', 0),
(31, 'img/produits/prod0000000031.jpeg', 'Sable Chaud', 20, 0, 'femme', 44, 8497, 'small', 'Des tons chauds et naturels rappellent le sable chaud sous les pieds, incarnant une femme qui aime la nature et les voyages.', 0),
(32, 'img/produits/prod0000000032.png', 'L\'Écho du Cœur', 23, 0, 'femme', 44, 16000, 'medium', 'Des détails en dentelle et une touche de blanche évoquent le mystère et la purete, symbolisant une femme qui a la maitre de soi.', 0),
(33, 'img/produits/prod0000000033.jpeg', 'Équilibre Harmonieux', 31, 0, 'mixte', 41, 14000, 'large', 'Des chaussures minimalistes avec des lignes épurées et des matériaux naturels. Elles incarnent l\'équilibre entre le corps et l\'esprit, la connexion av', 1),
(34, 'img/produits/prod0000000034.jpeg', 'Toiles Rebelles', 20, 0, 'mixte', 41, 13500, 'small', 'Des chaussures à lacets avec des imprimés audacieux et des couleurs vibrantes. Elles s\'adressent aux créatifs et aux rebelles qui osent se démarquer e', 1),
(35, 'img/produits/prod0000000035.png', 'Pas de Géant', 30, 2, 'enfant', 41, 2000, 'large', 'Des chaussures robustes avec des semelles épaisses et des matériaux durables. Elles offrent un maximum de protection et de confort pour les aventures', 1),
(36, 'img/produits/prod0000000036.jpeg', 'Sentier paisible', 15, 1, 'enfant', 41, 2500, 'small', 'Des chaussures de randonnée légères avec des semelles crantées pour une meilleure adhérence.', 1);

-- --------------------------------------------------------

--
-- Table structure for table `type_produit`
--

DROP TABLE IF EXISTS `type_produit`;
CREATE TABLE IF NOT EXISTS `type_produit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ref` varchar(11) DEFAULT NULL,
  `libelle` varchar(50) DEFAULT NULL,
  `etat` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `ref` (`ref`),
  UNIQUE KEY `libelle` (`libelle`)
) ENGINE=MyISAM AUTO_INCREMENT=45 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `type_produit`
--

INSERT INTO `type_produit` (`id`, `ref`, `libelle`, `etat`) VALUES
(41, 'TYPE00041', 'chaussure', 1),
(42, 'TYPE00042', 'sac a main', 1),
(37, 'TYPE00037', 'montres', 1),
(38, 'TYPE00038', 'pantalon court', 1),
(39, 'TYPE00039', 'robe', 1),
(40, 'TYPE00040', 'costume', 1);

-- --------------------------------------------------------

--
-- Table structure for table `unecommandeproduit`
--

DROP TABLE IF EXISTS `unecommandeproduit`;
CREATE TABLE IF NOT EXISTS `unecommandeproduit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `montant` float DEFAULT NULL,
  `produit` int(11) DEFAULT NULL,
  `commande` int(11) DEFAULT NULL,
  `qte` int(11) DEFAULT NULL,
  `etat` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `produit` (`produit`),
  KEY `commande` (`commande`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `unecommandeproduit`
--

INSERT INTO `unecommandeproduit` (`id`, `montant`, `produit`, `commande`, `qte`, `etat`) VALUES
(23, 4000, 35, 32, 2, 1),
(22, 64000, 27, 32, 2, 1),
(21, 2500, 36, 31, 1, 1),
(20, 27000, 34, 30, 2, 1),
(19, 125000, 25, 30, 5, 1),
(18, 36000, 30, 29, 3, 1),
(17, 12000, 30, 28, 1, 1),
(16, 35000, 28, 27, 1, 1),
(15, 23000, 24, 27, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(30) DEFAULT NULL,
  `prenom` varchar(30) DEFAULT NULL,
  `adresse` varchar(40) DEFAULT NULL,
  `contact` varchar(11) DEFAULT NULL,
  `mail` varchar(30) DEFAULT NULL,
  `profil` varchar(1000) DEFAULT NULL,
  `role` int(1) DEFAULT NULL,
  `password` varchar(100) DEFAULT 'Gnny@Password',
  `etat` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `contact` (`contact`),
  UNIQUE KEY `mail` (`mail`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `nom`, `prenom`, `adresse`, `contact`, `mail`, `profil`, `role`, `password`, `etat`) VALUES
(1, 'NGUEMA', 'Steeve', 'Ouakam, comico', '771479603', 'snguemaabesolo@ism.edu.sn', 'img/profiler/771479603.png', 0, 'steeve42', 1),
(22, 'tt', 'yy', 'gg', '7814799603', 'melda@ism.edu.sn', 'img/user_default.png', 2, 'Gnny@Passer', 0),
(21, 'Nguema', 'steeve', 'comico', '781478704', 'steeve@gmail.com', 'img/profiler/781478704.jpeg', 2, 'steeve345', 1),
(20, 'Bibaghan Louetsi ', 'Hulda Sagesse', 'pentola, senegal', '776544553', 'huldasagesse@ism.edu.sn', 'img/user_default.png', 2, 'huldahulda', 1),
(19, 'Mbaye', 'Omar', 'Liberte 6, senegal', '765432341', 'mbayeo34@gmail.com', 'img/user_default.png', 1, 'Gnny@Password', 0),
(18, 'ONDO ONDO', 'Giscard', 'point e, Senegal', '781345463', 'ondog1@gmail.com', 'img/user_default.png', 1, 'Gnny@Password', 1),
(17, 'DUBOIS', 'Richard Antoine', 'Saly, Senegal', '765432343', 'richarddubois2@gmail.com', 'img/profiler/765432343.jpeg', 2, 'dubois123', 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
