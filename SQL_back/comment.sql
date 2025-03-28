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

 Date: 26/03/2025 15:30:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '评论的唯一ID',
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '评论内容是富文本',
  `create_time` datetime NULL DEFAULT NULL COMMENT '发送时间',
  `user_id` int UNSIGNED NOT NULL COMMENT '发送的用户ID',
  `is_main` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '是否为主评论，1是0否',
  `reply_comment_id` bigint NULL DEFAULT NULL COMMENT '回复的评论的ID',
  `reply_work_id` bigint UNSIGNED NOT NULL COMMENT '回复的作品ID',
  `reply_work_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '回复的作品类型',
  `reply_user_id` bigint NULL DEFAULT NULL COMMENT '回复的用户的ID，如果有的话',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `cm_user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
