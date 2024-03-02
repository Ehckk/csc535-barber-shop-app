DROP DATABASE IF EXISTS csc535_barber;
CREATE DATABASE csc535_barber;
USE csc535_barber;


DROP PROCEDURE IF EXISTS csc535_barber.`sp_barber_availability_for_range`;

DROP VIEW IF EXISTS csc535_barber.`vw_barber_schedule`;
DROP VIEW IF EXISTS csc535_barber.`vw_barber_availability`;

DROP TABLE IF EXISTS csc535_barber.`appointment`;
DROP TABLE IF EXISTS csc535_barber.`unavailable`;
DROP TABLE IF EXISTS csc535_barber.`schedule`;
DROP TABLE IF EXISTS csc535_barber.`weekday`;
DROP TABLE IF EXISTS csc535_barber.`user`;

CREATE TABLE IF NOT EXISTS csc535_barber.`user` (
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `first_name` VARCHAR(255) NOT NULL,
    `last_name` VARCHAR(255) NOT NULL,
    `role` ENUM('Barber', 'Client') DEFAULT 'Client',
    `verified` BOOL DEFAULT 0,
    PRIMARY KEY (`user_id`),
    UNIQUE (`email`)
);

INSERT INTO csc535_barber.`user` VALUES 
	(1, 'test@test.com', 'test', 'Test', 'Test', 'Barber', 1),
    (2, 'test1@test.com', 'client1', 'Test1', 'Client1', 'Client', 1),
    (3, 'test2@test.com', 'client2', 'Test2', 'Client2', 'Client', 1);
    

CREATE TABLE IF NOT EXISTS csc535_barber.`weekday` (
	`weekday_id` TINYINT UNSIGNED NOT NULL,
    `day_name` VARCHAR(16) NOT NULL,
	CONSTRAINT chk_weekday CHECK (`weekday_id` <= 6),
    PRIMARY KEY (`weekday_id`)
);

INSERT INTO csc535_barber.`weekday` VALUES 
	(0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday');

CREATE TABLE IF NOT EXISTS csc535_barber.`schedule` (
    `schedule_id` INT NOT NULL AUTO_INCREMENT,
    `barber_id` INT NOT NULL,
    `weekday_id` TINYINT UNSIGNED NOT NULL,
    `start_time` TIME NOT NULL,
    `end_time` TIME NOT NULL,
    PRIMARY KEY (`schedule_id`),
    CONSTRAINT chk_times CHECK (`end_time` > `start_time`),
    FOREIGN KEY (`barber_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
	FOREIGN KEY (`weekday_id`) REFERENCES `weekday`(`weekday_id`) ON DELETE CASCADE
);

INSERT INTO csc535_barber.`schedule` VALUES 
	(1, 1, 0, '09:30', '12:30'),
    (2, 1, 0, '13:30', '16:30'),
    (3, 1, 1, '10:30', '15:30'),
    (4, 1, 2, '09:30', '12:30'),
    (5, 1, 2, '13:30', '16:30'),
    (6, 1, 4, '09:30', '12:30'),
    (7, 1, 4, '13:30', '16:30');

CREATE TABLE IF NOT EXISTS csc535_barber.`unavailable` (
    `unavailable_id` INT NOT NULL AUTO_INCREMENT,
    `barber_id` INT NOT NULL,
    `start_date` DATE NOT NULL,
    `end_date` DATE DEFAULT NULL,
    `reason` VARCHAR(255) NOT NULL DEFAULT 'Unavailable',
    PRIMARY KEY (`unavailable_id`),
    CONSTRAINT chk_dates CHECK (`end_date` > `start_date`),
	FOREIGN KEY (`barber_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE
);

INSERT INTO csc535_barber.`unavailable` VALUES
	(1, 1, '2024-02-14', DEFAULT, DEFAULT);

CREATE TABLE IF NOT EXISTS csc535_barber.`appointment` (
    `appointment_id` INT NOT NULL AUTO_INCREMENT,
    `barber_id` INT NOT NULL,
	`client_id` INT NOT NULL,
    `booked_date` DATE NOT NULL,
    `start_time` TIME NOT NULL,
    `duration` SMALLINT UNSIGNED NOT NULL,
    `description` TEXT NULL,
    PRIMARY KEY (`appointment_id`),
	FOREIGN KEY (`barber_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
	FOREIGN KEY (`client_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE
);

INSERT INTO csc535_barber.`appointment` VALUES
	(DEFAULT, 1, 2, '2024-02-13', '11:00', 60, DEFAULT),
    (DEFAULT, 1, 3, '2024-02-13', '13:30', 60, DEFAULT),
	(DEFAULT, 1, 2, '2024-02-16', '10:00', 60, DEFAULT),
    (DEFAULT, 1, 3, '2024-02-16', '11:30', 30, DEFAULT);

CREATE VIEW csc535_barber.`vw_barber_schedule` AS
SELECT 
	B.`user_id` AS `barber_id`,
    CONCAT(B.`first_name`, ' ', B.`last_name`) AS `barber_name`,
    W.`weekday_id`,
	W.`day_name`,
	LEFT(W.`day_name`, 3) AS `day_code`,
	S.`start_time`,
    S.`end_time`
FROM csc535_barber.`weekday` AS W 
LEFT JOIN csc535_barber.`schedule` AS S USING (`weekday_id`)
LEFT JOIN csc535_barber.`user` AS B ON B.`user_id` = S.`barber_id`
ORDER BY B.`user_id`, W.`weekday_id`, S.`start_time`;

CREATE VIEW csc535_barber.`vw_barber_availability` AS 
WITH appointments AS (
	SELECT
		A.`appointment_id`,
		A.`booked_date`,
		V.`barber_id`,
        V.`weekday_id`,
		V.`start_time`,
        V.`end_time`,
        A.`start_time` AS `appt_start`,
		DATE_ADD(A.`start_time`, INTERVAL A.`duration` MINUTE) AS `appt_end`
	FROM csc535_barber.`vw_barber_schedule` AS V
	LEFT JOIN csc535_barber.`appointment` AS A
	ON V.`barber_id` = A.`barber_id` 				-- Same barber
	AND V.`weekday_id` = WEEKDAY(A.`booked_date`)	-- Same weekday
	AND V.`start_time` <= A.`start_time`			-- Within range
	AND DATE_ADD(A.`start_time`, INTERVAL A.`duration` MINUTE) <= V.`end_time`
),
overlapping_appointments AS (
	SELECT 
		*,
		LAG(`appt_end`) OVER (
			PARTITION BY `barber_id`, `weekday_id`, `start_time`, `end_time` 
			ORDER BY `start_time`
		) AS `last_appt_end`, -- When does the prev appointment end
		LEAD(`appt_start`) OVER (
			PARTITION BY `barber_id`, `weekday_id`, `start_time`, `end_time` 
			ORDER BY `start_time`
		) AS `next_appt_start` -- When does the next appointment begin
	FROM appointments
	WHERE `appointment_id` IS NOT NULL
)
SELECT 
    `barber_id`,
    `weekday_id`,
    IF(`last_appt_end` IS NULL, `start_time`, `last_appt_end`) AS `start_time`,
    `appt_start` AS `end_time`,
    `booked_date`
FROM overlapping_appointments
UNION
SELECT 
	`barber_id`, 
	`weekday_id`,
	`appt_end` AS `start_time`,
    IF(`next_appt_start` IS NULL, `end_time`, `next_appt_start`) AS `end_time`,
    `booked_date`
FROM overlapping_appointments
UNION 
SELECT
    `barber_id`,
    `weekday_id`,
    `start_time`,
    `end_time`,
    NULL AS `booked_date`
FROM csc535_barber.`vw_barber_schedule`
ORDER BY `barber_id`, `weekday_id`, `start_time`, `end_time`;

DELIMITER //
CREATE PROCEDURE sp_barber_availability_for_range(
	IN range_start date, 
    IN range_duration enum ('D', 'W', 'M')
)
BEGIN
	DECLARE range_end date;
    SET range_end = (
		CASE range_duration
			WHEN 'M' THEN (range_start + INTERVAL 1 MONTH) - INTERVAL 1 DAY
            WHEN 'W' THEN (range_start + INTERVAL 1 WEEK) - INTERVAL 1 DAY
            WHEN 'D' THEN range_start
		END
    );

	WITH RECURSIVE dates AS (
		SELECT range_start AS `date`
		UNION ALL
		SELECT `date` + INTERVAL 1 DAY FROM dates
		WHERE `date` < range_end
	),
	available_dates AS (
		SELECT * FROM dates
		WHERE NOT EXISTS (
			SELECT * FROM csc535_barber.`unavailable`
			WHERE (`end_date` IS NULL AND `date` = `start_date`)
			OR `date` BETWEEN `start_date` AND `end_date`
		)
	),
	dates_with_appointments AS (
		SELECT `date`, A.*
		FROM available_dates -- Only the available dates
		LEFT JOIN  csc535_barber.`vw_barber_availability` AS A 
		ON `date`= `booked_date` 
		WHERE `booked_date` IS NOT NULL
	),
	full_schedule AS (
		SELECT * FROM dates_with_appointments
		UNION 
		SELECT `date`, A.*
		FROM available_dates
		LEFT JOIN  csc535_barber.`vw_barber_availability` AS A 
		ON WEEKDAY(`date`) = A.`weekday_id` 
		WHERE `booked_date` IS NULL AND `date` NOT IN (
			SELECT `date` FROM dates_with_appointments
		)
	)
	SELECT 
		D1.`date`,
		`barber_id`,
		`weekday_id`,
		`start_time`,
		`end_time`
	FROM dates AS D1
	LEFT JOIN full_schedule D2 USING (`date`);
END 
// DELIMITER ;