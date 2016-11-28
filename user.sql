CREATE TABLE `user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL DEFAULT '',
  `gender` tinyint(1) DEFAULT NULL,
  `fans` int(10) NOT NULL DEFAULT '0',
  `focus` int(10) NOT NULL DEFAULT '0',
  `gouda` int(10) NOT NULL DEFAULT '0',
  `praise` int(10) DEFAULT '0',
  `publish_count` int(10) NOT NULL DEFAULT '0',
  `address` varchar(50) DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=10320 DEFAULT CHARSET=utf8mb4;