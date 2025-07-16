-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 16-07-2025 a las 02:08:03
-- Versión del servidor: 9.1.0
-- Versión de PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `libreria_assets`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `assets`
--

DROP TABLE IF EXISTS `assets`;
CREATE TABLE IF NOT EXISTS `assets` (
  `id_asset` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text,
  `url_imagen` varchar(255) DEFAULT NULL,
  `id_categoria` int DEFAULT NULL,
  PRIMARY KEY (`id_asset`),
  KEY `id_categoria` (`id_categoria`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `assets`
--

INSERT INTO `assets` (`id_asset`, `nombre`, `descripcion`, `url_imagen`, `id_categoria`) VALUES
(1, 'Laptop ASUS', 'Laptop para desarrollo de software', '/static/images/laptop.jpg', 1),
(2, 'Libro DDD', 'Domain-Driven Design de Eric Evans', '/static/images/ddd_book.jpg', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `assettags`
--

DROP TABLE IF EXISTS `assettags`;
CREATE TABLE IF NOT EXISTS `assettags` (
  `id_asset` int NOT NULL,
  `id_tag` int NOT NULL,
  PRIMARY KEY (`id_asset`,`id_tag`),
  KEY `id_tag` (`id_tag`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `assettags`
--

INSERT INTO `assettags` (`id_asset`, `id_tag`) VALUES
(1, 1),
(1, 2),
(2, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categories`
--

DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  PRIMARY KEY (`id_categoria`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `categories`
--

INSERT INTO `categories` (`id_categoria`, `nombre`, `descripcion`) VALUES
(1, 'Tecnología', 'Productos electrónicos y software'),
(2, 'Libros', 'Libros físicos y digitales'),
(3, 'Naturaleza', 'Paisajes, Aventura, Camping');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `logs`
--

DROP TABLE IF EXISTS `logs`;
CREATE TABLE IF NOT EXISTS `logs` (
  `id_log` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `id_asset` int DEFAULT NULL,
  `accion` varchar(100) NOT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `id_categoria` int DEFAULT NULL,
  `id_tag` int DEFAULT NULL,
  `id_usuario_afectado` int DEFAULT NULL,
  `valores_antes` text,
  `valores_despues` text,
  `entidad` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_log`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_asset` (`id_asset`)
) ENGINE=MyISAM AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `logs`
--

INSERT INTO `logs` (`id_log`, `id_usuario`, `id_asset`, `accion`, `fecha_registro`, `id_categoria`, `id_tag`, `id_usuario_afectado`, `valores_antes`, `valores_despues`, `entidad`) VALUES
(20, 1, NULL, 'login_user', '2025-07-16 01:53:40', NULL, NULL, NULL, NULL, NULL, NULL),
(19, 1, NULL, 'logout_user', '2025-07-16 01:45:11', NULL, NULL, NULL, NULL, NULL, NULL),
(18, NULL, NULL, 'update_user', '2025-07-16 01:44:36', NULL, NULL, 2, '{\"nombre\": \"Usuario1\", \"email\": \"usuario1@test.com\", \"is_admin\": false}', '{\"nombre\": \"Usuario1\", \"email\": \"usuario1@test.com\", \"is_admin\": false}', 'usuario'),
(17, NULL, NULL, 'delete_user', '2025-07-16 01:43:27', NULL, NULL, 3, '{\"nombre\": \"Kevin\", \"email\": \"kevin@hotmail.com\", \"is_admin\": false}', NULL, 'usuario'),
(16, 1, NULL, 'login_user', '2025-07-16 01:43:05', NULL, NULL, NULL, NULL, NULL, NULL),
(21, NULL, 1, 'update_asset', '2025-07-16 01:54:28', NULL, NULL, NULL, '{\"nombre\": \"Laptop ASUS\", \"descripcion\": \"Laptop para desarrollo de software\", \"url_imagen\": \"/static/images/laptop.jpg\", \"id_categoria\": 1}', '{\"nombre\": \"Laptop ASUS\", \"descripcion\": \"Laptop para desarrollo de software\", \"url_imagen\": \"/static/images/laptop.jpg\", \"id_categoria\": 1}', 'asset'),
(22, 1, NULL, 'logout_user', '2025-07-16 01:55:43', NULL, NULL, NULL, NULL, NULL, NULL),
(23, 2, NULL, 'login_user', '2025-07-16 02:03:03', NULL, NULL, NULL, NULL, NULL, NULL),
(24, 2, NULL, 'Seleccionó categoría: 1', '2025-07-16 02:03:12', NULL, NULL, NULL, NULL, NULL, NULL),
(25, 2, NULL, 'Seleccionó categoría: 2', '2025-07-16 02:03:14', NULL, NULL, NULL, NULL, NULL, NULL),
(26, 2, NULL, 'logout_user', '2025-07-16 02:04:17', NULL, NULL, NULL, NULL, NULL, NULL),
(27, 1, NULL, 'login_user', '2025-07-16 02:04:20', NULL, NULL, NULL, NULL, NULL, NULL),
(28, NULL, NULL, 'create_category', '2025-07-16 02:05:04', 3, NULL, NULL, NULL, '{\"nombre\": \"Naturaleza\", \"descripcion\": \"Paisajes, Aventura, Camping\"}', 'categoria'),
(29, 1, NULL, 'logout_user', '2025-07-16 02:06:00', NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tags`
--

DROP TABLE IF EXISTS `tags`;
CREATE TABLE IF NOT EXISTS `tags` (
  `id_tag` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id_tag`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `tags`
--

INSERT INTO `tags` (`id_tag`, `nombre`) VALUES
(1, 'Nuevo'),
(2, 'Popular'),
(3, 'Descuento');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

DROP TABLE IF EXISTS `usuario`;
CREATE TABLE IF NOT EXISTS `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `nombre`, `email`, `password`, `is_admin`) VALUES
(1, 'Admin', 'admin@admin.com', '1234', 1),
(2, 'Usuario1', 'usuario1@test.com', '12345', 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
