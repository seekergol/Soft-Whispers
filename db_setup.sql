-- 创建梦语童话数据库
CREATE DATABASE IF NOT EXISTS `dreamtales` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE `dreamtales`;

-- 创建用户订阅表
-- 只包含ID和邮箱，并确保邮箱是唯一的
CREATE TABLE IF NOT EXISTS `user_subscriptions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 添加索引以提高查询性能
CREATE INDEX IF NOT EXISTS `idx_created_at` ON `user_subscriptions` (`created_at`);

-- 创建故事表（如果需要存储生成的故事）
CREATE TABLE IF NOT EXISTS `stories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_email` VARCHAR(255) NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `content` TEXT,
    `child_age` VARCHAR(50),
    `theme` VARCHAR(50),
    `educational_value` VARCHAR(50),
    `story_length` INT,
    `has_images` BOOLEAN DEFAULT FALSE,
    `created_at` DATETIME,
    FOREIGN KEY (`user_email`) REFERENCES `user_subscriptions` (`email`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 添加管理员用户表（如果需要后台管理）
CREATE TABLE IF NOT EXISTS `admin_users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `last_login` DATETIME,
    UNIQUE KEY `unique_username` (`username`),
    UNIQUE KEY `unique_admin_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建测试管理员账户（密码需要在实际使用前更改）
INSERT INTO `admin_users` (`username`, `password`, `email`, `last_login`)
VALUES ('admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'admin@dreamtales.com', NOW())
ON DUPLICATE KEY UPDATE `last_login` = NOW();

-- 创建统计表
CREATE TABLE IF NOT EXISTS `statistics` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `date` DATE NOT NULL,
    `new_subscriptions` INT DEFAULT 0,
    `stories_generated` INT DEFAULT 0,
    `total_users` INT DEFAULT 0,
    UNIQUE KEY `unique_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建一个触发器，当新用户订阅时更新统计信息
DELIMITER //
CREATE TRIGGER IF NOT EXISTS `after_subscription_insert`
AFTER INSERT ON `user_subscriptions`
FOR EACH ROW
BEGIN
    INSERT INTO `statistics` (`date`, `new_subscriptions`, `total_users`)
    VALUES (CURDATE(), 1, (SELECT COUNT(*) FROM `user_subscriptions`))
    ON DUPLICATE KEY UPDATE 
        `new_subscriptions` = `new_subscriptions` + 1,
        `total_users` = (SELECT COUNT(*) FROM `user_subscriptions`);
END //
DELIMITER ;

-- 创建一个视图，用于快速获取最活跃的用户
CREATE OR REPLACE VIEW `active_users` AS
SELECT 
    `user_email`,
    COUNT(*) AS `story_count`,
    MAX(`created_at`) AS `last_activity`
FROM 
    `stories`
GROUP BY 
    `user_email`
ORDER BY 
    `story_count` DESC,
    `last_activity` DESC;

-- 添加一些示例用户数据（可选）
INSERT INTO `user_subscriptions` (`email`, `child_age`, `theme`, `educational_value`, `created_at`)
VALUES 
('example1@test.com', 'preschool', 'fantasy', 'courage', NOW()),
('example2@test.com', 'elementary', 'nature', 'curiosity', NOW()),
('example3@test.com', 'middle', 'space', 'perseverance', NOW()),
('parent@family.com', 'toddler', 'animals', 'kindness', NOW())
ON DUPLICATE KEY UPDATE `created_at` = NOW(); 