-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : ven. 13 déc. 2024 à 14:44
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `budget_ai`
--

-- --------------------------------------------------------

--
-- Structure de la table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `montant` decimal(10,2) NOT NULL,
  `type` enum('Revenu','Dépense') NOT NULL,
  `date` date NOT NULL,
  `categorie` varchar(255) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `transactions`
--

INSERT INTO `transactions` (`id`, `montant`, `type`, `date`, `categorie`, `user_id`) VALUES
(1, 500.00, 'Revenu', '2024-12-06', 'Salaire', 1),
(2, 200.00, 'Dépense', '2024-12-20', 'Loisir', 1),
(3, 1000.00, 'Revenu', '2024-12-07', 'Salaire', 1),
(4, 75.00, 'Dépense', '2024-12-29', 'Transport', 1),
(5, 900.00, 'Dépense', '2024-12-01', 'Loyer', 3),
(6, 12000.00, 'Revenu', '2024-12-03', 'Salaire', 3),
(7, 1223.00, 'Dépense', '2024-12-29', 'Transport', 1);

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mdp` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `nom`, `email`, `mdp`) VALUES
(1, '', 'mamadousanogo352@gmail.com', '$2y$10$jW4u9CkQ/NHh0si1lMO.XOtTpxPwbAt2WLOLWWPid7gOrQtSV8QHm'),
(2, '', 'elmustafaayoub@gmail.com', '$2y$10$7rSSg/lnifcTpX3tirKN9eCmINAWDiCQVXRNq0NHUA34/1vd0aztW'),
(3, '', 'Adreadipama@gmail.com', '$2y$10$ZEkEFdmQ5YpgkaG96ldmTeowKjPyi1wx5M0yalszEBqzo4zzbfq6a');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
