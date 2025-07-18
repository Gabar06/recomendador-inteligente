-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: recomendador_db
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `academico_administrador`
--

DROP TABLE IF EXISTS `academico_administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_administrador` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `login` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `clave` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_administrador`
--

LOCK TABLES `academico_administrador` WRITE;
/*!40000 ALTER TABLE `academico_administrador` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_administrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_alumnos`
--

DROP TABLE IF EXISTS `academico_alumnos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_alumnos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `curso` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sexo` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_alumnos`
--

LOCK TABLES `academico_alumnos` WRITE;
/*!40000 ALTER TABLE `academico_alumnos` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_alumnos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_asignatura`
--

DROP TABLE IF EXISTS `academico_asignatura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_asignatura` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_asignatura`
--

LOCK TABLES `academico_asignatura` WRITE;
/*!40000 ALTER TABLE `academico_asignatura` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_asignatura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_asistencia`
--

DROP TABLE IF EXISTS `academico_asistencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_asistencia` (
  `id` int NOT NULL AUTO_INCREMENT,
  `materia` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `horas` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_asistencia`
--

LOCK TABLES `academico_asistencia` WRITE;
/*!40000 ALTER TABLE `academico_asistencia` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_asistencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_categorias`
--

DROP TABLE IF EXISTS `academico_categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_categorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_categorias`
--

LOCK TABLES `academico_categorias` WRITE;
/*!40000 ALTER TABLE `academico_categorias` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_contenido`
--

DROP TABLE IF EXISTS `academico_contenido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_contenido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `archivo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_subida` datetime(6) NOT NULL,
  `materia_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Academico_contenido_materia_id_5216eb06_fk_Academico_materia_id` (`materia_id`),
  CONSTRAINT `Academico_contenido_materia_id_5216eb06_fk_Academico_materia_id` FOREIGN KEY (`materia_id`) REFERENCES `academico_materia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_contenido`
--

LOCK TABLES `academico_contenido` WRITE;
/*!40000 ALTER TABLE `academico_contenido` DISABLE KEYS */;
INSERT INTO `academico_contenido` VALUES (1,'Ortograf├¡a','Contenido general de la ortograf├¡a','contenidos/manual_de_reglas_ortograficas.pdf','2025-07-03 20:26:52.951226',1);
/*!40000 ALTER TABLE `academico_contenido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_cuota`
--

DROP TABLE IF EXISTS `academico_cuota`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_cuota` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mes` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `monto` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_cuota`
--

LOCK TABLES `academico_cuota` WRITE;
/*!40000 ALTER TABLE `academico_cuota` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_cuota` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_docente`
--

DROP TABLE IF EXISTS `academico_docente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_docente` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `Academico_docente_usuario_id_f2c3d200_fk_Academico_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `academico_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_docente`
--

LOCK TABLES `academico_docente` WRITE;
/*!40000 ALTER TABLE `academico_docente` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_docente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_docente_materias`
--

DROP TABLE IF EXISTS `academico_docente_materias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_docente_materias` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `docente_id` bigint NOT NULL,
  `materia_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Academico_docente_materias_docente_id_materia_id_586b132c_uniq` (`docente_id`,`materia_id`),
  KEY `Academico_docente_ma_materia_id_27ca1d91_fk_Academico` (`materia_id`),
  CONSTRAINT `Academico_docente_ma_docente_id_1b4d12bc_fk_Academico` FOREIGN KEY (`docente_id`) REFERENCES `academico_docente` (`id`),
  CONSTRAINT `Academico_docente_ma_materia_id_27ca1d91_fk_Academico` FOREIGN KEY (`materia_id`) REFERENCES `academico_materia` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_docente_materias`
--

LOCK TABLES `academico_docente_materias` WRITE;
/*!40000 ALTER TABLE `academico_docente_materias` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_docente_materias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_docentes`
--

DROP TABLE IF EXISTS `academico_docentes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_docentes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `login` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `clave` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_docentes`
--

LOCK TABLES `academico_docentes` WRITE;
/*!40000 ALTER TABLE `academico_docentes` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_docentes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_estudiante`
--

DROP TABLE IF EXISTS `academico_estudiante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_estudiante` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `curso` varchar(2) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rendimiento_academico` decimal(5,2) NOT NULL,
  `feedback` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `usuario_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `Academico_estudiante_usuario_id_72f05962_fk_Academico_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `academico_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_estudiante`
--

LOCK TABLES `academico_estudiante` WRITE;
/*!40000 ALTER TABLE `academico_estudiante` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_estudiante` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_guia`
--

DROP TABLE IF EXISTS `academico_guia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_guia` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_asignacion` datetime(6) NOT NULL,
  `completada` tinyint(1) NOT NULL,
  `contenido_id` bigint NOT NULL,
  `estudiante_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Academico_guia_contenido_id_3fbf3bb6_fk_Academico_contenido_id` (`contenido_id`),
  KEY `Academico_guia_estudiante_id_59b8def1_fk_Academico_estudiante_id` (`estudiante_id`),
  CONSTRAINT `Academico_guia_contenido_id_3fbf3bb6_fk_Academico_contenido_id` FOREIGN KEY (`contenido_id`) REFERENCES `academico_contenido` (`id`),
  CONSTRAINT `Academico_guia_estudiante_id_59b8def1_fk_Academico_estudiante_id` FOREIGN KEY (`estudiante_id`) REFERENCES `academico_estudiante` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_guia`
--

LOCK TABLES `academico_guia` WRITE;
/*!40000 ALTER TABLE `academico_guia` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_guia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_materia`
--

DROP TABLE IF EXISTS `academico_materia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_materia` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nivel` varchar(2) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_materia`
--

LOCK TABLES `academico_materia` WRITE;
/*!40000 ALTER TABLE `academico_materia` DISABLE KEYS */;
INSERT INTO `academico_materia` VALUES (1,'Lengua Castellana y Literatura','1');
/*!40000 ALTER TABLE `academico_materia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_nota`
--

DROP TABLE IF EXISTS `academico_nota`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_nota` (
  `id` int NOT NULL AUTO_INCREMENT,
  `materia` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `calificacion` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_nota`
--

LOCK TABLES `academico_nota` WRITE;
/*!40000 ALTER TABLE `academico_nota` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_nota` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_soporte`
--

DROP TABLE IF EXISTS `academico_soporte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_soporte` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mantenimiento` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reparacion` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_soporte`
--

LOCK TABLES `academico_soporte` WRITE;
/*!40000 ALTER TABLE `academico_soporte` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_soporte` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_sucursal`
--

DROP TABLE IF EXISTS `academico_sucursal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_sucursal` (
  `id` int NOT NULL AUTO_INCREMENT,
  `direccion` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nr_sucursal` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_sucursal`
--

LOCK TABLES `academico_sucursal` WRITE;
/*!40000 ALTER TABLE `academico_sucursal` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_sucursal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_usuario`
--

DROP TABLE IF EXISTS `academico_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `is_estudiante` tinyint(1) NOT NULL,
  `is_docente` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_usuario`
--

LOCK TABLES `academico_usuario` WRITE;
/*!40000 ALTER TABLE `academico_usuario` DISABLE KEYS */;
INSERT INTO `academico_usuario` VALUES (1,'pbkdf2_sha256$1000000$5d09qRzbeKG6Lq2P27SFBA$O/Jh59daI+rCg/YuMe78Dyxk65lz03FdCRTDRYpSd84=','2025-07-10 00:07:58.667693',1,'admin','','','fergon.670@gmail.com',1,1,'2025-07-03 18:45:12.895665',0,0);
/*!40000 ALTER TABLE `academico_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_usuario_groups`
--

DROP TABLE IF EXISTS `academico_usuario_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_usuario_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Academico_usuario_groups_usuario_id_group_id_2d02481f_uniq` (`usuario_id`,`group_id`),
  KEY `Academico_usuario_groups_group_id_0cc81ea6_fk_auth_group_id` (`group_id`),
  CONSTRAINT `Academico_usuario_gr_usuario_id_0e2cb272_fk_Academico` FOREIGN KEY (`usuario_id`) REFERENCES `academico_usuario` (`id`),
  CONSTRAINT `Academico_usuario_groups_group_id_0cc81ea6_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_usuario_groups`
--

LOCK TABLES `academico_usuario_groups` WRITE;
/*!40000 ALTER TABLE `academico_usuario_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_usuario_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `academico_usuario_user_permissions`
--

DROP TABLE IF EXISTS `academico_usuario_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academico_usuario_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Academico_usuario_user_p_usuario_id_permission_id_d5306b64_uniq` (`usuario_id`,`permission_id`),
  KEY `Academico_usuario_us_permission_id_6eb3143f_fk_auth_perm` (`permission_id`),
  CONSTRAINT `Academico_usuario_us_permission_id_6eb3143f_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `Academico_usuario_us_usuario_id_9c95256f_fk_Academico` FOREIGN KEY (`usuario_id`) REFERENCES `academico_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academico_usuario_user_permissions`
--

LOCK TABLES `academico_usuario_user_permissions` WRITE;
/*!40000 ALTER TABLE `academico_usuario_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `academico_usuario_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add administrador',6,'add_administrador'),(22,'Can change administrador',6,'change_administrador'),(23,'Can delete administrador',6,'delete_administrador'),(24,'Can view administrador',6,'view_administrador'),(25,'Can add docentes',7,'add_docentes'),(26,'Can change docentes',7,'change_docentes'),(27,'Can delete docentes',7,'delete_docentes'),(28,'Can view docentes',7,'view_docentes'),(29,'Can add alumnos',8,'add_alumnos'),(30,'Can change alumnos',8,'change_alumnos'),(31,'Can delete alumnos',8,'delete_alumnos'),(32,'Can view alumnos',8,'view_alumnos'),(33,'Can add asignatura',9,'add_asignatura'),(34,'Can change asignatura',9,'change_asignatura'),(35,'Can delete asignatura',9,'delete_asignatura'),(36,'Can view asignatura',9,'view_asignatura'),(37,'Can add asistencia',10,'add_asistencia'),(38,'Can change asistencia',10,'change_asistencia'),(39,'Can delete asistencia',10,'delete_asistencia'),(40,'Can view asistencia',10,'view_asistencia'),(41,'Can add categorias',11,'add_categorias'),(42,'Can change categorias',11,'change_categorias'),(43,'Can delete categorias',11,'delete_categorias'),(44,'Can view categorias',11,'view_categorias'),(45,'Can add cuota',12,'add_cuota'),(46,'Can change cuota',12,'change_cuota'),(47,'Can delete cuota',12,'delete_cuota'),(48,'Can view cuota',12,'view_cuota'),(49,'Can add nota',13,'add_nota'),(50,'Can change nota',13,'change_nota'),(51,'Can delete nota',13,'delete_nota'),(52,'Can view nota',13,'view_nota'),(53,'Can add soporte',14,'add_soporte'),(54,'Can change soporte',14,'change_soporte'),(55,'Can delete soporte',14,'delete_soporte'),(56,'Can view soporte',14,'view_soporte'),(57,'Can add sucursal',15,'add_sucursal'),(58,'Can change sucursal',15,'change_sucursal'),(59,'Can delete sucursal',15,'delete_sucursal'),(60,'Can view sucursal',15,'view_sucursal'),(61,'Can add contenido',16,'add_contenido'),(62,'Can change contenido',16,'change_contenido'),(63,'Can delete contenido',16,'delete_contenido'),(64,'Can view contenido',16,'view_contenido'),(65,'Can add estudiante',17,'add_estudiante'),(66,'Can change estudiante',17,'change_estudiante'),(67,'Can delete estudiante',17,'delete_estudiante'),(68,'Can view estudiante',17,'view_estudiante'),(69,'Can add materia',18,'add_materia'),(70,'Can change materia',18,'change_materia'),(71,'Can delete materia',18,'delete_materia'),(72,'Can view materia',18,'view_materia'),(73,'Can add guia',19,'add_guia'),(74,'Can change guia',19,'change_guia'),(75,'Can delete guia',19,'delete_guia'),(76,'Can view guia',19,'view_guia'),(77,'Can add user',20,'add_usuario'),(78,'Can change user',20,'change_usuario'),(79,'Can delete user',20,'delete_usuario'),(80,'Can view user',20,'view_usuario'),(81,'Can add docente',21,'add_docente'),(82,'Can change docente',21,'change_docente'),(83,'Can delete docente',21,'delete_docente'),(84,'Can view docente',21,'view_docente');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_Academico_usuario_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_Academico_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `academico_usuario` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-07-03 20:13:51.423474','1','Lengua Castellana y Literatura - Nivel 1',1,'[{\"added\": {}}]',18,1),(2,'2025-07-03 20:26:52.952236','1','Ortograf├¡a',1,'[{\"added\": {}}]',16,1),(3,'2025-07-03 20:27:22.281165','1','Lengua Castellana y Literatura - Nivel 1',2,'[]',18,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (6,'Academico','administrador'),(8,'Academico','alumnos'),(9,'Academico','asignatura'),(10,'Academico','asistencia'),(11,'Academico','categorias'),(16,'Academico','contenido'),(12,'Academico','cuota'),(21,'Academico','docente'),(7,'Academico','docentes'),(17,'Academico','estudiante'),(19,'Academico','guia'),(18,'Academico','materia'),(13,'Academico','nota'),(14,'Academico','soporte'),(15,'Academico','sucursal'),(20,'Academico','usuario'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-07-03 18:40:06.936244'),(2,'contenttypes','0002_remove_content_type_name','2025-07-03 18:40:07.000681'),(3,'auth','0001_initial','2025-07-03 18:40:07.327949'),(4,'auth','0002_alter_permission_name_max_length','2025-07-03 18:40:07.403904'),(5,'auth','0003_alter_user_email_max_length','2025-07-03 18:40:07.409203'),(6,'auth','0004_alter_user_username_opts','2025-07-03 18:40:07.414441'),(7,'auth','0005_alter_user_last_login_null','2025-07-03 18:40:07.421192'),(8,'auth','0006_require_contenttypes_0002','2025-07-03 18:40:07.421192'),(9,'auth','0007_alter_validators_add_error_messages','2025-07-03 18:40:07.430106'),(10,'auth','0008_alter_user_username_max_length','2025-07-03 18:40:07.433641'),(11,'auth','0009_alter_user_last_name_max_length','2025-07-03 18:40:07.440675'),(12,'auth','0010_alter_group_name_max_length','2025-07-03 18:40:07.454521'),(13,'auth','0011_update_proxy_permissions','2025-07-03 18:40:07.460215'),(14,'auth','0012_alter_user_first_name_max_length','2025-07-03 18:40:07.460215'),(15,'Academico','0001_initial','2025-07-03 18:40:07.483678'),(16,'Academico','0002_docentes','2025-07-03 18:40:07.516852'),(17,'Academico','0003_alumnos','2025-07-03 18:40:07.539164'),(18,'Academico','0004_asignatura','2025-07-03 18:40:07.550370'),(19,'Academico','0005_asistencia_categorias_cuota_nota_soporte_sucursal','2025-07-03 18:40:07.687775'),(20,'Academico','0006_contenido_estudiante_materia_guia_contenido_materia_and_more','2025-07-03 18:40:08.765522'),(21,'admin','0001_initial','2025-07-03 18:40:08.931666'),(22,'admin','0002_logentry_remove_auto_add','2025-07-03 18:40:08.947627'),(23,'admin','0003_logentry_add_action_flag_choices','2025-07-03 18:40:08.960464'),(24,'sessions','0001_initial','2025-07-03 18:40:09.005829');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('rytzp1fohcaqwnkd9yow8xwvwkif1lx1','.eJxVjMsOwiAQRf-FtSHAFGFcuu83NDM8pGogKe3K-O_apAvd3nPOfYmJtrVMW0_LNEdxEVqcfjem8Eh1B_FO9dZkaHVdZpa7Ig_a5dhiel4P9--gUC_fOpH3OAB465FDNhajI4KoyQbAxJiQNSjiEFEzICif9dk743Iwg8ri_QHoYjfk:1uZepS:d2ePE8fr69HJqwqPQY3evUyHm0MOzdgLMkbQNdguT7E','2025-07-24 00:07:58.691109');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-10 23:27:35
