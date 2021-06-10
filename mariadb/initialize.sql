DELETE FROM mysql.user WHERE User='';
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
CREATE DATABASE IF NOT EXISTS zm;
CREATE USER 'zoneminder'@'%' IDENTIFIED BY 'zoneminder';
GRANT ALL PRIVILEGES ON * . * TO 'zoneminder'@'%';
FLUSH PRIVILEGES;