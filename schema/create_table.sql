create table `stock_info` (
	`id` int NOT NULL AUTO_INCREMENT,
	`stock_id` int NOT NULL DEFAULT 0,
	`stock_name` varchar(250) NOT NULL DEFAULT '',
	`block_id` int NOT NULL DEFAULT 0,
	PRIMARY KEY (`id`),
	UNIQUE KEY `stock_uniq_key` (`stock_id`)) ENGINE=innodb DEFAULT CHARSET=utf8;
create table `block_info` (
	`id` int NOT NULL AUTO_INCREMENT,
	`block_id` int NOT NULL DEFAULT 0,
	`block_name` varchar(250) NOT NULL DEFAULT '',
	PRIMARY KEY (`id`),
	UNIQUE KEY `block_uniq_key` (`block_id`)) ENGINE=innodb DEFAULT CHARSET=utf8;


