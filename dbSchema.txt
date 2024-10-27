-- Create the database
CREATE DATABASE db_interview_rohan;

-- Use the database
USE db_interview_rohan;

-- Create the user table
CREATE TABLE `user` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    name VARCHAR(120) NOT NULL,
);

-- Create the module table
CREATE TABLE `module` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    parent_id INT,
    `order` INT NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES `module`(id) ON DELETE CASCADE
);

-- Create the test_case table
CREATE TABLE `test_case` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    module_id INT NOT NULL,
    summary TEXT NOT NULL,
    description TEXT,
    attachment VARCHAR(255),
    FOREIGN KEY (module_id) REFERENCES `module`(id) ON DELETE CASCADE
);
