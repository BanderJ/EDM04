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

-- Tabla de Roles del Sistema
CREATE TABLE `roles` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) UNIQUE NOT NULL,
  `display_name` VARCHAR(100) NOT NULL,
  `description` TEXT,
  `is_system_role` BOOLEAN DEFAULT FALSE,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Módulos/Secciones del Sistema
CREATE TABLE `modules` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) UNIQUE NOT NULL,
  `display_name` VARCHAR(100) NOT NULL,
  `description` TEXT,
  `icon` VARCHAR(50),
  `is_active` BOOLEAN DEFAULT TRUE,
  `display_order` INT DEFAULT 0,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_name` (`name`),
  INDEX `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Permisos por Rol y Módulo
CREATE TABLE `role_permissions` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `role_id` INT NOT NULL,
  `module_id` INT NOT NULL,
  `can_view` BOOLEAN DEFAULT FALSE,
  `can_create` BOOLEAN DEFAULT FALSE,
  `can_edit` BOOLEAN DEFAULT FALSE,
  `can_delete` BOOLEAN DEFAULT FALSE,
  `can_export` BOOLEAN DEFAULT FALSE,
  `can_approve` BOOLEAN DEFAULT FALSE,
  `custom_permissions` JSON,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `unique_role_module` (`role_id`, `module_id`),
  FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`) ON DELETE CASCADE,
  INDEX `idx_role_module` (`role_id`, `module_id`)
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
  ('jefe_produccion', 'jefe.produccion@frutosoro.com', 'pbkdf2:sha256:600000$5rxu7B06pvLeE26B$aa81fa13037e96263748cf9c304a38d424f2bb434576e079014f3784bf898733', 'Juan Pérez García', 'Producción', 'jefe_produccion', TRUE),
  ('jefe_calidad', 'jefe.calidad@frutosoro.com', 'pbkdf2:sha256:600000$5rxu7B06pvLeE26B$aa81fa13037e96263748cf9c304a38d424f2bb434576e079014f3784bf898733', 'María Rodríguez López', 'Calidad', 'jefe_calidad', TRUE),
  ('auditor_interno', 'auditor.interno@frutosoro.com', 'pbkdf2:sha256:600000$5rxu7B06pvLeE26B$aa81fa13037e96263748cf9c304a38d424f2bb434576e079014f3784bf898733', 'Carlos González Martínez', 'Auditoría', 'auditor_interno', TRUE);

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
-- SISTEMA DE ROLES Y PERMISOS
-- ====================================================================

-- Insertar roles del sistema
INSERT INTO `roles` (`name`, `display_name`, `description`, `is_system_role`) 
VALUES 
  ('administrador', 'Administrador del Sistema', 'Acceso total al sistema, gestión de usuarios y permisos', TRUE),
  ('jefe_unidad', 'Jefe de Unidad', 'Gestión completa de su área asignada', TRUE),
  ('jefe_calidad', 'Jefe de Calidad', 'Gestión de calidad, auditorías y certificaciones', TRUE),
  ('jefe_produccion', 'Jefe de Producción', 'Gestión de producción y cumplimiento normativo', TRUE),
  ('auditor_interno', 'Auditor Interno', 'Realización y gestión de auditorías internas', TRUE),
  ('auditor', 'Auditor', 'Consulta y registro de auditorías', TRUE),
  ('usuario', 'Usuario General', 'Usuario con permisos básicos de consulta', TRUE);

-- Insertar módulos del sistema
INSERT INTO `modules` (`name`, `display_name`, `description`, `icon`, `is_active`, `display_order`) 
VALUES 
  ('dashboard', 'Dashboard', 'Panel principal con indicadores', 'fa-chart-line', TRUE, 1),
  ('certifications', 'Certificaciones', 'Gestión de certificaciones normativas', 'fa-certificate', TRUE, 2),
  ('audits', 'Auditorías', 'Gestión de auditorías internas y externas', 'fa-clipboard-check', TRUE, 3),
  ('findings', 'Hallazgos', 'Gestión de hallazgos de auditorías', 'fa-exclamation-triangle', TRUE, 4),
  ('policies', 'Políticas', 'Gestión de políticas de cumplimiento', 'fa-file-contract', TRUE, 5),
  ('reports', 'Reportes', 'Generación de reportes y estadísticas', 'fa-file-pdf', TRUE, 6),
  ('users', 'Usuarios', 'Administración de usuarios del sistema', 'fa-users', TRUE, 7),
  ('permissions', 'Permisos', 'Configuración de permisos por rol', 'fa-key', TRUE, 8),
  ('audit_logs', 'Registro del Sistema', 'Bitácora de acciones del sistema', 'fa-history', TRUE, 9);

-- ====================================================================
-- PERMISOS POR ROL - ADMINISTRADOR
-- ====================================================================
INSERT INTO `role_permissions` (`role_id`, `module_id`, `can_view`, `can_create`, `can_edit`, `can_delete`, `can_export`, `can_approve`) 
VALUES 
  -- Administrador tiene todos los permisos en todos los módulos
  (1, 1, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),  -- Dashboard
  (1, 2, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),  -- Certificaciones
  (1, 3, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),  -- Auditorías
  (1, 4, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),  -- Hallazgos
  (1, 5, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),  -- Políticas
  (1, 6, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),  -- Reportes
  (1, 7, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),  -- Usuarios
  (1, 8, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),  -- Permisos
  (1, 9, TRUE, FALSE, FALSE, FALSE, TRUE, FALSE); -- Registro del Sistema (solo ver y exportar)

-- ====================================================================
-- PERMISOS POR ROL - JEFE DE CALIDAD
-- ====================================================================
INSERT INTO `role_permissions` (`role_id`, `module_id`, `can_view`, `can_create`, `can_edit`, `can_delete`, `can_export`, `can_approve`) 
VALUES 
  (3, 1, TRUE, FALSE, FALSE, FALSE, TRUE, FALSE),   -- Dashboard: Ver y exportar
  (3, 2, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),       -- Certificaciones: Todos los permisos
  (3, 3, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),       -- Auditorías: Todos los permisos
  (3, 4, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),       -- Hallazgos: Todos los permisos
  (3, 5, TRUE, TRUE, TRUE, FALSE, TRUE, TRUE),      -- Políticas: Ver, crear, editar, exportar, aprobar (no eliminar)
  (3, 6, TRUE, TRUE, FALSE, FALSE, TRUE, FALSE),    -- Reportes: Ver, crear, exportar
  (3, 7, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE),  -- Usuarios: Solo ver
  (3, 8, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE), -- Permisos: Sin acceso
  (3, 9, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE); -- Registro: Sin acceso

-- ====================================================================
-- PERMISOS POR ROL - JEFE DE PRODUCCIÓN
-- ====================================================================
INSERT INTO `role_permissions` (`role_id`, `module_id`, `can_view`, `can_create`, `can_edit`, `can_delete`, `can_export`, `can_approve`) 
VALUES 
  (4, 1, TRUE, FALSE, FALSE, FALSE, TRUE, FALSE),   -- Dashboard: Ver y exportar
  (4, 2, TRUE, TRUE, TRUE, FALSE, TRUE, FALSE),     -- Certificaciones: Ver, crear, editar, exportar
  (4, 3, TRUE, TRUE, TRUE, FALSE, TRUE, FALSE),     -- Auditorías: Ver, crear, editar, exportar
  (4, 4, TRUE, TRUE, TRUE, FALSE, TRUE, FALSE),     -- Hallazgos: Ver, crear, editar, exportar
  (4, 5, TRUE, FALSE, FALSE, FALSE, TRUE, FALSE),   -- Políticas: Solo ver y exportar
  (4, 6, TRUE, TRUE, FALSE, FALSE, TRUE, FALSE),    -- Reportes: Ver, crear, exportar
  (4, 7, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE),  -- Usuarios: Solo ver
  (4, 8, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE), -- Permisos: Sin acceso
  (4, 9, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE); -- Registro: Sin acceso

-- ====================================================================
-- PERMISOS POR ROL - AUDITOR INTERNO
-- ====================================================================
INSERT INTO `role_permissions` (`role_id`, `module_id`, `can_view`, `can_create`, `can_edit`, `can_delete`, `can_export`, `can_approve`) 
VALUES 
  (5, 1, TRUE, FALSE, FALSE, FALSE, TRUE, FALSE),   -- Dashboard: Ver y exportar
  (5, 2, TRUE, FALSE, FALSE, FALSE, TRUE, FALSE),   -- Certificaciones: Solo ver y exportar
  (5, 3, TRUE, TRUE, TRUE, FALSE, TRUE, FALSE),     -- Auditorías: Ver, crear, editar, exportar (no eliminar)
  (5, 4, TRUE, TRUE, TRUE, FALSE, TRUE, FALSE),     -- Hallazgos: Ver, crear, editar, exportar (no eliminar)
  (5, 5, TRUE, FALSE, FALSE, FALSE, TRUE, FALSE),   -- Políticas: Solo ver y exportar
  (5, 6, TRUE, TRUE, FALSE, FALSE, TRUE, FALSE),    -- Reportes: Ver, crear, exportar
  (5, 7, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE),  -- Usuarios: Solo ver
  (5, 8, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE), -- Permisos: Sin acceso
  (5, 9, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE); -- Registro: Sin acceso

-- ====================================================================
-- PERMISOS POR ROL - AUDITOR
-- ====================================================================
INSERT INTO `role_permissions` (`role_id`, `module_id`, `can_view`, `can_create`, `can_edit`, `can_delete`, `can_export`, `can_approve`) 
VALUES 
  (6, 1, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE),  -- Dashboard: Solo ver
  (6, 2, TRUE, FALSE, FALSE, FALSE, TRUE, FALSE),   -- Certificaciones: Ver y exportar
  (6, 3, TRUE, TRUE, FALSE, FALSE, TRUE, FALSE),    -- Auditorías: Ver, crear, exportar
  (6, 4, TRUE, TRUE, FALSE, FALSE, TRUE, FALSE),    -- Hallazgos: Ver, crear, exportar
  (6, 5, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE),  -- Políticas: Solo ver
  (6, 6, TRUE, FALSE, FALSE, FALSE, TRUE, FALSE),   -- Reportes: Ver y exportar
  (6, 7, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE), -- Usuarios: Sin acceso
  (6, 8, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE), -- Permisos: Sin acceso
  (6, 9, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE); -- Registro: Sin acceso

-- ====================================================================
-- PERMISOS POR ROL - USUARIO GENERAL
-- ====================================================================
INSERT INTO `role_permissions` (`role_id`, `module_id`, `can_view`, `can_create`, `can_edit`, `can_delete`, `can_export`, `can_approve`) 
VALUES 
  (7, 1, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE),  -- Dashboard: Solo ver
  (7, 2, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE),  -- Certificaciones: Solo ver
  (7, 3, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE),  -- Auditorías: Solo ver
  (7, 4, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE),  -- Hallazgos: Solo ver
  (7, 5, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE),  -- Políticas: Solo ver
  (7, 6, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE),  -- Reportes: Solo ver
  (7, 7, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE), -- Usuarios: Sin acceso
  (7, 8, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE), -- Permisos: Sin acceso
  (7, 9, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE); -- Registro: Sin acceso

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
