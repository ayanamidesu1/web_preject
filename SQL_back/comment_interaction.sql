/*
 Navicat Premium Data Transfer

 Source Server         : forum
 Source Server Type    : MySQL
 Source Server Version : 80029
 Source Host           : localhost:3306
 Source Schema         : forum

 Target Server Type    : MySQL
 Target Server Version : 80029
 File Encoding         : 65001

 Date: 26/03/2025 15:31:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comment_interaction
-- ----------------------------
DROP TABLE IF EXISTS `comment_interaction`;
CREATE TABLE `comment_interaction`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `comment_id` bigint UNSIGNED NOT NULL COMMENT '交互的评论ID',
  `operate_user_id` int UNSIGNED NOT NULL COMMENT '操作的用户ID',
  `operate_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '交互类型',
  `datetime` datetime NULL DEFAULT NULL COMMENT '交互时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `cm_id_2`(`operate_user_id` ASC) USING BTREE,
  INDEX `cm_id_1`(`comment_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
