-- ======================================================
-- DATABASE: barangay_online_services
-- Run this in MySQL Workbench or CMD
-- ======================================================

CREATE DATABASE IF NOT EXISTS barangay_online_services;
USE barangay_online_services;

-- TABLE: users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    contact_number VARCHAR(15) DEFAULT NULL,
    address TEXT,
    role ENUM('resident', 'barangay_staff', 'admin') DEFAULT 'resident',
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLE: document_requests
CREATE TABLE IF NOT EXISTS document_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    document_type ENUM('barangay_clearance', 'certificate_indigency', 'proof_residency') NOT NULL,
    purpose TEXT,
    status ENUM('pending', 'reviewing', 'approved', 'rejected', 'completed') DEFAULT 'pending',
    requirements_file VARCHAR(255) DEFAULT NULL,
    admin_remarks TEXT,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- TABLE: event_permits
CREATE TABLE IF NOT EXISTS event_permits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_name VARCHAR(255) NOT NULL,
    event_description TEXT,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    estimated_attendees INT DEFAULT 0,
    venue VARCHAR(255) DEFAULT NULL,
    status ENUM('pending', 'reviewing', 'approved', 'rejected') DEFAULT 'pending',
    requirements_file VARCHAR(255) DEFAULT NULL,
    admin_remarks TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- TABLE: announcements
CREATE TABLE IF NOT EXISTS announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_by INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- TABLE: notifications
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    link VARCHAR(255) DEFAULT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- TABLE: activity_logs
CREATE TABLE IF NOT EXISTS activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT DEFAULT NULL,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Default Admin Account (password: admin123)
INSERT INTO users (first_name, last_name, email, password, role, is_verified) 
VALUES (
    'Admin', 
    'Barangay', 
    'admin@barangay.com', 
    'scrypt:32768:8:1$MnbX5F0hE6WnZ8sA$81c4b7f3a6d9e2f5b8c1a7d4e9f2b6c3a8d5e7f1b4c9a2d6e8f3b7c5a9d2e4f1', 
    'admin', 
    TRUE
);