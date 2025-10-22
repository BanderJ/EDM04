-- Script de inicialización de base de datos para
-- Frutos de Oro S.A.C. - Sistema de Gestión de Cumplimiento Normativo
-- ====================================================================

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS frutos_oro_db;
USE frutos_oro_db;

-- Tabla de Usuarios
CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(80) UNIQUE NOT NULL,
  `email` VARCHAR(120) UNIQUE NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `full_name` VARCHAR(120) NOT NULL,
  `department` VARCHAR(120),
  `role` VARCHAR(20) NOT NULL DEFAULT 'usuario',
  `is_active` BOOLEAN DEFAULT TRUE,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_username` (`username`),
  INDEX `idx_email` (`email`),
  INDEX `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Certificaciones
CREATE TABLE `certifications` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(150) NOT NULL,
  `norm` VARCHAR(100) NOT NULL,
  `issuing_entity` VARCHAR(150) NOT NULL,
  `emission_date` DATE NOT NULL,
  `expiration_date` DATE NOT NULL,
  `responsible_id` INT NOT NULL,
  `document_path` VARCHAR(255),
  `status` VARCHAR(20) NOT NULL DEFAULT 'vigente',
  `alert_sent_15` BOOLEAN DEFAULT FALSE,
  `alert_sent_30` BOOLEAN DEFAULT FALSE,
  `alert_sent_60` BOOLEAN DEFAULT FALSE,
  `notes` TEXT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`responsible_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT,
  INDEX `idx_expiration_date` (`expiration_date`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Auditorías
CREATE TABLE `audits` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `audit_type` VARCHAR(20) NOT NULL,
  `scheduled_date` DATE NOT NULL,
  `executed_date` DATE,
  `evaluated_area` VARCHAR(150) NOT NULL,
  `responsible_id` INT NOT NULL,
  `description` TEXT,
  `status` VARCHAR(20) NOT NULL DEFAULT 'programada',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`responsible_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT,
  INDEX `idx_audit_type` (`audit_type`),
  INDEX `idx_scheduled_date` (`scheduled_date`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Hallazgos de Auditoría
CREATE TABLE `audit_findings` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `audit_id` INT NOT NULL,
  `description` TEXT NOT NULL,
  `severity` VARCHAR(20) NOT NULL,
  `corrective_action` TEXT,
  `responsible` VARCHAR(120),
  `deadline` DATE,
  `status` VARCHAR(20) NOT NULL DEFAULT 'abierto',
  `notes` TEXT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`audit_id`) REFERENCES `audits` (`id`) ON DELETE CASCADE,
  INDEX `idx_severity` (`severity`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Políticas
CREATE TABLE `policies` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(200) NOT NULL,
  `description` TEXT NOT NULL,
  `content` TEXT,
  `version` VARCHAR(10) DEFAULT '1.0',
  `effective_date` DATE NOT NULL,
  `requires_confirmation` BOOLEAN DEFAULT TRUE,
  `is_active` BOOLEAN DEFAULT TRUE,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Confirmaciones de Políticas
CREATE TABLE `policy_confirmations` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `policy_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `confirmed` BOOLEAN DEFAULT FALSE,
  `confirmed_date` DATETIME,
  `digital_signature` VARCHAR(255),
  `ip_address` VARCHAR(50),
  `notes` TEXT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `unique_policy_user` (`policy_id`, `user_id`),
  FOREIGN KEY (`policy_id`) REFERENCES `policies` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  INDEX `idx_confirmed` (`confirmed`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Alertas
CREATE TABLE `alerts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `alert_type` VARCHAR(50) NOT NULL,
  `related_id` INT,
  `title` VARCHAR(200) NOT NULL,
  `message` TEXT,
  `severity` VARCHAR(20) DEFAULT 'info',
  `is_read` BOOLEAN DEFAULT FALSE,
  `recipient_email` VARCHAR(120),
  `sent` BOOLEAN DEFAULT FALSE,
  `sent_date` DATETIME,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_alert_type` (`alert_type`),
  INDEX `idx_is_read` (`is_read`),
  INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Registro de Auditoría del Sistema
CREATE TABLE `audit_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT,
  `action` VARCHAR(100) NOT NULL,
  `entity_type` VARCHAR(50),
  `entity_id` INT,
  `changes` TEXT,
  `ip_address` VARCHAR(50),
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  INDEX `idx_created_at` (`created_at`),
  INDEX `idx_entity_type` (`entity_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================================
-- DATOS INICIALES
-- ====================================================================

-- Insertar usuario administrador por defecto
-- Username: admin, Password: admin123 (debe ser cambiada en producción)
-- Hash generado con werkzeug.security.generate_password_hash('admin123', method='pbkdf2:sha256')
INSERT INTO `users` (`username`, `email`, `password_hash`, `full_name`, `department`, `role`, `is_active`) 
VALUES ('admin', 'admin@frutosoro.com', 'pbkdf2:sha256:600000$5rxu7B06pvLeE26B$aa81fa13037e96263748cf9c304a38d424f2bb434576e079014f3784bf898733', 'Administrador Sistema', 'Dirección', 'administrador', TRUE);

-- Insertar usuarios de ejemplo
-- jefe_produccion: produccion123
-- jefe_calidad: calidad123
-- auditor_interno: auditor123
INSERT INTO `users` (`username`, `email`, `password_hash`, `full_name`, `department`, `role`, `is_active`) 
VALUES 
  ('jefe_produccion', 'jefe.produccion@frutosoro.com', 'pbkdf2:sha256:600000$5rxu7B06pvLeE26B$aa81fa13037e96263748cf9c304a38d424f2bb434576e079014f3784bf898733', 'Juan Pérez García', 'Producción', 'jefe_unidad', TRUE),
  ('jefe_calidad', 'jefe.calidad@frutosoro.com', 'pbkdf2:sha256:600000$5rxu7B06pvLeE26B$aa81fa13037e96263748cf9c304a38d424f2bb434576e079014f3784bf898733', 'María Rodríguez López', 'Calidad', 'jefe_unidad', TRUE),
  ('auditor_interno', 'auditor.interno@frutosoro.com', 'pbkdf2:sha256:600000$5rxu7B06pvLeE26B$aa81fa13037e96263748cf9c304a38d424f2bb434576e079014f3784bf898733', 'Carlos González Martínez', 'Auditoría', 'auditor', TRUE);

-- Insertar certificaciones de ejemplo
INSERT INTO `certifications` (`name`, `norm`, `issuing_entity`, `emission_date`, `expiration_date`, `responsible_id`, `status`, `notes`)
VALUES
  ('GlobalG.A.P. Certificate', 'GlobalG.A.P.', 'GlobalG.A.P. Organization', '2022-01-15', '2025-01-15', 2, 'vigente', 'Certificación internacional para agricultura segura'),
  ('HACCP Certification', 'HACCP', 'DIGESA', '2023-06-01', '2025-12-01', 3, 'vigente', 'Análisis de Peligros y Puntos Críticos de Control'),
  ('BRC Certification', 'BRC', 'Bureau Veritas', '2022-09-20', '2025-03-20', 2, 'proxima_vencer', 'Norma de Seguridad Alimentaria Británica'),
  ('ISO 22000:2018', 'ISO 22000', 'TÜV Rheinland', '2023-03-10', '2026-03-10', 3, 'vigente', 'Sistema de Gestión de Seguridad Alimentaria');

-- Insertar auditorías de ejemplo
INSERT INTO `audits` (`audit_type`, `scheduled_date`, `executed_date`, `evaluated_area`, `responsible_id`, `status`, `description`)
VALUES
  ('interna', '2025-10-20', '2025-10-20', 'Producción', 4, 'completada', 'Auditoría interna para verificar cumplimiento de protocolos de seguridad alimentaria'),
  ('externa', '2025-11-15', NULL, 'Almacenamiento', 4, 'programada', 'Auditoría externa por certificadora BRC'),
  ('interna', '2025-10-25', NULL, 'Laboratorio de Calidad', 4, 'programada', 'Verificación de equipos de medición calibrados');

-- Insertar hallazgos de ejemplo
INSERT INTO `audit_findings` (`audit_id`, `description`, `severity`, `corrective_action`, `responsible`, `deadline`, `status`)
VALUES
  (1, 'Algunos registros de temperatura no estaban completos', 'menor', 'Implementar sistema automático de registro de temperatura', 'Juan Pérez García', '2025-11-20', 'cerrado'),
  (3, 'Necesidad de actualizar manuales de procedimiento', 'mayor', 'Revisar y actualizar todos los manuales antes de auditoría', 'María Rodríguez López', '2025-11-10', 'abierto');

-- Insertar políticas de ejemplo
INSERT INTO `policies` (`title`, `description`, `content`, `version`, `effective_date`, `requires_confirmation`, `is_active`)
VALUES
  ('Política de Seguridad Alimentaria', 'Todos los empleados deben cumplir con los protocolos de seguridad alimentaria establecidos por la empresa.', 
   'Contenido completo de la política...', '1.0', '2025-10-01', TRUE, TRUE),
  ('Política de Higiene y Saneamiento', 'Procedimientos de higiene y saneamiento en todas las áreas de producción y almacenamiento.', 
   'Contenido completo de la política...', '2.0', '2025-09-15', TRUE, TRUE);

-- ====================================================================
-- CREAR ÍNDICES ADICIONALES PARA OPTIMIZAR QUERIES
-- ====================================================================

-- Índices para búsquedas frecuentes
CREATE INDEX `idx_cert_responsible_date` ON `certifications` (`responsible_id`, `expiration_date`);
CREATE INDEX `idx_audit_responsible_date` ON `audits` (`responsible_id`, `scheduled_date`);
CREATE INDEX `idx_policy_active_date` ON `policies` (`is_active`, `effective_date`);

-- ====================================================================
-- FIN DEL SCRIPT
-- ====================================================================
