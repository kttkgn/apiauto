-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS api_auto CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE api_auto;

-- 创建用户（如果不存在）
CREATE USER IF NOT EXISTS 'api_user'@'%' IDENTIFIED BY 'ApiUser123';

-- 授予权限
GRANT ALL PRIVILEGES ON api_auto.* TO 'api_user'@'%';
GRANT ALL PRIVILEGES ON api_auto.* TO 'root'@'%';

-- 刷新权限
FLUSH PRIVILEGES;

-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4; 