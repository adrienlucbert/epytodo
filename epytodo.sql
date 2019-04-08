CREATE DATABASE IF NOT EXISTS `epytodo`;
USE `epytodo`;
CREATE TABLE IF NOT EXISTS `user` (
       `user_id` INT(11) NOT NULL AUTO_INCREMENT,
       `username` VARCHAR(255) NOT NULL,
       `password` VARCHAR(255) NOT NULL,
       PRIMARY KEY (`user_id`),
       UNIQUE KEY `username` (`username`)
);
CREATE TABLE `task` (
       `task_id` INT(11) NOT NULL AUTO_INCREMENT,
       `title` VARCHAR(255) NOT NULL,
       `begin` DATETIME DEFAULT CURRENT_TIMESTAMP,
       `end` DATETIME DEFAULT NULL,
       `status` ENUM('not started', 'in progress', 'done') NOT NULL DEFAULT 'not started',
       PRIMARY KEY (`task_id`)
);
CREATE TABLE `user_has_task` (
       `fk_user_id` INT(11) NOT NULL,
       `fk_task_id` INT(11) NOT NULL,
       KEY `fk_user_id` (`fk_user_id`),
       KEY `fk_task_id` (`fk_task_id`)
);

ALTER TABLE `user_has_task`
    ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`fk_user_id`) REFERENCES `user` (`user_id`),
    ADD CONSTRAINT `fk_task_id` FOREIGN KEY (`fk_task_id`) REFERENCES `task` (`task_id`);
COMMIT;