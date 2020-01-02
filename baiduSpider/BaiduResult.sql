/*
Navicat MySQL Data Transfer

Source Server         : CMCandy
Source Server Version : 80018
Source Host           : www.cmcandy.com:3306
Source Database       : BaiduResult

Target Server Type    : MYSQL
Target Server Version : 80018
File Encoding         : 65001

Date: 2020-01-02 14:10:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for KeyWords
-- ----------------------------
DROP TABLE IF EXISTS `KeyWords`;
CREATE TABLE `KeyWords` (
  `KeywordID` int(11) NOT NULL AUTO_INCREMENT,
  `Keyword` varchar(50) NOT NULL,
  `Word` varchar(50) NOT NULL,
  PRIMARY KEY (`KeywordID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for KeywordsLinks
-- ----------------------------
DROP TABLE IF EXISTS `KeywordsLinks`;
CREATE TABLE `KeywordsLinks` (
  `LinkID` int(11) NOT NULL AUTO_INCREMENT,
  `Link` varchar(500) NOT NULL,
  `Content` text,
  `KeyWordID` int(11) NOT NULL,
  PRIMARY KEY (`LinkID`),
  KEY `KeyWordID` (`KeyWordID`),
  CONSTRAINT `KeywordsLinks_ibfk_1` FOREIGN KEY (`KeyWordID`) REFERENCES `KeyWords` (`KeywordID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8;
