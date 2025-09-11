-- Adminer 5.3.0 MariaDB 10.11.10-MariaDB dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

CREATE DATABASE `u760464709_23005026_bd` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `u760464709_23005026_bd`;

DROP TABLE IF EXISTS `categorias`;
CREATE TABLE `categorias` (
  `idCategoria` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombreCategoria` varchar(50) NOT NULL,
  PRIMARY KEY (`idCategoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `categorias` (`idCategoria`, `nombreCategoria`) VALUES
(1,	'Escolar'),
(2,	'Trabajo'),
(3,	'Personal'),
(4,	'Urgente');

DROP TABLE IF EXISTS `pendientes`;
CREATE TABLE `pendientes` (
  `idPendiente` bigint(20) NOT NULL AUTO_INCREMENT,
  `tituloPendiente` varchar(100) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `estado` varchar(10) NOT NULL,
  `idCategoria` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`idPendiente`),
  KEY `idCategoria` (`idCategoria`),
  CONSTRAINT `pendientes_ibfk_1` FOREIGN KEY (`idCategoria`) REFERENCES `categorias` (`idCategoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `pendientes` (`idPendiente`, `tituloPendiente`, `descripcion`, `estado`, `idCategoria`) VALUES
(1,	'tarea AS',	'Primera practica',	'pendiente',	1),
(2,	'Reunión de equipo',	'Reunión semanal del equipo de desarrollo',	'en_progreso',	2),
(3,	'Comprar supermercado',	'Lista de compras para la semana',	'pendiente',	3),
(4,	'Entrega proyecto',	'Finalizar y entregar proyecto final',	'pendiente',	4);

DROP TABLE IF EXISTS `recordatorios`;
CREATE TABLE `recordatorios` (
  `idRecordatorio` bigint(20) NOT NULL AUTO_INCREMENT,
  `idPendiente` bigint(20) NOT NULL,
  `idCategoria` bigint(20) DEFAULT NULL,
  `mensaje` varchar(100) DEFAULT NULL,
  `fechaHora` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`idRecordatorio`),
  KEY `idPendiente` (`idPendiente`),
  KEY `idCategoria` (`idCategoria`),
  CONSTRAINT `recordatorios_ibfk_1` FOREIGN KEY (`idPendiente`) REFERENCES `pendientes` (`idPendiente`),
  CONSTRAINT `recordatorios_ibfk_2` FOREIGN KEY (`idCategoria`) REFERENCES `categorias` (`idCategoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `recordatorios` (`idRecordatorio`, `idPendiente`, `idCategoria`, `mensaje`, `fechaHora`) VALUES
(1,	1,	1,	'Acabarlo ya',	'2025-09-11 01:19:56'),
(2,	2,	2,	'No olvides llevar la presentación',	'2025-01-15 10:00:00'),
(3,	3,	3,	'Recordar comprar leche y pan',	'2025-01-14 18:30:00'),
(4,	4,	4,	'¡Último día para entregar!',	'2025-01-20 23:59:59');

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `idUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(55) NOT NULL,
  `contrasena` varchar(55) NOT NULL,
  PRIMARY KEY (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `usuarios` (`idUsuario`, `usuario`, `contrasena`) VALUES
(1,	'admin',	'admin123'),
(2,	'usuario',	'password');


-- 2025-09-11 01:22:45 UTC
