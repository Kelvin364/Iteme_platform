-- Create the database
CREATE DATABASE IF NOT EXISTS iteme_db;

-- Create the user
CREATE USER 'kelvin'@'localhost' IDENTIFIED BY 'Iteme_db_123';

-- Grant permissions to the user on the database
GRANT ALL PRIVILEGES ON iteme_db.* TO 'kelvin'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;