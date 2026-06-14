-- InnovateTech Database Schema (Vulnerable Lab)
CREATE DATABASE IF NOT EXISTS innovatetech;
USE innovatetech;

-- Users table (stores plaintext passwords - bad practice!)
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  email VARCHAR(200),
  password VARCHAR(100),
  is_admin TINYINT(1) DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table (for search SQLi)
CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200),
  description TEXT,
  price DECIMAL(10,2),
  category VARCHAR(100)
);

-- Secret data table (extracted via UNION SQLi)
CREATE TABLE secret_data (
  id INT AUTO_INCREMENT PRIMARY KEY,
  label VARCHAR(100),
  flag VARCHAR(200),
  data TEXT
);

-- Flags table (accessible via direct MySQL connection)
CREATE TABLE flags (
  id INT AUTO_INCREMENT PRIMARY KEY,
  challenge VARCHAR(200),
  flag VARCHAR(200),
  note TEXT
);

-- Seed users
INSERT INTO users (username, email, password, is_admin) VALUES
  ('admin', 'admin@innovatetech.com', 'Adm1n@InnovateTech2024', 1),
  ('user', 'user@example.com', 'password123', 0),
  ('alice', 'alice@example.com', 'alice123', 0),
  ('bob', 'bob@example.com', 'bob123', 0),
  ('devops', 'devops@innovatetech.com', 'D3v0ps@2024', 0);

-- Seed products
INSERT INTO products (name, description, price, category) VALUES
  ('CloudSync Pro', 'Enterprise cloud synchronization solution with real-time updates', 299.99, 'Cloud'),
  ('AI Analytics', 'Machine learning powered business intelligence platform', 499.99, 'AI'),
  ('SecureVault', 'Zero-knowledge encrypted file storage for teams', 199.99, 'Security'),
  ('FastAPI Gateway', 'High-performance API management and rate limiting', 149.99, 'Infrastructure'),
  ('DataFlow', 'Visual ETL and data pipeline automation tool', 349.99, 'Data'),
  ('GlobalCDN', 'Content delivery network with edge computing', 99.99, 'Infrastructure');

-- Hidden secret data (found via SQLi UNION attack)
INSERT INTO secret_data (label, flag, data) VALUES
  ('SQLi Challenge #25', 'FLAG{un10n_b4s3d_sqli_d4t4_dump}', 'User credentials: admin:Adm1n@InnovateTech2024'),
  ('Internal Config', 'FLAG{bl1nd_sqli_p4ti3nc3_p4y5}', 'JWT_SECRET=secret123,DB_PASS=root,REDIS_HOST=redis'),
  ('Admin Token', 'DO_NOT_SHARE', 'eyJhbGciOiJIUzI1NiJ9.admin_token_here');

-- MySQL direct connection flags
INSERT INTO flags (challenge, flag, note) VALUES
  ('MySQL Exposed Port', 'FLAG{mysql_p0rt_3306_n3v3r_publ1c}', 'Port 3306 should NEVER be internet-facing!'),
  ('SQL Injection Login', 'FLAG{sq1_1nj3ct10n_byp455_l0g1n}', 'Always use parameterized queries!'),
  ('Full Chain Final', 'FLAG{full_ch41n_3xpl01t_m4st3r}', 'Congratulations! You completed the lab!');
