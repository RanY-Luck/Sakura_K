/*
 Navicat Premium Data Transfer

 Source Server         : 本地数据库
 Source Server Type    : MySQL
 Source Server Version : 80033
 Source Host           : 192.168.1.243:3306
 Source Schema         : skf

 Target Server Type    : MySQL
 Target Server Version : 80033
 File Encoding         : 65001

 Date: 16/04/2025 15:02:36
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for api_info
-- ----------------------------
DROP TABLE IF EXISTS `api_info`;
CREATE TABLE `api_info`  (
  `api_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '接口ID',
  `api_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '接口名称',
  `project_id` int(0) NOT NULL COMMENT '项目ID',
  `api_method` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '接口方法',
  `api_url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '接口地址',
  `api_status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '状态（0正常 1停用）',
  `api_level` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '优先级（P0、P1、P2、P3）',
  `api_tags` json NULL COMMENT '标签',
  `request_data_type` int(0) NULL DEFAULT NULL COMMENT '请求数据类型',
  `request_data` json NULL COMMENT '请求数据',
  `request_headers` json NULL COMMENT '请求头',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `del_flag` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '删除标志（0代表存在 2代表删除）',
  PRIMARY KEY (`api_id`) USING BTREE,
  INDEX `ix_api_info_api_name`(`api_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 101 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '接口表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_info
-- ----------------------------
INSERT INTO `api_info` VALUES (1, '查询倾角图表', 3, 'POST', 'https://www.convercomm.com/api/admin/packetInfo/getDevicePacketChart', '0', 'P0', '[]', 1, '{\"imei\": \"BD012307272000FB\", \"endTime\": \"2024-04-08 23:59:59\", \"startTime\": \"2024-04-01 00:00:00\"}', '{\"Authorization\": \"Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyYW5fMDAxIiwidXNlcklkIjoiNDk2IiwibmFtZSI6InJhbl8wMDEiLCJpZCI6IjFhQ1dacjdEIiwiZXhwIjoxNzMwNjQzODQzfQ.G5PkcS1NTuC2rNdNV78jUFro5y-sqFifHEW2G-5AliUds1Ye0e0vCLlsvPDC_XupwT0dmKbnE4YyKtVLF35FOzj42X0xbeZcPNkr3IEUHICBKEMyjqLUsRq_HOPZcY2EKmO4xV-yJFFR2IWyixHUC465oU9F9f2OlThV_sU6QhU\"}', 'admin', '2024-10-24 22:06:52', 'admin', '2024-10-24 22:06:52', '', '0');
INSERT INTO `api_info` VALUES (2, '登录', 3, 'POST', 'https://www.convercomm.com//api/auth/jwt/miniLogin', '0', 'P0', '[]', 1, '{\"password\": \"3H/5JXwqnCGKh+s=\", \"username\": \"ran_dev\"}', '{}', 'admin', '2024-10-24 22:06:52', 'admin', '2024-10-24 22:06:52', '', '0');
INSERT INTO `api_info` VALUES (3, 'string', 0, 'GET', 'string', '0', 'P0', '[]', 0, '{}', '{}', 'admin', '2024-10-24 23:33:18', 'admin', '2024-10-24 23:33:18', 'string', '0');
INSERT INTO `api_info` VALUES (99, '登录接口', 17, 'DELETE', '/login', '0', 'P0', '[\"登录\"]', 0, '{}', '{}', 'admin', '2024-10-26 16:33:36', 'admin', '2024-10-26 16:37:24', '这是一个编辑功能', '0');
INSERT INTO `api_info` VALUES (100, 'restart', 17, 'POST', '/restart', '0', 'P0', '[]', 0, '{}', '{}', 'admin', '2024-10-26 16:47:43', 'admin', '2024-10-26 16:47:43', '', '0');
INSERT INTO `api_info` VALUES (101, '111', 17, 'POST', '111', '0', 'P0', '[]', 0, '{}', '{}', 'admin', '2024-10-26 16:47:59', 'admin', '2024-10-26 16:47:59', '', '0');

-- ----------------------------
-- Table structure for apscheduler_jobs
-- ----------------------------
DROP TABLE IF EXISTS `apscheduler_jobs`;
CREATE TABLE `apscheduler_jobs`  (
  `id` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `next_run_time` double NULL DEFAULT NULL,
  `job_state` blob NOT NULL,
  `del_flag` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '删除标志（0代表存在 2代表删除）',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_apscheduler_jobs_next_run_time`(`next_run_time`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of apscheduler_jobs
-- ----------------------------

-- ----------------------------
-- Table structure for data_source
-- ----------------------------
DROP TABLE IF EXISTS `data_source`;
CREATE TABLE `data_source`  (
  `datasource_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '数据源ID',
  `datasource_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据源名称',
  `datasource_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据源类型',
  `datasource_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据源地址',
  `datasource_port` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据源端口',
  `datasource_user` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据源用户名',
  `datasource_pwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据源密码',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `del_flag` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '删除标志（0代表存在 2代表删除）',
  PRIMARY KEY (`datasource_id`) USING BTREE,
  INDEX `ix_data_source_datasource_name`(`datasource_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '数据源配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of data_source
-- ----------------------------
INSERT INTO `data_source` VALUES (1, '本地数据库', 'mysql', '192.168.1.243', '3306', 'root', 'gAAAAABnDh7xQd7yE0F342INWrA8mTLC2Tb8LXyqsAUKGz7Aj55gwdW5NwvDTTnqWpnrHzTJcBHzZUckTkciL4gmNmDsTr7rqg==', 'admin', '2024-09-21 15:53:47', 'admin', '2024-10-15 15:51:25', '本地数据库测试连接', NULL);
INSERT INTO `data_source` VALUES (6, '测试加密', 'mysql', '127.0.0.1', '3306', 'root', 'gAAAAABnDiHDT-8sdkTyWVogae6BGNbx7G0eh1pUsgfXqkrza24J3ainH09QoI0c0s6wWxycHVPlXi7L-Gu9ATEgl8gNM4dsxA==', 'admin', '2024-09-22 01:04:36', 'admin', '2024-10-15 16:03:15', '', NULL);
INSERT INTO `data_source` VALUES (8, 'Docker 数据库', 'mysql', 'beidoulab.club', '62387', 'root', 'gAAAAABnE11wnZm0AKb7nRJv3o9LMLQOADyDTWuFZ6gb21mFrt5bRYDJzxyfDYc58TxX4DLkXxPmdyhVIKhZc8tLFJPF8PWPkA==', 'admin', '2024-10-19 15:19:12', 'admin', '2024-10-19 15:19:12', '', NULL);

-- ----------------------------
-- Table structure for demo
-- ----------------------------
DROP TABLE IF EXISTS `demo`;
CREATE TABLE `demo`  (
  `user_id` bigint(0) NOT NULL COMMENT '用户ID',
  `post_id` bigint(0) NOT NULL COMMENT '岗位ID',
  PRIMARY KEY (`user_id`, `post_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户与岗位关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of demo
-- ----------------------------

-- ----------------------------
-- Table structure for env_info
-- ----------------------------
DROP TABLE IF EXISTS `env_info`;
CREATE TABLE `env_info`  (
  `env_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '环境ID',
  `env_name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环境名称',
  `env_url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环境地址',
  `env_variables` json NULL COMMENT '环境变量',
  `env_headers` json NULL COMMENT '环境请求头',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `del_flag` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '删除标志（0代表存在 2代表删除）',
  PRIMARY KEY (`env_id`) USING BTREE,
  INDEX `ix_env_info_env_name`(`env_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 100 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '环境表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of env_info
-- ----------------------------
INSERT INTO `env_info` VALUES (1, '测试环境', 'https://beidoulab.club:5557/', '{}', '{}', 'admin', '2024-10-30 22:54:51', 'admin', '2024-10-30 22:54:51', '', NULL);
INSERT INTO `env_info` VALUES (2, '正式环境', 'https://convercomm.com/', '{}', '{}', 'admin', '2024-10-30 22:56:38', 'admin', '2024-10-30 22:56:38', '', NULL);
INSERT INTO `env_info` VALUES (46, '眼', 'https://beidoulab.club:5557/', '{}', '{}', 'admin', '2024-10-31 22:47:50', 'admin', '2024-10-31 22:47:50', '', NULL);
INSERT INTO `env_info` VALUES (61, '方', 'https://beidoulab.club:5557/', '{}', '{}', 'admin', '2024-10-31 22:47:49', 'admin', '2024-10-31 22:47:49', '', NULL);
INSERT INTO `env_info` VALUES (100, '好 123', 'https:www.hao123.com', '{}', '{}', 'admin', '2024-10-31 23:39:40', 'admin', '2024-10-31 23:39:40', '', NULL);

-- ----------------------------
-- Table structure for gen_table
-- ----------------------------
DROP TABLE IF EXISTS `gen_table`;
CREATE TABLE `gen_table`  (
  `table_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `table_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '' COMMENT '表名称',
  `table_comment` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '' COMMENT '表描述',
  `sub_table_name` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '关联子表的表名',
  `sub_table_fk_name` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '子表关联的外键名',
  `class_name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '' COMMENT '实体类名称',
  `tpl_category` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT 'crud' COMMENT '使用的模板（crud单表操作 tree树表操作）',
  `tpl_web_type` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '' COMMENT '前端模板类型（element-ui模版 element-plus模版）',
  `package_name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '生成包路径',
  `module_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '生成模块名',
  `business_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '生成业务名',
  `function_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '生成功能名',
  `function_author` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '生成功能作者',
  `gen_type` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '0' COMMENT '生成代码方式（0zip压缩包 1自定义路径）',
  `gen_path` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '/' COMMENT '生成路径（不填默认项目路径）',
  `options` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '其它生成选项',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`table_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '代码生成业务表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of gen_table
-- ----------------------------
INSERT INTO `gen_table` VALUES (5, 'demo', '用户与岗位关联表', NULL, NULL, 'Demo', 'crud', 'element-plus', 'module_admin.system', 'system', 'demo', '用户与岗位关联', '冉勇', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": null}', 'admin', '2025-02-21 16:36:17', 'admin', '2025-04-14 14:01:09', NULL);

-- ----------------------------
-- Table structure for gen_table_column
-- ----------------------------
DROP TABLE IF EXISTS `gen_table_column`;
CREATE TABLE `gen_table_column`  (
  `column_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `table_id` bigint(0) NULL DEFAULT NULL COMMENT '归属表编号',
  `column_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '列名称',
  `column_comment` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '列描述',
  `column_type` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '列类型',
  `python_type` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT 'PYTHON类型',
  `python_field` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT 'PYTHON字段名',
  `is_pk` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '是否主键（1是）',
  `is_increment` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '是否自增（1是）',
  `is_required` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '是否必填（1是）',
  `is_unique` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '是否唯一（1是）',
  `is_insert` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '是否为插入字段（1是）',
  `is_edit` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '是否编辑字段（1是）',
  `is_list` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '是否列表字段（1是）',
  `is_query` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '是否查询字段（1是）',
  `query_type` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT 'EQ' COMMENT '查询方式（等于、不等于、大于、小于、范围）',
  `html_type` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）',
  `dict_type` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '' COMMENT '字典类型',
  `sort` int(0) NULL DEFAULT NULL COMMENT '排序',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`column_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 50 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '代码生成业务表字段' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of gen_table_column
-- ----------------------------
INSERT INTO `gen_table_column` VALUES (48, 5, 'user_id', '用户ID', 'bigint', 'int', 'userId', '1', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 1, 'admin', NULL, 'admin', '2025-04-14 14:01:09');
INSERT INTO `gen_table_column` VALUES (49, 5, 'post_id', '岗位ID', 'bigint', 'int', 'postId', '1', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 2, 'admin', NULL, 'admin', '2025-04-14 14:01:09');

-- ----------------------------
-- Table structure for project_info
-- ----------------------------
DROP TABLE IF EXISTS `project_info`;
CREATE TABLE `project_info`  (
  `project_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '项目ID',
  `project_name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目名称',
  `responsible_name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '负责人',
  `test_user` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '测试人员',
  `dev_user` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '开发人员',
  `publish_app` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '发布应用',
  `simple_desc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '简要描述',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`project_id`) USING BTREE,
  INDEX `ix_project_info_project_name`(`project_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '项目表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of project_info
-- ----------------------------
INSERT INTO `project_info` VALUES (1, '123123', 'string', 'string', 'string', 'string', 'string', 'string', '2024-09-15 09:00:39', 'admin', '2024-09-15 17:00:44', 'string');
INSERT INTO `project_info` VALUES (2, '反无', '冉勇', '冉勇_测试', '冉勇_开发', 'web', '这是一个描述', 'admin', '2024-09-04 10:50:42', 'admin', '2024-09-04 10:50:42', '这是一个备注');
INSERT INTO `project_info` VALUES (3, '异动通', '冉勇', '冉勇_测试', '冉勇_开发', 'web', '这是一个描述', 'admin', '2024-09-04 10:50:42', 'admin', '2024-09-10 21:54:43', '这是一个备注');
INSERT INTO `project_info` VALUES (7, '冉勇', 'string', 'asda', 'string', 'string', 'string', 'admin', '2024-09-15 22:08:28', 'admin', '2024-09-15 22:09:03', 'string');
INSERT INTO `project_info` VALUES (14, '！@#！#', '！@#！#', '！@#！#', '！@#！#', '！@#！#', '', 'admin', '2024-09-10 21:57:14', 'admin', '2024-09-10 21:57:14', '');
INSERT INTO `project_info` VALUES (15, '1111111111', '2222222222', '4444444444', '3333333333', '5555555555', '9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999', 'admin', '2024-09-10 22:36:27', 'admin', '2024-09-10 22:36:27', '8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888');
INSERT INTO `project_info` VALUES (17, '测试项目', '冉勇', '冉勇', '冉勇', 'web', '这是一个描述', 'admin', '2024-09-16 10:06:07', 'admin', '2024-09-20 22:31:33', '这是一个备注放放风1');

-- ----------------------------
-- Table structure for robot_conf
-- ----------------------------
DROP TABLE IF EXISTS `robot_conf`;
CREATE TABLE `robot_conf`  (
  `robot_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '机器人ID',
  `robot_name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '机器人名称',
  `robot_webhook` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '机器人WebHook',
  `robot_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '机器人类型',
  `robot_template` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '机器人通知模板',
  `robot_status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '机器人状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`robot_id`) USING BTREE,
  INDEX `ix_robot_conf_robot_name`(`robot_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '机器人配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of robot_conf
-- ----------------------------
INSERT INTO `robot_conf` VALUES (1, '企业微信机器人1', 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=55e6d5bc-61fc-4d26-9615-01ab51c82801', 'Wx_bot', '**${name}**\n项目：${project_name}\n时间：${start_time} ～ ${end_date}\n共测试：${run_count}次\n通过数：${run_success_count}\n异常数：${run_err_count}\n失败数：${run_fail_count}\n测试通过率：${rate}%\n详细统计：[点击查看](${url})', '0', 'admin', '2024-09-28 17:35:47', 'admin', '2024-09-28 17:46:11', '这是一个备注');
INSERT INTO `robot_conf` VALUES (2, '企业微信机器人2', 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=55e6d5bc-61fc-4d26-9615-01ab51c82801', 'Wx_bot', '**${name}**\n项目：${project_name}\n时间：${start_time} ～ ${end_date}\n共测试：${run_count}次\n通过数：${run_success_count}\n异常数：${run_err_count}\n失败数：${run_fail_count}\n测试通过率：${rate}%\n详细统计：[点击查看](${url})', '1', 'admin', '2024-09-16 16:54:40', 'admin', '2024-09-28 17:36:19', '这是一个备注');
INSERT INTO `robot_conf` VALUES (6, '企业微信机器人62', 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=55e6d5bc-61fc-4d26-9615-01ab51c82801', 'Wx_bot', '**${name}**\n项目：${project_name}\n时间：${start_time} ～ ${end_date}\n共测试：${run_count}次\n通过数：${run_success_count}\n异常数：${run_err_count}\n失败数：${run_fail_count}\n测试通过率：${rate}%\n详细统计：[点击查看](${url})', '0', 'admin', '2024-09-29 17:16:45', 'admin', '2024-09-29 17:16:45', '这是一个备注');

-- ----------------------------
-- Table structure for sys_config
-- ----------------------------
DROP TABLE IF EXISTS `sys_config`;
CREATE TABLE `sys_config`  (
  `config_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '参数主键',
  `config_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '参数名称',
  `config_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '参数键名',
  `config_value` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '参数键值',
  `config_type` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'N' COMMENT '系统内置（Y是 N否）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`config_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 101 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '参数配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_config
-- ----------------------------
INSERT INTO `sys_config` VALUES (1, '主框架页-默认皮肤样式名称', 'sys.index.skinName', 'skin-blue', 'Y', 'admin', '2024-08-13 18:18:19', '', NULL, '蓝色 skin-blue、绿色 skin-green、紫色 skin-purple、红色 skin-red、黄色 skin-yellow');
INSERT INTO `sys_config` VALUES (2, '用户管理-账号初始密码', 'sys.user.initPassword', '123456', 'Y', 'admin', '2024-08-13 18:18:19', '', NULL, '初始化密码 123456');
INSERT INTO `sys_config` VALUES (3, '主框架页-侧边栏主题', 'sys.index.sideTheme', 'theme-dark', 'Y', 'admin', '2024-08-13 18:18:19', '', NULL, '深色主题theme-dark，浅色主题theme-light');
INSERT INTO `sys_config` VALUES (4, '账号自助-验证码开关', 'sys.account.captchaEnabled', 'true', 'Y', 'admin', '2024-08-13 18:18:19', '', NULL, '是否开启验证码功能（true开启，false关闭）');
INSERT INTO `sys_config` VALUES (5, '账号自助-是否开启用户注册功能', 'sys.account.registerUser', 'true', 'Y', 'admin', '2024-08-13 18:18:19', '', NULL, '是否开启注册用户功能（true开启，false关闭）');
INSERT INTO `sys_config` VALUES (6, '用户登录-黑名单列表', 'sys.login.blackIPList', '', 'Y', 'admin', '2024-08-13 18:18:19', '', NULL, '设置登录IP黑名单限制，多个匹配项以;分隔，支持匹配（*通配、网段）');

-- ----------------------------
-- Table structure for sys_dept
-- ----------------------------
DROP TABLE IF EXISTS `sys_dept`;
CREATE TABLE `sys_dept`  (
  `dept_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '部门id',
  `parent_id` bigint(0) NULL DEFAULT 0 COMMENT '父部门id',
  `ancestors` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '祖级列表',
  `dept_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '部门名称',
  `order_num` int(0) NULL DEFAULT 0 COMMENT '显示顺序',
  `leader` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '负责人',
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '联系电话',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '部门状态（0正常 1停用）',
  `del_flag` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`dept_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 201 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '部门表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dept
-- ----------------------------
INSERT INTO `sys_dept` VALUES (100, 0, '0', 'Sakura_k', 0, '年糕', '15888888888', 'niangao@qq.com', '0', '0', 'admin', '2024-08-13 18:18:19', 'admin', '2024-08-15 11:31:23');
INSERT INTO `sys_dept` VALUES (101, 100, '0,100', '深圳分公司', 1, '年糕', '15888888888', 'niangao@qq.com', '0', '0', 'admin', '2024-08-13 18:18:19', '', NULL);
INSERT INTO `sys_dept` VALUES (102, 100, '0,100', '长沙分公司', 2, '年糕', '15888888888', 'niangao@qq.com', '0', '2', 'admin', '2024-08-13 18:18:19', NULL, NULL);
INSERT INTO `sys_dept` VALUES (103, 101, '0,100,101', '研发部门', 1, '年糕', '15888888888', 'niangao@qq.com', '0', '0', 'admin', '2024-08-13 18:18:19', '', NULL);
INSERT INTO `sys_dept` VALUES (104, 101, '0,100,101', '市场部门', 2, '年糕', '15888888888', 'niangao@qq.com', '0', '2', 'admin', '2024-08-13 18:18:19', NULL, NULL);
INSERT INTO `sys_dept` VALUES (105, 101, '0,100,101', '测试部门', 2, '年糕', '15888888888', 'niangao@qq.com', '0', '0', 'admin', '2024-08-13 18:18:19', 'admin', '2024-09-20 22:42:40');
INSERT INTO `sys_dept` VALUES (106, 101, '0,100,101', '财务部门', 4, '年糕', '15888888888', 'niangao@qq.com', '0', '2', 'admin', '2024-08-13 18:18:19', NULL, NULL);
INSERT INTO `sys_dept` VALUES (107, 101, '0,100,101', '运维部门', 5, '年糕', '15888888888', 'niangao@qq.com', '0', '2', 'admin', '2024-08-13 18:18:19', NULL, NULL);
INSERT INTO `sys_dept` VALUES (108, 102, '0,100,102', '市场部门', 1, '年糕', '15888888888', 'niangao@qq.com', '0', '2', 'admin', '2024-08-13 18:18:19', NULL, NULL);
INSERT INTO `sys_dept` VALUES (109, 102, '0,100,102', '财务部门', 2, '年糕', '15888888888', 'niangao@qq.com', '0', '2', 'admin', '2024-08-13 18:18:19', NULL, NULL);
INSERT INTO `sys_dept` VALUES (200, 101, '0,100,101', 'demo', 0, '1', '13206269804', '1111@qq.com', '1', '2', 'admin', '2024-08-15 11:31:41', NULL, NULL);

-- ----------------------------
-- Table structure for sys_dict_data
-- ----------------------------
DROP TABLE IF EXISTS `sys_dict_data`;
CREATE TABLE `sys_dict_data`  (
  `dict_code` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '字典编码',
  `dict_sort` int(0) NULL DEFAULT 0 COMMENT '字典排序',
  `dict_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '字典标签',
  `dict_value` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '字典键值',
  `dict_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '字典类型',
  `css_class` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '样式属性（其他样式扩展）',
  `list_class` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '表格回显样式',
  `is_default` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'N' COMMENT '是否默认（Y是 N否）',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`dict_code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 104 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '字典数据表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dict_data
-- ----------------------------
INSERT INTO `sys_dict_data` VALUES (1, 1, '男', '0', 'sys_user_sex', '', '', 'Y', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '性别男');
INSERT INTO `sys_dict_data` VALUES (2, 2, '女', '1', 'sys_user_sex', '', '', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '性别女');
INSERT INTO `sys_dict_data` VALUES (3, 3, '未知', '2', 'sys_user_sex', '', '', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '性别未知');
INSERT INTO `sys_dict_data` VALUES (4, 1, '显示', '0', 'sys_show_hide', '', 'primary', 'Y', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '显示菜单');
INSERT INTO `sys_dict_data` VALUES (5, 2, '隐藏', '1', 'sys_show_hide', '', 'danger', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '隐藏菜单');
INSERT INTO `sys_dict_data` VALUES (6, 1, '正常', '0', 'sys_normal_disable', '', 'primary', 'Y', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '正常状态');
INSERT INTO `sys_dict_data` VALUES (7, 2, '停用', '1', 'sys_normal_disable', '', 'danger', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '停用状态');
INSERT INTO `sys_dict_data` VALUES (8, 1, '正常', '0', 'sys_job_status', '', 'primary', 'Y', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '正常状态');
INSERT INTO `sys_dict_data` VALUES (9, 2, '暂停', '1', 'sys_job_status', '', 'danger', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '停用状态');
INSERT INTO `sys_dict_data` VALUES (10, 1, '默认', 'default', 'sys_job_group', '', '', 'Y', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '默认分组');
INSERT INTO `sys_dict_data` VALUES (11, 2, '数据库', 'sqlalchemy', 'sys_job_group', '', '', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '数据库分组');
INSERT INTO `sys_dict_data` VALUES (12, 3, 'redis', 'redis', 'sys_job_group', '', '', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, 'reids分组');
INSERT INTO `sys_dict_data` VALUES (13, 1, '默认', 'default', 'sys_job_executor', '', '', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '线程池');
INSERT INTO `sys_dict_data` VALUES (14, 2, '进程池', 'processpool', 'sys_job_executor', '', '', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '进程池');
INSERT INTO `sys_dict_data` VALUES (15, 1, '是', 'Y', 'sys_yes_no', '', 'primary', 'Y', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '系统默认是');
INSERT INTO `sys_dict_data` VALUES (16, 2, '否', 'N', 'sys_yes_no', '', 'danger', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '系统默认否');
INSERT INTO `sys_dict_data` VALUES (17, 1, '通知', '1', 'sys_notice_type', '', 'warning', 'Y', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '通知');
INSERT INTO `sys_dict_data` VALUES (18, 2, '公告', '2', 'sys_notice_type', '', 'success', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '公告');
INSERT INTO `sys_dict_data` VALUES (19, 1, '正常', '0', 'sys_notice_status', '', 'primary', 'Y', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '正常状态');
INSERT INTO `sys_dict_data` VALUES (20, 2, '关闭', '1', 'sys_notice_status', '', 'danger', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '关闭状态');
INSERT INTO `sys_dict_data` VALUES (21, 99, '其他', '0', 'sys_oper_type', '', 'info', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '其他操作');
INSERT INTO `sys_dict_data` VALUES (22, 1, '新增', '1', 'sys_oper_type', '', 'info', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '新增操作');
INSERT INTO `sys_dict_data` VALUES (23, 2, '修改', '2', 'sys_oper_type', '', 'info', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '修改操作');
INSERT INTO `sys_dict_data` VALUES (24, 3, '删除', '3', 'sys_oper_type', '', 'danger', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '删除操作');
INSERT INTO `sys_dict_data` VALUES (25, 4, '授权', '4', 'sys_oper_type', '', 'primary', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '授权操作');
INSERT INTO `sys_dict_data` VALUES (26, 5, '导出', '5', 'sys_oper_type', '', 'warning', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '导出操作');
INSERT INTO `sys_dict_data` VALUES (27, 6, '导入', '6', 'sys_oper_type', '', 'warning', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '导入操作');
INSERT INTO `sys_dict_data` VALUES (28, 7, '强退', '7', 'sys_oper_type', '', 'danger', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '强退操作');
INSERT INTO `sys_dict_data` VALUES (29, 8, '生成代码', '8', 'sys_oper_type', '', 'warning', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '生成操作');
INSERT INTO `sys_dict_data` VALUES (30, 9, '清空数据', '9', 'sys_oper_type', '', 'danger', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '清空操作');
INSERT INTO `sys_dict_data` VALUES (31, 1, '成功', '0', 'sys_common_status', '', 'primary', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '正常状态');
INSERT INTO `sys_dict_data` VALUES (32, 2, '失败', '1', 'sys_common_status', '', 'danger', 'N', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '停用状态');
INSERT INTO `sys_dict_data` VALUES (102, 1, '成功', '0', 'run_status', NULL, 'primary', 'N', '0', 'admin', '2025-01-04 14:25:26', 'admin', '2025-01-04 14:25:26', '成功状态');
INSERT INTO `sys_dict_data` VALUES (103, 2, '失败', '1', 'run_status', NULL, 'danger', 'N', '0', 'admin', '2025-01-04 14:25:55', 'admin', '2025-01-04 14:25:59', '失败状态');

-- ----------------------------
-- Table structure for sys_dict_type
-- ----------------------------
DROP TABLE IF EXISTS `sys_dict_type`;
CREATE TABLE `sys_dict_type`  (
  `dict_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '字典主键',
  `dict_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '字典名称',
  `dict_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '字典类型',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`dict_id`) USING BTREE,
  UNIQUE INDEX `dict_type`(`dict_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 102 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '字典类型表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dict_type
-- ----------------------------
INSERT INTO `sys_dict_type` VALUES (1, '用户性别', 'sys_user_sex', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '用户性别列表');
INSERT INTO `sys_dict_type` VALUES (2, '菜单状态', 'sys_show_hide', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '菜单状态列表');
INSERT INTO `sys_dict_type` VALUES (3, '系统开关', 'sys_normal_disable', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '系统开关列表');
INSERT INTO `sys_dict_type` VALUES (4, '任务状态', 'sys_job_status', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '任务状态列表');
INSERT INTO `sys_dict_type` VALUES (5, '任务分组', 'sys_job_group', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '任务分组列表');
INSERT INTO `sys_dict_type` VALUES (6, '任务执行器', 'sys_job_executor', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '任务执行器列表');
INSERT INTO `sys_dict_type` VALUES (7, '系统是否', 'sys_yes_no', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '系统是否列表');
INSERT INTO `sys_dict_type` VALUES (8, '通知类型', 'sys_notice_type', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '通知类型列表');
INSERT INTO `sys_dict_type` VALUES (9, '通知状态', 'sys_notice_status', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '通知状态列表');
INSERT INTO `sys_dict_type` VALUES (10, '操作类型', 'sys_oper_type', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '操作类型列表');
INSERT INTO `sys_dict_type` VALUES (11, '系统状态', 'sys_common_status', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '登录状态列表');
INSERT INTO `sys_dict_type` VALUES (101, '运行状态', 'run_status', '0', 'admin', '2025-01-04 14:24:49', 'admin', '2025-01-04 14:24:49', '运行测试用例返回结果');

-- ----------------------------
-- Table structure for sys_job
-- ----------------------------
DROP TABLE IF EXISTS `sys_job`;
CREATE TABLE `sys_job`  (
  `job_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `job_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '任务名称',
  `job_group` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'default' COMMENT '任务组名',
  `job_executor` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'default' COMMENT '任务执行器',
  `invoke_target` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '调用目标字符串',
  `job_args` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '位置参数',
  `job_kwargs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '关键字参数',
  `cron_expression` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT 'cron执行表达式',
  `misfire_policy` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '3' COMMENT '计划执行错误策略（1立即执行 2执行一次 3放弃执行）',
  `concurrent` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '1' COMMENT '是否并发执行（0允许 1禁止）',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '状态（0正常 1暂停）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '备注信息',
  PRIMARY KEY (`job_id`, `job_name`, `job_group`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 103 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '定时任务调度表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_job
-- ----------------------------
INSERT INTO `sys_job` VALUES (1, '系统默认（无参）', 'default', 'default', 'module_task.scheduler_test.job', NULL, NULL, '0/10 * * * * ?', '3', '1', '1', 'admin', '2024-08-06 10:15:16', '', NULL, '');
INSERT INTO `sys_job` VALUES (2, '系统默认（有参）', 'default', 'default', 'module_task.scheduler_test.job', 'test', NULL, '0/15 * * * * ?', '3', '1', '1', 'admin', '2024-08-06 10:15:16', '', NULL, '');
INSERT INTO `sys_job` VALUES (3, '系统默认（多参）', 'default', 'default', 'module_task.scheduler_test.job', 'new', '{\"test\": 111}', '0/20 * * * * ?', '3', '1', '1', 'admin', '2024-08-06 10:15:16', '', NULL, '');
INSERT INTO `sys_job` VALUES (4, '系统默认异步（无参）', 'default', 'default', 'module_task.scheduler_test.async_job', '', '', '0/10 * * * * ?', '1', '1', '1', 'admin', '2024-11-14 11:19:00', 'admin', '2024-11-14 11:19:48', NULL);
INSERT INTO `sys_job` VALUES (5, '系统默认异步（有参）', 'default', 'default', 'module_task.scheduler_test.async_job', 'test', '', '0/15 * * * * ?', '1', '1', '1', 'admin', '2024-11-14 11:21:03', 'admin', '2024-11-14 11:21:43', NULL);
INSERT INTO `sys_job` VALUES (6, '系统默认异步（多参）', 'default', 'default', 'module_task.scheduler_test.async_job', 'new', '{\"test\":111}', '0/20 * * * * ?', '1', '1', '1', 'admin', '2024-11-14 11:25:48', 'admin', '2024-11-14 11:26:09', NULL);
INSERT INTO `sys_job` VALUES (7, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log.log', '', '', '0 0 0 * * ?', '1', '1', '0', 'admin', '2024-08-06 10:50:16', 'admin', '2024-08-23 00:24:19', '');

-- ----------------------------
-- Table structure for sys_job_log
-- ----------------------------
DROP TABLE IF EXISTS `sys_job_log`;
CREATE TABLE `sys_job_log`  (
  `job_log_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '任务日志ID',
  `job_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '任务名称',
  `job_group` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '任务组名',
  `job_executor` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '任务执行器',
  `invoke_target` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '调用目标字符串',
  `job_args` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '位置参数',
  `job_kwargs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '关键字参数',
  `job_trigger` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '任务触发器',
  `job_message` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '日志信息',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '执行状态（0正常 1失败）',
  `exception_info` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '异常信息',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`job_log_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 213 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '定时任务调度日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_job_log
-- ----------------------------
INSERT INTO `sys_job_log` VALUES (139, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-23 00:00:00', '0', '', '2024-11-23 00:00:00');
INSERT INTO `sys_job_log` VALUES (140, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-23 00:00:00', '0', '', '2024-11-23 00:00:00');
INSERT INTO `sys_job_log` VALUES (141, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-24 00:00:00', '0', '', '2024-11-24 00:00:00');
INSERT INTO `sys_job_log` VALUES (142, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-24 00:00:00', '0', '', '2024-11-24 00:00:00');
INSERT INTO `sys_job_log` VALUES (143, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-25 00:00:00', '0', '', '2024-11-25 00:00:00');
INSERT INTO `sys_job_log` VALUES (144, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-25 00:00:00', '0', '', '2024-11-25 00:00:00');
INSERT INTO `sys_job_log` VALUES (145, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-26 00:00:00', '0', '', '2024-11-26 00:00:00');
INSERT INTO `sys_job_log` VALUES (146, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-26 00:00:00', '0', '', '2024-11-26 00:00:00');
INSERT INTO `sys_job_log` VALUES (147, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-27 00:00:00', '0', '', '2024-11-27 00:00:00');
INSERT INTO `sys_job_log` VALUES (148, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-27 00:00:00', '0', '', '2024-11-27 00:00:00');
INSERT INTO `sys_job_log` VALUES (149, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-28 00:00:00', '0', '', '2024-11-28 00:00:00');
INSERT INTO `sys_job_log` VALUES (150, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-28 00:00:00', '0', '', '2024-11-28 00:00:00');
INSERT INTO `sys_job_log` VALUES (151, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-29 00:00:00', '0', '', '2024-11-29 00:00:00');
INSERT INTO `sys_job_log` VALUES (152, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-29 00:00:00', '0', '', '2024-11-29 00:00:00');
INSERT INTO `sys_job_log` VALUES (153, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-30 00:00:00', '0', '', '2024-11-30 00:00:00');
INSERT INTO `sys_job_log` VALUES (154, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-11-30 00:00:00', '0', '', '2024-11-30 00:00:00');
INSERT INTO `sys_job_log` VALUES (155, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-01 00:00:00', '0', '', '2024-12-01 00:00:00');
INSERT INTO `sys_job_log` VALUES (156, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-01 00:00:00', '0', '', '2024-12-01 00:00:00');
INSERT INTO `sys_job_log` VALUES (157, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-02 00:00:00', '0', '', '2024-12-02 00:00:00');
INSERT INTO `sys_job_log` VALUES (158, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-02 00:00:00', '0', '', '2024-12-02 00:00:00');
INSERT INTO `sys_job_log` VALUES (159, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-03 00:00:00', '0', '', '2024-12-03 00:00:00');
INSERT INTO `sys_job_log` VALUES (160, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-03 00:00:00', '0', '', '2024-12-03 00:00:00');
INSERT INTO `sys_job_log` VALUES (161, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-04 00:00:00', '0', '', '2024-12-04 00:00:00');
INSERT INTO `sys_job_log` VALUES (162, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-04 00:00:00', '0', '', '2024-12-04 00:00:00');
INSERT INTO `sys_job_log` VALUES (163, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-05 00:00:00', '0', '', '2024-12-05 00:00:00');
INSERT INTO `sys_job_log` VALUES (164, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-05 00:00:00', '0', '', '2024-12-05 00:00:00');
INSERT INTO `sys_job_log` VALUES (165, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-06 00:00:00', '0', '', '2024-12-06 00:00:00');
INSERT INTO `sys_job_log` VALUES (166, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-06 00:00:00', '0', '', '2024-12-06 00:00:00');
INSERT INTO `sys_job_log` VALUES (167, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-07 00:00:00', '0', '', '2024-12-07 00:00:00');
INSERT INTO `sys_job_log` VALUES (168, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-07 00:00:00', '0', '', '2024-12-07 00:00:00');
INSERT INTO `sys_job_log` VALUES (169, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-08 00:00:00', '0', '', '2024-12-08 00:00:00');
INSERT INTO `sys_job_log` VALUES (170, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-08 00:00:00', '0', '', '2024-12-08 00:00:00');
INSERT INTO `sys_job_log` VALUES (171, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-09 00:00:00', '0', '', '2024-12-09 00:00:00');
INSERT INTO `sys_job_log` VALUES (172, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-09 00:00:00', '0', '', '2024-12-09 00:00:00');
INSERT INTO `sys_job_log` VALUES (173, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-10 00:00:00', '0', '', '2024-12-10 00:00:00');
INSERT INTO `sys_job_log` VALUES (174, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-10 00:00:00', '0', '', '2024-12-10 00:00:00');
INSERT INTO `sys_job_log` VALUES (175, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-11 00:00:00', '0', '', '2024-12-11 00:00:00');
INSERT INTO `sys_job_log` VALUES (176, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-11 00:00:00', '0', '', '2024-12-11 00:00:00');
INSERT INTO `sys_job_log` VALUES (177, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-12 00:00:00', '0', '', '2024-12-12 00:00:00');
INSERT INTO `sys_job_log` VALUES (178, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-12 00:00:00', '0', '', '2024-12-12 00:00:00');
INSERT INTO `sys_job_log` VALUES (179, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-13 00:00:00', '0', '', '2024-12-13 00:00:00');
INSERT INTO `sys_job_log` VALUES (180, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-13 00:00:00', '0', '', '2024-12-13 00:00:00');
INSERT INTO `sys_job_log` VALUES (181, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-14 00:00:00', '0', '', '2024-12-14 00:00:00');
INSERT INTO `sys_job_log` VALUES (182, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-14 00:00:00', '0', '', '2024-12-14 00:00:00');
INSERT INTO `sys_job_log` VALUES (183, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-15 00:00:00', '0', '', '2024-12-15 00:00:00');
INSERT INTO `sys_job_log` VALUES (184, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-15 00:00:00', '0', '', '2024-12-15 00:00:00');
INSERT INTO `sys_job_log` VALUES (185, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-16 00:00:00', '0', '', '2024-12-16 00:00:00');
INSERT INTO `sys_job_log` VALUES (186, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-16 00:00:00', '0', '', '2024-12-16 00:00:00');
INSERT INTO `sys_job_log` VALUES (187, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-17 00:00:00', '0', '', '2024-12-17 00:00:00');
INSERT INTO `sys_job_log` VALUES (188, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-17 00:00:00', '0', '', '2024-12-17 00:00:00');
INSERT INTO `sys_job_log` VALUES (189, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-18 00:00:00', '0', '', '2024-12-18 00:00:00');
INSERT INTO `sys_job_log` VALUES (190, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-18 00:00:00', '0', '', '2024-12-18 00:00:00');
INSERT INTO `sys_job_log` VALUES (191, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-19 00:00:00', '0', '', '2024-12-19 00:00:00');
INSERT INTO `sys_job_log` VALUES (192, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-19 00:00:00', '0', '', '2024-12-19 00:00:00');
INSERT INTO `sys_job_log` VALUES (193, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-20 00:00:00', '0', '', '2024-12-20 00:00:00');
INSERT INTO `sys_job_log` VALUES (194, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-20 00:00:00', '0', '', '2024-12-20 00:00:00');
INSERT INTO `sys_job_log` VALUES (195, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-21 00:00:00', '0', '', '2024-12-21 00:00:00');
INSERT INTO `sys_job_log` VALUES (196, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-21 00:00:00', '0', '', '2024-12-21 00:00:00');
INSERT INTO `sys_job_log` VALUES (197, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-22 00:00:00', '0', '', '2024-12-22 00:00:00');
INSERT INTO `sys_job_log` VALUES (198, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-22 00:00:00', '0', '', '2024-12-22 00:00:00');
INSERT INTO `sys_job_log` VALUES (199, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-23 00:00:00', '0', '', '2024-12-23 00:00:00');
INSERT INTO `sys_job_log` VALUES (200, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-23 00:00:00', '0', '', '2024-12-23 00:00:00');
INSERT INTO `sys_job_log` VALUES (201, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-24 00:00:00', '0', '', '2024-12-24 00:00:00');
INSERT INTO `sys_job_log` VALUES (202, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2024-12-24 00:00:00', '0', '', '2024-12-24 00:00:00');
INSERT INTO `sys_job_log` VALUES (203, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2025-01-11 00:00:00', '0', '', '2025-01-11 00:00:00');
INSERT INTO `sys_job_log` VALUES (204, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2025-01-11 00:00:00', '0', '', '2025-01-11 00:00:00');
INSERT INTO `sys_job_log` VALUES (205, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2025-01-12 00:00:00', '0', '', '2025-01-12 00:00:01');
INSERT INTO `sys_job_log` VALUES (206, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2025-01-12 00:00:00', '0', '', '2025-01-12 00:00:01');
INSERT INTO `sys_job_log` VALUES (207, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2025-02-08 00:00:00', '0', '', '2025-02-08 00:00:00');
INSERT INTO `sys_job_log` VALUES (208, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2025-02-08 00:00:00', '0', '', '2025-02-08 00:00:00');
INSERT INTO `sys_job_log` VALUES (209, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2025-04-15 00:00:03', '0', '', '2025-04-15 00:00:03');
INSERT INTO `sys_job_log` VALUES (210, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2025-04-15 00:00:03', '1', '[WinError 32] 另一个程序正在使用此文件，进程无法访问。: \'F:\\\\gitpush\\\\Sakura_K\\\\logs\\\\2025-04-14_error.log\'', '2025-04-15 00:00:03');
INSERT INTO `sys_job_log` VALUES (211, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobSubmissionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2025-04-16 00:00:00', '0', '', '2025-04-16 00:00:00');
INSERT INTO `sys_job_log` VALUES (212, '打包、删除日志', 'default', 'default', 'module_task.scheduler_log:log', '', '{}', 'cron[month=\'*\', day=\'*\', hour=\'0\', minute=\'0\', second=\'0\']', '事件类型: JobExecutionEvent, 任务ID: 7, 任务名称: 打包、删除日志, 执行于2025-04-16 00:00:00', '1', '[WinError 32] 另一个程序正在使用此文件，进程无法访问。: \'F:\\\\gitpush\\\\Sakura_K\\\\logs\\\\2025-04-15_error.log\'', '2025-04-16 00:00:00');

-- ----------------------------
-- Table structure for sys_logininfor
-- ----------------------------
DROP TABLE IF EXISTS `sys_logininfor`;
CREATE TABLE `sys_logininfor`  (
  `info_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '访问ID',
  `user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '用户账号',
  `ipaddr` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '登录IP地址',
  `login_location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '登录地点',
  `browser` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '浏览器类型',
  `os` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '操作系统',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '登录状态（0成功 1失败）',
  `msg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '提示消息',
  `login_time` datetime(0) NULL DEFAULT NULL COMMENT '访问时间',
  PRIMARY KEY (`info_id`) USING BTREE,
  INDEX `idx_sys_logininfor_s`(`status`) USING BTREE,
  INDEX `idx_sys_logininfor_lt`(`login_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3645 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '系统访问记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_logininfor
-- ----------------------------
INSERT INTO `sys_logininfor` VALUES (1907, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-21 12:08:55');
INSERT INTO `sys_logininfor` VALUES (1908, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-21 12:09:25');
INSERT INTO `sys_logininfor` VALUES (1909, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-22 16:54:29');
INSERT INTO `sys_logininfor` VALUES (1910, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-22 16:56:21');
INSERT INTO `sys_logininfor` VALUES (1911, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-23 23:58:55');
INSERT INTO `sys_logininfor` VALUES (1912, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-25 20:27:03');
INSERT INTO `sys_logininfor` VALUES (1913, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-25 21:23:40');
INSERT INTO `sys_logininfor` VALUES (1914, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-27 11:47:37');
INSERT INTO `sys_logininfor` VALUES (1915, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-27 11:48:25');
INSERT INTO `sys_logininfor` VALUES (1916, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-27 12:21:08');
INSERT INTO `sys_logininfor` VALUES (1917, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-27 12:40:33');
INSERT INTO `sys_logininfor` VALUES (1918, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '1', '验证码错误', '2024-08-27 18:25:14');
INSERT INTO `sys_logininfor` VALUES (1919, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-27 18:25:16');
INSERT INTO `sys_logininfor` VALUES (1920, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-29 00:44:30');
INSERT INTO `sys_logininfor` VALUES (1921, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-08-29 10:27:49');
INSERT INTO `sys_logininfor` VALUES (1922, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-07 17:17:25');
INSERT INTO `sys_logininfor` VALUES (1923, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-08 10:53:20');
INSERT INTO `sys_logininfor` VALUES (1924, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '1', '验证码错误', '2024-09-08 11:12:43');
INSERT INTO `sys_logininfor` VALUES (1925, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-08 11:12:46');
INSERT INTO `sys_logininfor` VALUES (1926, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-09 22:49:08');
INSERT INTO `sys_logininfor` VALUES (1927, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-10 10:16:22');
INSERT INTO `sys_logininfor` VALUES (1928, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-11 11:05:36');
INSERT INTO `sys_logininfor` VALUES (1929, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-15 12:28:32');
INSERT INTO `sys_logininfor` VALUES (1930, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-15 22:03:04');
INSERT INTO `sys_logininfor` VALUES (1931, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-15 22:05:26');
INSERT INTO `sys_logininfor` VALUES (1932, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-16 10:05:43');
INSERT INTO `sys_logininfor` VALUES (1933, '', '', '内网IP', 'Other', 'Other', '1', '验证码已失效', '2024-09-16 10:14:44');
INSERT INTO `sys_logininfor` VALUES (1934, '', '', '内网IP', 'Other', 'Other', '1', '验证码已失效', '2024-09-16 10:16:57');
INSERT INTO `sys_logininfor` VALUES (1935, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-16 10:18:53');
INSERT INTO `sys_logininfor` VALUES (1936, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-09-16 10:19:11');
INSERT INTO `sys_logininfor` VALUES (1937, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-16 19:11:52');
INSERT INTO `sys_logininfor` VALUES (1938, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-18 15:25:04');
INSERT INTO `sys_logininfor` VALUES (1939, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-19 16:07:01');
INSERT INTO `sys_logininfor` VALUES (1940, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-19 17:31:12');
INSERT INTO `sys_logininfor` VALUES (1941, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-19 17:33:40');
INSERT INTO `sys_logininfor` VALUES (1942, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-20 15:56:07');
INSERT INTO `sys_logininfor` VALUES (1943, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-20 22:31:03');
INSERT INTO `sys_logininfor` VALUES (1944, 'demo1', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-20 22:40:21');
INSERT INTO `sys_logininfor` VALUES (1945, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '1', '验证码已失效', '2024-09-21 22:44:37');
INSERT INTO `sys_logininfor` VALUES (1946, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-21 22:44:41');
INSERT INTO `sys_logininfor` VALUES (1947, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-22 17:11:50');
INSERT INTO `sys_logininfor` VALUES (1948, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-22 17:12:22');
INSERT INTO `sys_logininfor` VALUES (1949, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-22 17:14:26');
INSERT INTO `sys_logininfor` VALUES (1950, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-23 22:18:31');
INSERT INTO `sys_logininfor` VALUES (1951, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-24 17:01:24');
INSERT INTO `sys_logininfor` VALUES (1952, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-25 09:54:52');
INSERT INTO `sys_logininfor` VALUES (1953, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-26 00:49:38');
INSERT INTO `sys_logininfor` VALUES (1954, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '1', '验证码已失效', '2024-09-26 01:21:40');
INSERT INTO `sys_logininfor` VALUES (1955, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-26 01:21:44');
INSERT INTO `sys_logininfor` VALUES (1956, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-26 01:23:20');
INSERT INTO `sys_logininfor` VALUES (1957, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-26 20:52:24');
INSERT INTO `sys_logininfor` VALUES (1958, 'admin', '', '内网IP', 'Other', 'Other', '1', '验证码已失效', '2024-09-27 17:31:05');
INSERT INTO `sys_logininfor` VALUES (1959, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-09-27 17:32:35');
INSERT INTO `sys_logininfor` VALUES (1960, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-09-28 00:47:12');
INSERT INTO `sys_logininfor` VALUES (1961, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-09-28 17:10:18');
INSERT INTO `sys_logininfor` VALUES (1962, 'admin', '', '内网IP', 'Other', 'Other', '1', '验证码已失效', '2024-09-29 16:41:19');
INSERT INTO `sys_logininfor` VALUES (1963, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-09-29 16:42:09');
INSERT INTO `sys_logininfor` VALUES (1964, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-09-29 18:31:30');
INSERT INTO `sys_logininfor` VALUES (1965, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-09-29 18:31:48');
INSERT INTO `sys_logininfor` VALUES (1966, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-09-29 18:31:55');
INSERT INTO `sys_logininfor` VALUES (1967, '', '', '内网IP', 'Other', 'Other', '1', '验证码已失效', '2024-09-29 18:32:23');
INSERT INTO `sys_logininfor` VALUES (1968, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-09-29 18:32:29');
INSERT INTO `sys_logininfor` VALUES (1969, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-09-29 18:33:09');
INSERT INTO `sys_logininfor` VALUES (1970, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-09-29 18:56:56');
INSERT INTO `sys_logininfor` VALUES (1971, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-09-29 18:57:56');
INSERT INTO `sys_logininfor` VALUES (1972, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-09-29 19:00:54');
INSERT INTO `sys_logininfor` VALUES (1973, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-10-02 00:34:52');
INSERT INTO `sys_logininfor` VALUES (1974, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 11:46:33');
INSERT INTO `sys_logininfor` VALUES (1975, '', '', '内网IP', 'Other', 'Other', '1', '验证码已失效', '2024-10-03 11:50:37');
INSERT INTO `sys_logininfor` VALUES (1976, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-03 11:50:46');
INSERT INTO `sys_logininfor` VALUES (1977, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:01:55');
INSERT INTO `sys_logininfor` VALUES (1978, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:03:36');
INSERT INTO `sys_logininfor` VALUES (1979, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:03:48');
INSERT INTO `sys_logininfor` VALUES (1980, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:03:58');
INSERT INTO `sys_logininfor` VALUES (1981, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:04:17');
INSERT INTO `sys_logininfor` VALUES (1982, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:04:23');
INSERT INTO `sys_logininfor` VALUES (1983, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:04:32');
INSERT INTO `sys_logininfor` VALUES (1984, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:04:40');
INSERT INTO `sys_logininfor` VALUES (1985, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:04:48');
INSERT INTO `sys_logininfor` VALUES (1986, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:04:54');
INSERT INTO `sys_logininfor` VALUES (1987, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:05:02');
INSERT INTO `sys_logininfor` VALUES (1988, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:05:07');
INSERT INTO `sys_logininfor` VALUES (1989, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:08:14');
INSERT INTO `sys_logininfor` VALUES (1990, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:09:27');
INSERT INTO `sys_logininfor` VALUES (1991, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:10:21');
INSERT INTO `sys_logininfor` VALUES (1992, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:10:59');
INSERT INTO `sys_logininfor` VALUES (1993, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:11:07');
INSERT INTO `sys_logininfor` VALUES (1994, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:11:17');
INSERT INTO `sys_logininfor` VALUES (1995, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:11:41');
INSERT INTO `sys_logininfor` VALUES (1996, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:12:46');
INSERT INTO `sys_logininfor` VALUES (1997, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:14:06');
INSERT INTO `sys_logininfor` VALUES (1998, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:14:13');
INSERT INTO `sys_logininfor` VALUES (1999, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:15:00');
INSERT INTO `sys_logininfor` VALUES (2000, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:16:19');
INSERT INTO `sys_logininfor` VALUES (2001, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:16:42');
INSERT INTO `sys_logininfor` VALUES (2002, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:17:12');
INSERT INTO `sys_logininfor` VALUES (2003, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:17:36');
INSERT INTO `sys_logininfor` VALUES (2004, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:17:48');
INSERT INTO `sys_logininfor` VALUES (2005, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:18:11');
INSERT INTO `sys_logininfor` VALUES (2006, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:18:26');
INSERT INTO `sys_logininfor` VALUES (2007, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:18:38');
INSERT INTO `sys_logininfor` VALUES (2008, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:19:05');
INSERT INTO `sys_logininfor` VALUES (2009, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:19:25');
INSERT INTO `sys_logininfor` VALUES (2010, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:20:03');
INSERT INTO `sys_logininfor` VALUES (2011, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:20:55');
INSERT INTO `sys_logininfor` VALUES (2012, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:21:36');
INSERT INTO `sys_logininfor` VALUES (2013, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:21:50');
INSERT INTO `sys_logininfor` VALUES (2014, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:22:33');
INSERT INTO `sys_logininfor` VALUES (2015, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:24:43');
INSERT INTO `sys_logininfor` VALUES (2016, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:27:58');
INSERT INTO `sys_logininfor` VALUES (2017, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:36:50');
INSERT INTO `sys_logininfor` VALUES (2018, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-03 12:49:43');
INSERT INTO `sys_logininfor` VALUES (2019, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-03 12:49:54');
INSERT INTO `sys_logininfor` VALUES (2020, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-03 12:50:09');
INSERT INTO `sys_logininfor` VALUES (2021, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-03 12:50:28');
INSERT INTO `sys_logininfor` VALUES (2022, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-03 12:51:08');
INSERT INTO `sys_logininfor` VALUES (2023, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-03 12:51:45');
INSERT INTO `sys_logininfor` VALUES (2024, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-03 12:52:08');
INSERT INTO `sys_logininfor` VALUES (2025, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-03 12:52:18');
INSERT INTO `sys_logininfor` VALUES (2026, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-03 12:53:08');
INSERT INTO `sys_logininfor` VALUES (2027, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-03 12:53:56');
INSERT INTO `sys_logininfor` VALUES (2028, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-03 12:54:51');
INSERT INTO `sys_logininfor` VALUES (2029, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-03 12:55:22');
INSERT INTO `sys_logininfor` VALUES (2030, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 12:58:21');
INSERT INTO `sys_logininfor` VALUES (2031, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:05:30');
INSERT INTO `sys_logininfor` VALUES (2032, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:11:02');
INSERT INTO `sys_logininfor` VALUES (2033, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:11:42');
INSERT INTO `sys_logininfor` VALUES (2034, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:12:52');
INSERT INTO `sys_logininfor` VALUES (2035, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:13:06');
INSERT INTO `sys_logininfor` VALUES (2036, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:16:55');
INSERT INTO `sys_logininfor` VALUES (2037, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-03 13:16:55');
INSERT INTO `sys_logininfor` VALUES (2038, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:17:30');
INSERT INTO `sys_logininfor` VALUES (2039, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:18:04');
INSERT INTO `sys_logininfor` VALUES (2040, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:36:45');
INSERT INTO `sys_logininfor` VALUES (2041, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:37:09');
INSERT INTO `sys_logininfor` VALUES (2042, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:38:38');
INSERT INTO `sys_logininfor` VALUES (2043, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:39:13');
INSERT INTO `sys_logininfor` VALUES (2044, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:39:46');
INSERT INTO `sys_logininfor` VALUES (2045, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:40:11');
INSERT INTO `sys_logininfor` VALUES (2046, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:40:24');
INSERT INTO `sys_logininfor` VALUES (2047, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:40:31');
INSERT INTO `sys_logininfor` VALUES (2048, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:41:03');
INSERT INTO `sys_logininfor` VALUES (2049, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:41:11');
INSERT INTO `sys_logininfor` VALUES (2050, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:41:20');
INSERT INTO `sys_logininfor` VALUES (2051, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:42:21');
INSERT INTO `sys_logininfor` VALUES (2052, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:43:12');
INSERT INTO `sys_logininfor` VALUES (2053, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:43:37');
INSERT INTO `sys_logininfor` VALUES (2054, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:44:26');
INSERT INTO `sys_logininfor` VALUES (2055, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:44:52');
INSERT INTO `sys_logininfor` VALUES (2056, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:45:08');
INSERT INTO `sys_logininfor` VALUES (2057, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-03 13:45:24');
INSERT INTO `sys_logininfor` VALUES (2058, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:45:36');
INSERT INTO `sys_logininfor` VALUES (2059, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:46:39');
INSERT INTO `sys_logininfor` VALUES (2060, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:47:02');
INSERT INTO `sys_logininfor` VALUES (2061, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-03 13:47:15');
INSERT INTO `sys_logininfor` VALUES (2062, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-04 00:05:21');
INSERT INTO `sys_logininfor` VALUES (2063, '', '', '内网IP', 'Other', 'Other', '1', '验证码已失效', '2024-10-08 20:44:39');
INSERT INTO `sys_logininfor` VALUES (2064, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-08 20:44:52');
INSERT INTO `sys_logininfor` VALUES (2065, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-08 21:07:58');
INSERT INTO `sys_logininfor` VALUES (2066, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-08 21:08:17');
INSERT INTO `sys_logininfor` VALUES (2067, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-08 21:08:43');
INSERT INTO `sys_logininfor` VALUES (2068, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-08 21:08:45');
INSERT INTO `sys_logininfor` VALUES (2069, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-08 21:09:24');
INSERT INTO `sys_logininfor` VALUES (2070, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-08 21:09:56');
INSERT INTO `sys_logininfor` VALUES (2071, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-08 21:10:34');
INSERT INTO `sys_logininfor` VALUES (2072, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-08 21:11:41');
INSERT INTO `sys_logininfor` VALUES (2073, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-08 21:11:58');
INSERT INTO `sys_logininfor` VALUES (2074, '', '', '内网IP', 'Python aiohttp 3', 'Other', '1', '验证码已失效', '2024-10-08 21:12:11');
INSERT INTO `sys_logininfor` VALUES (2075, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-08 21:13:19');
INSERT INTO `sys_logininfor` VALUES (2076, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-08 21:17:24');
INSERT INTO `sys_logininfor` VALUES (2077, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-08 21:18:29');
INSERT INTO `sys_logininfor` VALUES (2078, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-08 21:39:29');
INSERT INTO `sys_logininfor` VALUES (2079, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-08 21:41:07');
INSERT INTO `sys_logininfor` VALUES (2080, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-08 21:41:37');
INSERT INTO `sys_logininfor` VALUES (2081, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-08 21:45:03');
INSERT INTO `sys_logininfor` VALUES (2082, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-08 21:51:57');
INSERT INTO `sys_logininfor` VALUES (2083, 'admin', '', '内网IP', 'Other', 'Other', '1', '验证码已失效', '2024-10-11 18:00:02');
INSERT INTO `sys_logininfor` VALUES (2084, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-11 18:02:45');
INSERT INTO `sys_logininfor` VALUES (2085, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-11 18:07:43');
INSERT INTO `sys_logininfor` VALUES (2086, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-11 18:22:50');
INSERT INTO `sys_logininfor` VALUES (2087, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-11 18:23:19');
INSERT INTO `sys_logininfor` VALUES (2088, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-11 18:23:47');
INSERT INTO `sys_logininfor` VALUES (2089, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-11 18:23:53');
INSERT INTO `sys_logininfor` VALUES (2090, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-15 10:34:18');
INSERT INTO `sys_logininfor` VALUES (2091, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-15 10:34:46');
INSERT INTO `sys_logininfor` VALUES (2092, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-15 10:35:25');
INSERT INTO `sys_logininfor` VALUES (2093, 'admin', '', '内网IP', 'Chrome 120', 'Windows 10', '0', '登录成功', '2024-10-15 11:19:55');
INSERT INTO `sys_logininfor` VALUES (2094, 'admin', '', '内网IP', 'Chrome 120', 'Windows 10', '0', '登录成功', '2024-10-15 13:47:20');
INSERT INTO `sys_logininfor` VALUES (2095, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-15 13:51:55');
INSERT INTO `sys_logininfor` VALUES (2096, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-15 14:48:05');
INSERT INTO `sys_logininfor` VALUES (2097, 'admin', '', '内网IP', 'Edge 123', 'Windows 10', '0', '登录成功', '2024-10-15 15:47:56');
INSERT INTO `sys_logininfor` VALUES (2098, 'admin', '', '内网IP', 'Chrome 120', 'Windows 10', '0', '登录成功', '2024-10-15 17:12:38');
INSERT INTO `sys_logininfor` VALUES (2099, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-15 18:09:13');
INSERT INTO `sys_logininfor` VALUES (2100, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-16 09:48:15');
INSERT INTO `sys_logininfor` VALUES (2101, 'admin', '', '内网IP', 'Chrome 120', 'Windows 10', '0', '登录成功', '2024-10-16 10:20:08');
INSERT INTO `sys_logininfor` VALUES (2102, 'admin', '', '内网IP', 'Chrome 120', 'Windows 10', '0', '登录成功', '2024-10-16 11:20:58');
INSERT INTO `sys_logininfor` VALUES (2103, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-10-16 22:58:19');
INSERT INTO `sys_logininfor` VALUES (2104, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-10-17 22:36:11');
INSERT INTO `sys_logininfor` VALUES (2105, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-10-19 15:17:04');
INSERT INTO `sys_logininfor` VALUES (2106, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-10-22 23:23:48');
INSERT INTO `sys_logininfor` VALUES (2107, 'admin', '', '内网IP', 'Other', 'Other', '1', '验证码已失效', '2024-10-23 22:44:59');
INSERT INTO `sys_logininfor` VALUES (2108, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-23 22:46:06');
INSERT INTO `sys_logininfor` VALUES (2109, 'admin', '', '内网IP', 'Python aiohttp 3', 'Other', '0', '登录成功', '2024-10-23 22:50:25');
INSERT INTO `sys_logininfor` VALUES (2110, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-10-24 22:01:41');
INSERT INTO `sys_logininfor` VALUES (2111, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-10-26 16:33:01');
INSERT INTO `sys_logininfor` VALUES (2112, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-26 17:08:47');
INSERT INTO `sys_logininfor` VALUES (2113, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-10-30 22:50:37');
INSERT INTO `sys_logininfor` VALUES (2114, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-10-31 21:58:22');
INSERT INTO `sys_logininfor` VALUES (2115, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-08 13:29:18');
INSERT INTO `sys_logininfor` VALUES (2116, 'admin', '', '内网IP', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-14 11:15:54');
INSERT INTO `sys_logininfor` VALUES (2117, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-11-16 16:14:12');
INSERT INTO `sys_logininfor` VALUES (2118, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-11-16 16:14:55');
INSERT INTO `sys_logininfor` VALUES (2119, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-11-16 16:15:52');
INSERT INTO `sys_logininfor` VALUES (2120, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-11-16 21:16:43');
INSERT INTO `sys_logininfor` VALUES (2121, 'admin', '222.80.90.97', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-16 23:53:08');
INSERT INTO `sys_logininfor` VALUES (2122, 'admin', '222.80.90.97', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-17 00:57:09');
INSERT INTO `sys_logininfor` VALUES (2123, 'admin', '222.80.90.97', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-17 01:27:27');
INSERT INTO `sys_logininfor` VALUES (2124, 'admin', '222.80.90.97', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-17 01:30:41');
INSERT INTO `sys_logininfor` VALUES (2125, 'admin', '222.80.90.97', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-17 23:21:06');
INSERT INTO `sys_logininfor` VALUES (2126, 'admin', '222.80.90.97', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-17 23:38:54');
INSERT INTO `sys_logininfor` VALUES (2127, 'admin', '222.80.90.97', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-18 00:07:28');
INSERT INTO `sys_logininfor` VALUES (2128, 'admin', '112.96.226.60', '亚洲-广东省', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-18 13:06:25');
INSERT INTO `sys_logininfor` VALUES (2129, 'admin', '', '内网IP', 'Other', 'Other', '1', '验证码已失效', '2024-11-19 16:36:36');
INSERT INTO `sys_logininfor` VALUES (2130, 'admin', '222.80.91.121', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-22 01:28:10');
INSERT INTO `sys_logininfor` VALUES (2131, 'admin', '222.80.91.121', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-22 01:34:23');
INSERT INTO `sys_logininfor` VALUES (2132, 'admin', '222.80.91.84', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-27 17:49:43');
INSERT INTO `sys_logininfor` VALUES (2133, 'admin', '222.80.88.110', '亚洲-新疆维吾尔自治区', 'Chrome Mobile iOS 125', 'iOS 15', '0', '登录成功', '2024-11-29 09:41:25');
INSERT INTO `sys_logininfor` VALUES (2134, 'admin', '222.80.91.84', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-11-30 09:59:29');
INSERT INTO `sys_logininfor` VALUES (2135, 'admin', '222.80.91.104', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '1', '验证码已失效', '2024-12-02 10:43:45');
INSERT INTO `sys_logininfor` VALUES (2136, 'admin', '222.80.91.104', '亚洲-新疆维吾尔自治区', 'Chrome 109', 'Mac OS X 10', '0', '登录成功', '2024-12-02 10:43:49');
INSERT INTO `sys_logininfor` VALUES (2137, 'admin', '222.137.128.42', '未知', 'Chrome 131', 'Windows 10', '1', '密码错误', '2024-12-15 00:25:54');
INSERT INTO `sys_logininfor` VALUES (2138, 'admin', '', '内网IP', 'Other', 'Other', '1', '验证码已失效', '2024-12-17 15:45:06');
INSERT INTO `sys_logininfor` VALUES (2139, 'admin', '', '内网IP', 'Other', 'Other', '1', '验证码已失效', '2024-12-17 15:45:20');
INSERT INTO `sys_logininfor` VALUES (2140, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-12-25 15:29:41');
INSERT INTO `sys_logininfor` VALUES (2141, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:33');
INSERT INTO `sys_logininfor` VALUES (2142, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:41');
INSERT INTO `sys_logininfor` VALUES (2143, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:41');
INSERT INTO `sys_logininfor` VALUES (2144, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:41');
INSERT INTO `sys_logininfor` VALUES (2145, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:41');
INSERT INTO `sys_logininfor` VALUES (2146, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:41');
INSERT INTO `sys_logininfor` VALUES (2147, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:41');
INSERT INTO `sys_logininfor` VALUES (2148, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:41');
INSERT INTO `sys_logininfor` VALUES (2149, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:41');
INSERT INTO `sys_logininfor` VALUES (2150, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:41');
INSERT INTO `sys_logininfor` VALUES (2151, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:42');
INSERT INTO `sys_logininfor` VALUES (2152, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:42');
INSERT INTO `sys_logininfor` VALUES (2153, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:42');
INSERT INTO `sys_logininfor` VALUES (2154, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:42');
INSERT INTO `sys_logininfor` VALUES (2155, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:43');
INSERT INTO `sys_logininfor` VALUES (2156, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:43');
INSERT INTO `sys_logininfor` VALUES (2157, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:43');
INSERT INTO `sys_logininfor` VALUES (2158, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:43');
INSERT INTO `sys_logininfor` VALUES (2159, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:43');
INSERT INTO `sys_logininfor` VALUES (2160, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:43');
INSERT INTO `sys_logininfor` VALUES (2161, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:43');
INSERT INTO `sys_logininfor` VALUES (2162, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:43');
INSERT INTO `sys_logininfor` VALUES (2163, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:43');
INSERT INTO `sys_logininfor` VALUES (2164, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:43');
INSERT INTO `sys_logininfor` VALUES (2165, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:44');
INSERT INTO `sys_logininfor` VALUES (2166, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:44');
INSERT INTO `sys_logininfor` VALUES (2167, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:44');
INSERT INTO `sys_logininfor` VALUES (2168, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:44');
INSERT INTO `sys_logininfor` VALUES (2169, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:44');
INSERT INTO `sys_logininfor` VALUES (2170, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:44');
INSERT INTO `sys_logininfor` VALUES (2171, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:44');
INSERT INTO `sys_logininfor` VALUES (2172, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:44');
INSERT INTO `sys_logininfor` VALUES (2173, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:44');
INSERT INTO `sys_logininfor` VALUES (2174, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:45');
INSERT INTO `sys_logininfor` VALUES (2175, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:45');
INSERT INTO `sys_logininfor` VALUES (2176, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:45');
INSERT INTO `sys_logininfor` VALUES (2177, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:45');
INSERT INTO `sys_logininfor` VALUES (2178, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:45');
INSERT INTO `sys_logininfor` VALUES (2179, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:45');
INSERT INTO `sys_logininfor` VALUES (2180, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:45');
INSERT INTO `sys_logininfor` VALUES (2181, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:45');
INSERT INTO `sys_logininfor` VALUES (2182, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:45');
INSERT INTO `sys_logininfor` VALUES (2183, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:45');
INSERT INTO `sys_logininfor` VALUES (2184, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:46');
INSERT INTO `sys_logininfor` VALUES (2185, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:46');
INSERT INTO `sys_logininfor` VALUES (2186, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:46');
INSERT INTO `sys_logininfor` VALUES (2187, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:46');
INSERT INTO `sys_logininfor` VALUES (2188, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:46');
INSERT INTO `sys_logininfor` VALUES (2189, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:46');
INSERT INTO `sys_logininfor` VALUES (2190, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:46');
INSERT INTO `sys_logininfor` VALUES (2191, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:46');
INSERT INTO `sys_logininfor` VALUES (2192, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:46');
INSERT INTO `sys_logininfor` VALUES (2193, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:47');
INSERT INTO `sys_logininfor` VALUES (2194, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:47');
INSERT INTO `sys_logininfor` VALUES (2195, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:47');
INSERT INTO `sys_logininfor` VALUES (2196, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:47');
INSERT INTO `sys_logininfor` VALUES (2197, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:47');
INSERT INTO `sys_logininfor` VALUES (2198, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:47');
INSERT INTO `sys_logininfor` VALUES (2199, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:47');
INSERT INTO `sys_logininfor` VALUES (2200, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:47');
INSERT INTO `sys_logininfor` VALUES (2201, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:47');
INSERT INTO `sys_logininfor` VALUES (2202, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:48');
INSERT INTO `sys_logininfor` VALUES (2203, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:48');
INSERT INTO `sys_logininfor` VALUES (2204, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:48');
INSERT INTO `sys_logininfor` VALUES (2205, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:48');
INSERT INTO `sys_logininfor` VALUES (2206, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:48');
INSERT INTO `sys_logininfor` VALUES (2207, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:48');
INSERT INTO `sys_logininfor` VALUES (2208, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:48');
INSERT INTO `sys_logininfor` VALUES (2209, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:48');
INSERT INTO `sys_logininfor` VALUES (2210, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:48');
INSERT INTO `sys_logininfor` VALUES (2211, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:48');
INSERT INTO `sys_logininfor` VALUES (2212, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:49');
INSERT INTO `sys_logininfor` VALUES (2213, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:49');
INSERT INTO `sys_logininfor` VALUES (2214, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:49');
INSERT INTO `sys_logininfor` VALUES (2215, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:49');
INSERT INTO `sys_logininfor` VALUES (2216, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:49');
INSERT INTO `sys_logininfor` VALUES (2217, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:49');
INSERT INTO `sys_logininfor` VALUES (2218, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:49');
INSERT INTO `sys_logininfor` VALUES (2219, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:49');
INSERT INTO `sys_logininfor` VALUES (2220, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:49');
INSERT INTO `sys_logininfor` VALUES (2221, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:50');
INSERT INTO `sys_logininfor` VALUES (2222, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:50');
INSERT INTO `sys_logininfor` VALUES (2223, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:50');
INSERT INTO `sys_logininfor` VALUES (2224, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:50');
INSERT INTO `sys_logininfor` VALUES (2225, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:50');
INSERT INTO `sys_logininfor` VALUES (2226, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:50');
INSERT INTO `sys_logininfor` VALUES (2227, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:50');
INSERT INTO `sys_logininfor` VALUES (2228, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:50');
INSERT INTO `sys_logininfor` VALUES (2229, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:50');
INSERT INTO `sys_logininfor` VALUES (2230, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2231, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2232, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2233, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2234, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2235, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2236, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2237, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2238, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2239, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2240, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2241, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2242, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:51');
INSERT INTO `sys_logininfor` VALUES (2243, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:52');
INSERT INTO `sys_logininfor` VALUES (2244, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:52');
INSERT INTO `sys_logininfor` VALUES (2245, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:52');
INSERT INTO `sys_logininfor` VALUES (2246, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:52');
INSERT INTO `sys_logininfor` VALUES (2247, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:52');
INSERT INTO `sys_logininfor` VALUES (2248, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:52');
INSERT INTO `sys_logininfor` VALUES (2249, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:52');
INSERT INTO `sys_logininfor` VALUES (2250, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:52');
INSERT INTO `sys_logininfor` VALUES (2251, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:52');
INSERT INTO `sys_logininfor` VALUES (2252, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:53');
INSERT INTO `sys_logininfor` VALUES (2253, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:53');
INSERT INTO `sys_logininfor` VALUES (2254, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:53');
INSERT INTO `sys_logininfor` VALUES (2255, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:53');
INSERT INTO `sys_logininfor` VALUES (2256, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:53');
INSERT INTO `sys_logininfor` VALUES (2257, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:53');
INSERT INTO `sys_logininfor` VALUES (2258, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:53');
INSERT INTO `sys_logininfor` VALUES (2259, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:53');
INSERT INTO `sys_logininfor` VALUES (2260, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:53');
INSERT INTO `sys_logininfor` VALUES (2261, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:54');
INSERT INTO `sys_logininfor` VALUES (2262, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:54');
INSERT INTO `sys_logininfor` VALUES (2263, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:54');
INSERT INTO `sys_logininfor` VALUES (2264, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:54');
INSERT INTO `sys_logininfor` VALUES (2265, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:54');
INSERT INTO `sys_logininfor` VALUES (2266, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:54');
INSERT INTO `sys_logininfor` VALUES (2267, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:54');
INSERT INTO `sys_logininfor` VALUES (2268, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:54');
INSERT INTO `sys_logininfor` VALUES (2269, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:54');
INSERT INTO `sys_logininfor` VALUES (2270, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:54');
INSERT INTO `sys_logininfor` VALUES (2271, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:54');
INSERT INTO `sys_logininfor` VALUES (2272, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:55');
INSERT INTO `sys_logininfor` VALUES (2273, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:55');
INSERT INTO `sys_logininfor` VALUES (2274, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:55');
INSERT INTO `sys_logininfor` VALUES (2275, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:55');
INSERT INTO `sys_logininfor` VALUES (2276, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:55');
INSERT INTO `sys_logininfor` VALUES (2277, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:55');
INSERT INTO `sys_logininfor` VALUES (2278, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:55');
INSERT INTO `sys_logininfor` VALUES (2279, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:55');
INSERT INTO `sys_logininfor` VALUES (2280, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:55');
INSERT INTO `sys_logininfor` VALUES (2281, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:56');
INSERT INTO `sys_logininfor` VALUES (2282, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:56');
INSERT INTO `sys_logininfor` VALUES (2283, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:56');
INSERT INTO `sys_logininfor` VALUES (2284, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:56');
INSERT INTO `sys_logininfor` VALUES (2285, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:56');
INSERT INTO `sys_logininfor` VALUES (2286, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:56');
INSERT INTO `sys_logininfor` VALUES (2287, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:56');
INSERT INTO `sys_logininfor` VALUES (2288, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:56');
INSERT INTO `sys_logininfor` VALUES (2289, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:56');
INSERT INTO `sys_logininfor` VALUES (2290, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:56');
INSERT INTO `sys_logininfor` VALUES (2291, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:56');
INSERT INTO `sys_logininfor` VALUES (2292, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:57');
INSERT INTO `sys_logininfor` VALUES (2293, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:57');
INSERT INTO `sys_logininfor` VALUES (2294, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:57');
INSERT INTO `sys_logininfor` VALUES (2295, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:57');
INSERT INTO `sys_logininfor` VALUES (2296, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:57');
INSERT INTO `sys_logininfor` VALUES (2297, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:57');
INSERT INTO `sys_logininfor` VALUES (2298, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:57');
INSERT INTO `sys_logininfor` VALUES (2299, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:58');
INSERT INTO `sys_logininfor` VALUES (2300, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:58');
INSERT INTO `sys_logininfor` VALUES (2301, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:58');
INSERT INTO `sys_logininfor` VALUES (2302, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:57');
INSERT INTO `sys_logininfor` VALUES (2303, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:58');
INSERT INTO `sys_logininfor` VALUES (2304, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:58');
INSERT INTO `sys_logininfor` VALUES (2305, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:58');
INSERT INTO `sys_logininfor` VALUES (2306, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:58');
INSERT INTO `sys_logininfor` VALUES (2307, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:58');
INSERT INTO `sys_logininfor` VALUES (2308, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:58');
INSERT INTO `sys_logininfor` VALUES (2309, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:58');
INSERT INTO `sys_logininfor` VALUES (2310, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:59');
INSERT INTO `sys_logininfor` VALUES (2311, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:59');
INSERT INTO `sys_logininfor` VALUES (2312, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:59');
INSERT INTO `sys_logininfor` VALUES (2313, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:59');
INSERT INTO `sys_logininfor` VALUES (2314, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:59');
INSERT INTO `sys_logininfor` VALUES (2315, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:59');
INSERT INTO `sys_logininfor` VALUES (2316, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:59');
INSERT INTO `sys_logininfor` VALUES (2317, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:59');
INSERT INTO `sys_logininfor` VALUES (2318, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:59');
INSERT INTO `sys_logininfor` VALUES (2319, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:31:59');
INSERT INTO `sys_logininfor` VALUES (2320, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:00');
INSERT INTO `sys_logininfor` VALUES (2321, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:00');
INSERT INTO `sys_logininfor` VALUES (2322, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:00');
INSERT INTO `sys_logininfor` VALUES (2323, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:00');
INSERT INTO `sys_logininfor` VALUES (2324, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:00');
INSERT INTO `sys_logininfor` VALUES (2325, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:00');
INSERT INTO `sys_logininfor` VALUES (2326, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:00');
INSERT INTO `sys_logininfor` VALUES (2327, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:00');
INSERT INTO `sys_logininfor` VALUES (2328, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:00');
INSERT INTO `sys_logininfor` VALUES (2329, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:00');
INSERT INTO `sys_logininfor` VALUES (2330, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:01');
INSERT INTO `sys_logininfor` VALUES (2331, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:01');
INSERT INTO `sys_logininfor` VALUES (2332, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:01');
INSERT INTO `sys_logininfor` VALUES (2333, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:01');
INSERT INTO `sys_logininfor` VALUES (2334, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:01');
INSERT INTO `sys_logininfor` VALUES (2335, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:01');
INSERT INTO `sys_logininfor` VALUES (2336, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:01');
INSERT INTO `sys_logininfor` VALUES (2337, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:01');
INSERT INTO `sys_logininfor` VALUES (2338, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2339, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2340, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2341, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2342, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2343, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2344, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2345, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2346, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2347, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2348, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2349, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2350, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2351, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:02');
INSERT INTO `sys_logininfor` VALUES (2352, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:03');
INSERT INTO `sys_logininfor` VALUES (2353, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:03');
INSERT INTO `sys_logininfor` VALUES (2354, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:03');
INSERT INTO `sys_logininfor` VALUES (2355, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:03');
INSERT INTO `sys_logininfor` VALUES (2356, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:03');
INSERT INTO `sys_logininfor` VALUES (2357, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:03');
INSERT INTO `sys_logininfor` VALUES (2358, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:03');
INSERT INTO `sys_logininfor` VALUES (2359, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:32:03');
INSERT INTO `sys_logininfor` VALUES (2360, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-12-25 15:38:49');
INSERT INTO `sys_logininfor` VALUES (2361, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:49:09');
INSERT INTO `sys_logininfor` VALUES (2362, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:47');
INSERT INTO `sys_logininfor` VALUES (2363, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:47');
INSERT INTO `sys_logininfor` VALUES (2364, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:47');
INSERT INTO `sys_logininfor` VALUES (2365, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:47');
INSERT INTO `sys_logininfor` VALUES (2366, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:47');
INSERT INTO `sys_logininfor` VALUES (2367, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:47');
INSERT INTO `sys_logininfor` VALUES (2368, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:47');
INSERT INTO `sys_logininfor` VALUES (2369, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:47');
INSERT INTO `sys_logininfor` VALUES (2370, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2371, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2372, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2373, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2374, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2375, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2376, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2377, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2378, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2379, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2380, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2381, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2382, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2383, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2384, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2385, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2386, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2387, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2388, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2389, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2390, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2391, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2392, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2393, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2394, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2395, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2396, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2397, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2398, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2399, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2400, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2401, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2402, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2403, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2404, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2405, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2406, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2407, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2408, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2409, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2410, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2411, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2412, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2413, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2414, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2415, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2416, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2417, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2418, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2419, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2420, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2421, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2422, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2423, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2424, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2425, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2426, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2427, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2428, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2429, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2430, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2431, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2432, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2433, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2434, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2435, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2436, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2437, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2438, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2439, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:02');
INSERT INTO `sys_logininfor` VALUES (2440, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:00');
INSERT INTO `sys_logininfor` VALUES (2441, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2442, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:02');
INSERT INTO `sys_logininfor` VALUES (2443, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2444, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2445, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2446, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2447, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2448, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2449, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:02');
INSERT INTO `sys_logininfor` VALUES (2450, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2451, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:54');
INSERT INTO `sys_logininfor` VALUES (2452, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2453, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2454, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2455, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2456, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2457, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:02');
INSERT INTO `sys_logininfor` VALUES (2458, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2459, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2460, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2461, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:02');
INSERT INTO `sys_logininfor` VALUES (2462, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:03');
INSERT INTO `sys_logininfor` VALUES (2463, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2464, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2465, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2466, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2467, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:03');
INSERT INTO `sys_logininfor` VALUES (2468, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:03');
INSERT INTO `sys_logininfor` VALUES (2469, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2470, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2471, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2472, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2473, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2474, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2475, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2476, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2477, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2478, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2479, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2480, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:56:59');
INSERT INTO `sys_logininfor` VALUES (2481, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:08');
INSERT INTO `sys_logininfor` VALUES (2482, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:00');
INSERT INTO `sys_logininfor` VALUES (2483, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:08');
INSERT INTO `sys_logininfor` VALUES (2484, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:00');
INSERT INTO `sys_logininfor` VALUES (2485, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:00');
INSERT INTO `sys_logininfor` VALUES (2486, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:00');
INSERT INTO `sys_logininfor` VALUES (2487, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:57:00');
INSERT INTO `sys_logininfor` VALUES (2491, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-12-25 15:58:29');
INSERT INTO `sys_logininfor` VALUES (2492, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2493, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2494, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2495, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2496, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2497, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2498, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2499, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2500, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2501, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2502, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2503, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2504, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2505, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:39');
INSERT INTO `sys_logininfor` VALUES (2506, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2507, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2508, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2509, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2510, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2511, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2512, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2513, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2514, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2515, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2516, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2517, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2518, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2519, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2520, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2521, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2522, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2523, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2524, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2525, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2526, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2527, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2528, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2529, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2530, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2531, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2532, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2533, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2534, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2535, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2536, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2537, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2538, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2539, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2540, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2541, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2542, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2543, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2544, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2545, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2546, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2547, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2548, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2549, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2550, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2551, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2552, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2553, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2554, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2555, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2556, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2557, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2558, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2559, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2560, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2561, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2562, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2563, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2564, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2565, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2566, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2567, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2568, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2569, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2570, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2571, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2572, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:03');
INSERT INTO `sys_logininfor` VALUES (2573, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2574, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2575, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2576, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2577, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2578, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2579, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2580, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2581, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2582, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2583, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2584, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2585, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2586, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2587, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2588, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2589, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2590, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:57');
INSERT INTO `sys_logininfor` VALUES (2591, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2592, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:57');
INSERT INTO `sys_logininfor` VALUES (2593, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2594, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2595, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:57');
INSERT INTO `sys_logininfor` VALUES (2596, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2597, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2598, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2599, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2600, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2601, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2602, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2603, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2604, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2605, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2606, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2607, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2608, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2609, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2610, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2611, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2612, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2613, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2614, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2615, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2616, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2617, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2618, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2619, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2620, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2621, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2622, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2623, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2624, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2625, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2626, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2627, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2628, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2629, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2630, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2631, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2632, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2633, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2634, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2635, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2636, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2637, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2638, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2639, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2640, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2641, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2642, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2643, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2644, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2645, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2646, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2647, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2648, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2649, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2650, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2651, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2652, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2653, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2654, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2655, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2656, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2657, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2658, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2659, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2660, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2661, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2662, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2663, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2664, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2665, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2666, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2667, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2668, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2669, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2670, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2671, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2672, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:03');
INSERT INTO `sys_logininfor` VALUES (2673, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:04');
INSERT INTO `sys_logininfor` VALUES (2674, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2675, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2676, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2677, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2678, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2679, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2680, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2681, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2682, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2683, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2684, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:03');
INSERT INTO `sys_logininfor` VALUES (2685, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2686, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:06');
INSERT INTO `sys_logininfor` VALUES (2687, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2688, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2689, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:57');
INSERT INTO `sys_logininfor` VALUES (2690, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:03');
INSERT INTO `sys_logininfor` VALUES (2691, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:57');
INSERT INTO `sys_logininfor` VALUES (2692, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:57');
INSERT INTO `sys_logininfor` VALUES (2693, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:57');
INSERT INTO `sys_logininfor` VALUES (2694, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:57');
INSERT INTO `sys_logininfor` VALUES (2695, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:04');
INSERT INTO `sys_logininfor` VALUES (2696, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:57');
INSERT INTO `sys_logininfor` VALUES (2697, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2698, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2699, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:04');
INSERT INTO `sys_logininfor` VALUES (2700, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2701, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2702, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2703, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2704, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2705, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:04');
INSERT INTO `sys_logininfor` VALUES (2706, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2707, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2708, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2709, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:04');
INSERT INTO `sys_logininfor` VALUES (2710, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2711, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2712, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2713, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2714, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2715, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2716, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2717, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2718, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2719, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2720, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2721, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2722, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2723, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2724, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2725, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2726, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:54');
INSERT INTO `sys_logininfor` VALUES (2727, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2728, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2729, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2730, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2731, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2732, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2733, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2734, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2735, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2736, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2737, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2738, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2739, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2740, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2741, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2742, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2743, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2744, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2745, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:48');
INSERT INTO `sys_logininfor` VALUES (2746, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2747, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2748, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2749, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2750, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2751, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:03');
INSERT INTO `sys_logininfor` VALUES (2752, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2753, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2754, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:57');
INSERT INTO `sys_logininfor` VALUES (2755, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:04');
INSERT INTO `sys_logininfor` VALUES (2756, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:57');
INSERT INTO `sys_logininfor` VALUES (2757, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2758, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2759, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2760, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2761, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:04');
INSERT INTO `sys_logininfor` VALUES (2762, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:04');
INSERT INTO `sys_logininfor` VALUES (2763, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:04');
INSERT INTO `sys_logininfor` VALUES (2764, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2765, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2766, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2767, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2768, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2769, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2770, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2771, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2772, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2773, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2774, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2775, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2776, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2777, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2778, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2779, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2780, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2781, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2782, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2783, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2784, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:56');
INSERT INTO `sys_logininfor` VALUES (2785, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:06');
INSERT INTO `sys_logininfor` VALUES (2786, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:06');
INSERT INTO `sys_logininfor` VALUES (2787, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:06');
INSERT INTO `sys_logininfor` VALUES (2788, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:06');
INSERT INTO `sys_logininfor` VALUES (2789, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:06');
INSERT INTO `sys_logininfor` VALUES (2790, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:06');
INSERT INTO `sys_logininfor` VALUES (2791, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:06');
INSERT INTO `sys_logininfor` VALUES (2792, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:06');
INSERT INTO `sys_logininfor` VALUES (2793, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2794, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2795, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:00');
INSERT INTO `sys_logininfor` VALUES (2796, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:01');
INSERT INTO `sys_logininfor` VALUES (2797, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2798, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2799, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:02');
INSERT INTO `sys_logininfor` VALUES (2800, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2801, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:04');
INSERT INTO `sys_logininfor` VALUES (2802, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2803, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2804, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2805, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:05');
INSERT INTO `sys_logininfor` VALUES (2806, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:06');
INSERT INTO `sys_logininfor` VALUES (2807, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 15:59:55');
INSERT INTO `sys_logininfor` VALUES (2808, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2809, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2810, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2811, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2812, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2813, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2814, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2815, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2816, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2817, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2818, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2819, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2820, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2821, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2822, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2823, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2824, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2825, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2826, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2827, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2828, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2829, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2830, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2831, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2832, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2833, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2834, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2835, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2836, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2837, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2838, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2839, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2840, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2841, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2842, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2843, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2844, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2845, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2846, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2847, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2848, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2849, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2850, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2851, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2852, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2853, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2854, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2855, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2856, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2857, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2858, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2859, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2860, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2861, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2862, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2863, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2864, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2865, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2866, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:00:30');
INSERT INTO `sys_logininfor` VALUES (2867, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2868, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2869, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2870, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2871, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2872, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2873, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2874, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2875, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2876, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2877, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2878, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2879, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2880, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2881, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2882, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2883, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2884, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2885, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2886, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2887, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2888, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2889, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2890, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2891, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2892, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2893, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2894, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2895, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2896, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:02:20');
INSERT INTO `sys_logininfor` VALUES (2897, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:08');
INSERT INTO `sys_logininfor` VALUES (2898, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:08');
INSERT INTO `sys_logininfor` VALUES (2899, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:08');
INSERT INTO `sys_logininfor` VALUES (2900, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:08');
INSERT INTO `sys_logininfor` VALUES (2901, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:08');
INSERT INTO `sys_logininfor` VALUES (2902, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:15');
INSERT INTO `sys_logininfor` VALUES (2903, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:15');
INSERT INTO `sys_logininfor` VALUES (2904, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:15');
INSERT INTO `sys_logininfor` VALUES (2905, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:15');
INSERT INTO `sys_logininfor` VALUES (2906, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:15');
INSERT INTO `sys_logininfor` VALUES (2907, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:15');
INSERT INTO `sys_logininfor` VALUES (2908, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:15');
INSERT INTO `sys_logininfor` VALUES (2909, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:15');
INSERT INTO `sys_logininfor` VALUES (2910, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:15');
INSERT INTO `sys_logininfor` VALUES (2911, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:15');
INSERT INTO `sys_logininfor` VALUES (2912, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:16');
INSERT INTO `sys_logininfor` VALUES (2913, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:16');
INSERT INTO `sys_logininfor` VALUES (2914, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:16');
INSERT INTO `sys_logininfor` VALUES (2915, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:16');
INSERT INTO `sys_logininfor` VALUES (2916, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:16');
INSERT INTO `sys_logininfor` VALUES (2917, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:17');
INSERT INTO `sys_logininfor` VALUES (2918, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:17');
INSERT INTO `sys_logininfor` VALUES (2919, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:17');
INSERT INTO `sys_logininfor` VALUES (2920, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:17');
INSERT INTO `sys_logininfor` VALUES (2921, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:17');
INSERT INTO `sys_logininfor` VALUES (2922, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:17');
INSERT INTO `sys_logininfor` VALUES (2923, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:17');
INSERT INTO `sys_logininfor` VALUES (2924, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2925, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2926, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2927, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2928, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2929, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2930, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2931, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2932, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2933, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2934, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2935, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2936, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:18');
INSERT INTO `sys_logininfor` VALUES (2937, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:19');
INSERT INTO `sys_logininfor` VALUES (2938, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:19');
INSERT INTO `sys_logininfor` VALUES (2939, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:19');
INSERT INTO `sys_logininfor` VALUES (2940, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:19');
INSERT INTO `sys_logininfor` VALUES (2941, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:19');
INSERT INTO `sys_logininfor` VALUES (2942, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:19');
INSERT INTO `sys_logininfor` VALUES (2943, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:20');
INSERT INTO `sys_logininfor` VALUES (2944, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:20');
INSERT INTO `sys_logininfor` VALUES (2945, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:20');
INSERT INTO `sys_logininfor` VALUES (2946, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:20');
INSERT INTO `sys_logininfor` VALUES (2947, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:20');
INSERT INTO `sys_logininfor` VALUES (2948, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:20');
INSERT INTO `sys_logininfor` VALUES (2949, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:20');
INSERT INTO `sys_logininfor` VALUES (2950, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:20');
INSERT INTO `sys_logininfor` VALUES (2951, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:21');
INSERT INTO `sys_logininfor` VALUES (2952, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:21');
INSERT INTO `sys_logininfor` VALUES (2953, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:21');
INSERT INTO `sys_logininfor` VALUES (2954, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:21');
INSERT INTO `sys_logininfor` VALUES (2955, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:21');
INSERT INTO `sys_logininfor` VALUES (2956, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:21');
INSERT INTO `sys_logininfor` VALUES (2957, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:21');
INSERT INTO `sys_logininfor` VALUES (2958, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:21');
INSERT INTO `sys_logininfor` VALUES (2959, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:21');
INSERT INTO `sys_logininfor` VALUES (2960, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:21');
INSERT INTO `sys_logininfor` VALUES (2961, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:21');
INSERT INTO `sys_logininfor` VALUES (2962, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:21');
INSERT INTO `sys_logininfor` VALUES (2963, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:22');
INSERT INTO `sys_logininfor` VALUES (2964, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:22');
INSERT INTO `sys_logininfor` VALUES (2965, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:22');
INSERT INTO `sys_logininfor` VALUES (2966, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:22');
INSERT INTO `sys_logininfor` VALUES (2967, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:22');
INSERT INTO `sys_logininfor` VALUES (2968, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:22');
INSERT INTO `sys_logininfor` VALUES (2969, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2970, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2971, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2972, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2973, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2974, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2975, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2976, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2977, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2978, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2979, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2980, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2981, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:24');
INSERT INTO `sys_logininfor` VALUES (2982, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2983, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:23');
INSERT INTO `sys_logininfor` VALUES (2984, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:24');
INSERT INTO `sys_logininfor` VALUES (2985, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:24');
INSERT INTO `sys_logininfor` VALUES (2986, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:24');
INSERT INTO `sys_logininfor` VALUES (2987, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:24');
INSERT INTO `sys_logininfor` VALUES (2988, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:25');
INSERT INTO `sys_logininfor` VALUES (2989, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:25');
INSERT INTO `sys_logininfor` VALUES (2990, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:25');
INSERT INTO `sys_logininfor` VALUES (2991, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:25');
INSERT INTO `sys_logininfor` VALUES (2992, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:25');
INSERT INTO `sys_logininfor` VALUES (2993, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:25');
INSERT INTO `sys_logininfor` VALUES (2994, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:25');
INSERT INTO `sys_logininfor` VALUES (2995, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:25');
INSERT INTO `sys_logininfor` VALUES (2996, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:25');
INSERT INTO `sys_logininfor` VALUES (2997, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:25');
INSERT INTO `sys_logininfor` VALUES (2998, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:25');
INSERT INTO `sys_logininfor` VALUES (2999, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:26');
INSERT INTO `sys_logininfor` VALUES (3000, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:26');
INSERT INTO `sys_logininfor` VALUES (3001, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:26');
INSERT INTO `sys_logininfor` VALUES (3002, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:26');
INSERT INTO `sys_logininfor` VALUES (3003, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:26');
INSERT INTO `sys_logininfor` VALUES (3004, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:26');
INSERT INTO `sys_logininfor` VALUES (3005, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:26');
INSERT INTO `sys_logininfor` VALUES (3006, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:26');
INSERT INTO `sys_logininfor` VALUES (3007, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:26');
INSERT INTO `sys_logininfor` VALUES (3008, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:26');
INSERT INTO `sys_logininfor` VALUES (3009, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:27');
INSERT INTO `sys_logininfor` VALUES (3010, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:27');
INSERT INTO `sys_logininfor` VALUES (3011, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:27');
INSERT INTO `sys_logininfor` VALUES (3012, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:27');
INSERT INTO `sys_logininfor` VALUES (3013, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3014, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3015, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3016, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3017, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3018, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3019, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3020, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3021, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3022, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3023, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3024, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3025, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3026, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3027, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3028, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:29');
INSERT INTO `sys_logininfor` VALUES (3029, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:29');
INSERT INTO `sys_logininfor` VALUES (3030, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:28');
INSERT INTO `sys_logininfor` VALUES (3031, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:29');
INSERT INTO `sys_logininfor` VALUES (3032, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:29');
INSERT INTO `sys_logininfor` VALUES (3033, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:29');
INSERT INTO `sys_logininfor` VALUES (3034, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:30');
INSERT INTO `sys_logininfor` VALUES (3035, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:29');
INSERT INTO `sys_logininfor` VALUES (3036, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:29');
INSERT INTO `sys_logininfor` VALUES (3037, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:30');
INSERT INTO `sys_logininfor` VALUES (3038, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:30');
INSERT INTO `sys_logininfor` VALUES (3039, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:30');
INSERT INTO `sys_logininfor` VALUES (3040, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:30');
INSERT INTO `sys_logininfor` VALUES (3041, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:31');
INSERT INTO `sys_logininfor` VALUES (3042, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:31');
INSERT INTO `sys_logininfor` VALUES (3043, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:31');
INSERT INTO `sys_logininfor` VALUES (3044, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:31');
INSERT INTO `sys_logininfor` VALUES (3045, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:31');
INSERT INTO `sys_logininfor` VALUES (3046, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:31');
INSERT INTO `sys_logininfor` VALUES (3047, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:31');
INSERT INTO `sys_logininfor` VALUES (3048, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:31');
INSERT INTO `sys_logininfor` VALUES (3049, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:31');
INSERT INTO `sys_logininfor` VALUES (3050, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:31');
INSERT INTO `sys_logininfor` VALUES (3051, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:32');
INSERT INTO `sys_logininfor` VALUES (3052, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:31');
INSERT INTO `sys_logininfor` VALUES (3053, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:32');
INSERT INTO `sys_logininfor` VALUES (3054, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:32');
INSERT INTO `sys_logininfor` VALUES (3055, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:32');
INSERT INTO `sys_logininfor` VALUES (3056, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:32');
INSERT INTO `sys_logininfor` VALUES (3057, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:32');
INSERT INTO `sys_logininfor` VALUES (3058, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:32');
INSERT INTO `sys_logininfor` VALUES (3059, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:32');
INSERT INTO `sys_logininfor` VALUES (3060, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:32');
INSERT INTO `sys_logininfor` VALUES (3061, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:33');
INSERT INTO `sys_logininfor` VALUES (3062, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:33');
INSERT INTO `sys_logininfor` VALUES (3063, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:33');
INSERT INTO `sys_logininfor` VALUES (3064, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:33');
INSERT INTO `sys_logininfor` VALUES (3065, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:33');
INSERT INTO `sys_logininfor` VALUES (3066, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:33');
INSERT INTO `sys_logininfor` VALUES (3067, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:33');
INSERT INTO `sys_logininfor` VALUES (3068, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:33');
INSERT INTO `sys_logininfor` VALUES (3069, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:34');
INSERT INTO `sys_logininfor` VALUES (3070, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:33');
INSERT INTO `sys_logininfor` VALUES (3071, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:33');
INSERT INTO `sys_logininfor` VALUES (3072, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:33');
INSERT INTO `sys_logininfor` VALUES (3073, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:34');
INSERT INTO `sys_logininfor` VALUES (3074, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:34');
INSERT INTO `sys_logininfor` VALUES (3075, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:34');
INSERT INTO `sys_logininfor` VALUES (3076, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:34');
INSERT INTO `sys_logininfor` VALUES (3077, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:35');
INSERT INTO `sys_logininfor` VALUES (3078, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:35');
INSERT INTO `sys_logininfor` VALUES (3079, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:35');
INSERT INTO `sys_logininfor` VALUES (3080, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:35');
INSERT INTO `sys_logininfor` VALUES (3081, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:35');
INSERT INTO `sys_logininfor` VALUES (3082, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:35');
INSERT INTO `sys_logininfor` VALUES (3083, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:35');
INSERT INTO `sys_logininfor` VALUES (3084, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:35');
INSERT INTO `sys_logininfor` VALUES (3085, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:35');
INSERT INTO `sys_logininfor` VALUES (3086, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:35');
INSERT INTO `sys_logininfor` VALUES (3087, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:35');
INSERT INTO `sys_logininfor` VALUES (3088, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:35');
INSERT INTO `sys_logininfor` VALUES (3089, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:36');
INSERT INTO `sys_logininfor` VALUES (3090, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:36');
INSERT INTO `sys_logininfor` VALUES (3091, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:36');
INSERT INTO `sys_logininfor` VALUES (3092, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:36');
INSERT INTO `sys_logininfor` VALUES (3093, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:36');
INSERT INTO `sys_logininfor` VALUES (3094, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:36');
INSERT INTO `sys_logininfor` VALUES (3095, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:36');
INSERT INTO `sys_logininfor` VALUES (3096, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:37');
INSERT INTO `sys_logininfor` VALUES (3097, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:37');
INSERT INTO `sys_logininfor` VALUES (3098, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:37');
INSERT INTO `sys_logininfor` VALUES (3099, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:37');
INSERT INTO `sys_logininfor` VALUES (3100, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:37');
INSERT INTO `sys_logininfor` VALUES (3101, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:37');
INSERT INTO `sys_logininfor` VALUES (3102, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:38');
INSERT INTO `sys_logininfor` VALUES (3103, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:38');
INSERT INTO `sys_logininfor` VALUES (3104, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:38');
INSERT INTO `sys_logininfor` VALUES (3105, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:38');
INSERT INTO `sys_logininfor` VALUES (3106, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:38');
INSERT INTO `sys_logininfor` VALUES (3107, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:38');
INSERT INTO `sys_logininfor` VALUES (3108, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:38');
INSERT INTO `sys_logininfor` VALUES (3109, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:38');
INSERT INTO `sys_logininfor` VALUES (3110, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:38');
INSERT INTO `sys_logininfor` VALUES (3111, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:38');
INSERT INTO `sys_logininfor` VALUES (3112, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:39');
INSERT INTO `sys_logininfor` VALUES (3113, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:39');
INSERT INTO `sys_logininfor` VALUES (3114, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:39');
INSERT INTO `sys_logininfor` VALUES (3115, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:39');
INSERT INTO `sys_logininfor` VALUES (3116, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:39');
INSERT INTO `sys_logininfor` VALUES (3117, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:39');
INSERT INTO `sys_logininfor` VALUES (3118, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:39');
INSERT INTO `sys_logininfor` VALUES (3119, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:39');
INSERT INTO `sys_logininfor` VALUES (3120, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:39');
INSERT INTO `sys_logininfor` VALUES (3121, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:39');
INSERT INTO `sys_logininfor` VALUES (3122, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:40');
INSERT INTO `sys_logininfor` VALUES (3123, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:40');
INSERT INTO `sys_logininfor` VALUES (3124, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:40');
INSERT INTO `sys_logininfor` VALUES (3125, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:40');
INSERT INTO `sys_logininfor` VALUES (3126, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:40');
INSERT INTO `sys_logininfor` VALUES (3127, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:40');
INSERT INTO `sys_logininfor` VALUES (3128, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:04:41');
INSERT INTO `sys_logininfor` VALUES (3129, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-12-25 16:08:12');
INSERT INTO `sys_logininfor` VALUES (3130, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:50');
INSERT INTO `sys_logininfor` VALUES (3131, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:50');
INSERT INTO `sys_logininfor` VALUES (3132, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:50');
INSERT INTO `sys_logininfor` VALUES (3133, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:50');
INSERT INTO `sys_logininfor` VALUES (3134, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:50');
INSERT INTO `sys_logininfor` VALUES (3135, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:51');
INSERT INTO `sys_logininfor` VALUES (3136, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:51');
INSERT INTO `sys_logininfor` VALUES (3137, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:52');
INSERT INTO `sys_logininfor` VALUES (3138, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:52');
INSERT INTO `sys_logininfor` VALUES (3139, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:52');
INSERT INTO `sys_logininfor` VALUES (3140, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:52');
INSERT INTO `sys_logininfor` VALUES (3141, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:52');
INSERT INTO `sys_logininfor` VALUES (3142, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:52');
INSERT INTO `sys_logininfor` VALUES (3143, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:53');
INSERT INTO `sys_logininfor` VALUES (3144, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:53');
INSERT INTO `sys_logininfor` VALUES (3145, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:53');
INSERT INTO `sys_logininfor` VALUES (3146, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:53');
INSERT INTO `sys_logininfor` VALUES (3147, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:53');
INSERT INTO `sys_logininfor` VALUES (3148, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:54');
INSERT INTO `sys_logininfor` VALUES (3149, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:54');
INSERT INTO `sys_logininfor` VALUES (3150, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:54');
INSERT INTO `sys_logininfor` VALUES (3151, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:54');
INSERT INTO `sys_logininfor` VALUES (3152, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:54');
INSERT INTO `sys_logininfor` VALUES (3153, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:55');
INSERT INTO `sys_logininfor` VALUES (3154, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:55');
INSERT INTO `sys_logininfor` VALUES (3155, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:55');
INSERT INTO `sys_logininfor` VALUES (3156, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:55');
INSERT INTO `sys_logininfor` VALUES (3157, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:55');
INSERT INTO `sys_logininfor` VALUES (3158, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:55');
INSERT INTO `sys_logininfor` VALUES (3159, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:55');
INSERT INTO `sys_logininfor` VALUES (3160, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:55');
INSERT INTO `sys_logininfor` VALUES (3161, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:56');
INSERT INTO `sys_logininfor` VALUES (3162, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:56');
INSERT INTO `sys_logininfor` VALUES (3163, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:56');
INSERT INTO `sys_logininfor` VALUES (3164, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:56');
INSERT INTO `sys_logininfor` VALUES (3165, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:56');
INSERT INTO `sys_logininfor` VALUES (3166, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:56');
INSERT INTO `sys_logininfor` VALUES (3167, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:56');
INSERT INTO `sys_logininfor` VALUES (3168, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:57');
INSERT INTO `sys_logininfor` VALUES (3169, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:57');
INSERT INTO `sys_logininfor` VALUES (3170, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:57');
INSERT INTO `sys_logininfor` VALUES (3171, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:57');
INSERT INTO `sys_logininfor` VALUES (3172, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:57');
INSERT INTO `sys_logininfor` VALUES (3173, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:57');
INSERT INTO `sys_logininfor` VALUES (3174, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:57');
INSERT INTO `sys_logininfor` VALUES (3175, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:57');
INSERT INTO `sys_logininfor` VALUES (3176, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:58');
INSERT INTO `sys_logininfor` VALUES (3177, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:58');
INSERT INTO `sys_logininfor` VALUES (3178, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:58');
INSERT INTO `sys_logininfor` VALUES (3179, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:58');
INSERT INTO `sys_logininfor` VALUES (3180, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:58');
INSERT INTO `sys_logininfor` VALUES (3181, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:58');
INSERT INTO `sys_logininfor` VALUES (3182, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:58');
INSERT INTO `sys_logininfor` VALUES (3183, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:58');
INSERT INTO `sys_logininfor` VALUES (3184, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:58');
INSERT INTO `sys_logininfor` VALUES (3185, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:59');
INSERT INTO `sys_logininfor` VALUES (3186, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:59');
INSERT INTO `sys_logininfor` VALUES (3187, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:59');
INSERT INTO `sys_logininfor` VALUES (3188, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:59');
INSERT INTO `sys_logininfor` VALUES (3189, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:59');
INSERT INTO `sys_logininfor` VALUES (3190, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:59');
INSERT INTO `sys_logininfor` VALUES (3191, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:08:59');
INSERT INTO `sys_logininfor` VALUES (3192, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:00');
INSERT INTO `sys_logininfor` VALUES (3193, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:00');
INSERT INTO `sys_logininfor` VALUES (3194, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:00');
INSERT INTO `sys_logininfor` VALUES (3195, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:00');
INSERT INTO `sys_logininfor` VALUES (3196, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:00');
INSERT INTO `sys_logininfor` VALUES (3197, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:00');
INSERT INTO `sys_logininfor` VALUES (3198, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:00');
INSERT INTO `sys_logininfor` VALUES (3199, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:00');
INSERT INTO `sys_logininfor` VALUES (3200, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:00');
INSERT INTO `sys_logininfor` VALUES (3201, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:00');
INSERT INTO `sys_logininfor` VALUES (3202, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:01');
INSERT INTO `sys_logininfor` VALUES (3203, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:01');
INSERT INTO `sys_logininfor` VALUES (3204, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:01');
INSERT INTO `sys_logininfor` VALUES (3205, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:01');
INSERT INTO `sys_logininfor` VALUES (3206, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:01');
INSERT INTO `sys_logininfor` VALUES (3207, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:02');
INSERT INTO `sys_logininfor` VALUES (3208, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:02');
INSERT INTO `sys_logininfor` VALUES (3209, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:02');
INSERT INTO `sys_logininfor` VALUES (3210, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:02');
INSERT INTO `sys_logininfor` VALUES (3211, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:03');
INSERT INTO `sys_logininfor` VALUES (3212, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:03');
INSERT INTO `sys_logininfor` VALUES (3213, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:03');
INSERT INTO `sys_logininfor` VALUES (3214, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:03');
INSERT INTO `sys_logininfor` VALUES (3215, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:03');
INSERT INTO `sys_logininfor` VALUES (3216, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:03');
INSERT INTO `sys_logininfor` VALUES (3217, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:04');
INSERT INTO `sys_logininfor` VALUES (3218, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:04');
INSERT INTO `sys_logininfor` VALUES (3219, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:04');
INSERT INTO `sys_logininfor` VALUES (3220, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:04');
INSERT INTO `sys_logininfor` VALUES (3221, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:04');
INSERT INTO `sys_logininfor` VALUES (3222, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:04');
INSERT INTO `sys_logininfor` VALUES (3223, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:04');
INSERT INTO `sys_logininfor` VALUES (3224, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:04');
INSERT INTO `sys_logininfor` VALUES (3225, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:05');
INSERT INTO `sys_logininfor` VALUES (3226, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:05');
INSERT INTO `sys_logininfor` VALUES (3227, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:05');
INSERT INTO `sys_logininfor` VALUES (3228, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:05');
INSERT INTO `sys_logininfor` VALUES (3229, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:05');
INSERT INTO `sys_logininfor` VALUES (3230, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:05');
INSERT INTO `sys_logininfor` VALUES (3231, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:05');
INSERT INTO `sys_logininfor` VALUES (3232, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:05');
INSERT INTO `sys_logininfor` VALUES (3233, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:06');
INSERT INTO `sys_logininfor` VALUES (3234, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:05');
INSERT INTO `sys_logininfor` VALUES (3235, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:05');
INSERT INTO `sys_logininfor` VALUES (3236, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:06');
INSERT INTO `sys_logininfor` VALUES (3237, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:06');
INSERT INTO `sys_logininfor` VALUES (3238, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:06');
INSERT INTO `sys_logininfor` VALUES (3239, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:06');
INSERT INTO `sys_logininfor` VALUES (3240, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:06');
INSERT INTO `sys_logininfor` VALUES (3241, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:07');
INSERT INTO `sys_logininfor` VALUES (3242, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:07');
INSERT INTO `sys_logininfor` VALUES (3243, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:07');
INSERT INTO `sys_logininfor` VALUES (3244, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:07');
INSERT INTO `sys_logininfor` VALUES (3245, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:08');
INSERT INTO `sys_logininfor` VALUES (3246, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:08');
INSERT INTO `sys_logininfor` VALUES (3247, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:08');
INSERT INTO `sys_logininfor` VALUES (3248, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:08');
INSERT INTO `sys_logininfor` VALUES (3249, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:08');
INSERT INTO `sys_logininfor` VALUES (3250, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:09');
INSERT INTO `sys_logininfor` VALUES (3251, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:09');
INSERT INTO `sys_logininfor` VALUES (3252, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:09');
INSERT INTO `sys_logininfor` VALUES (3253, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:09');
INSERT INTO `sys_logininfor` VALUES (3254, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:09');
INSERT INTO `sys_logininfor` VALUES (3255, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:09');
INSERT INTO `sys_logininfor` VALUES (3256, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:09');
INSERT INTO `sys_logininfor` VALUES (3257, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:09');
INSERT INTO `sys_logininfor` VALUES (3258, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:09');
INSERT INTO `sys_logininfor` VALUES (3259, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3260, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3261, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3262, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3263, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3264, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3265, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3266, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3267, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3268, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3269, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3270, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3271, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3272, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3273, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3274, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3275, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3276, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3277, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:10');
INSERT INTO `sys_logininfor` VALUES (3278, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:11');
INSERT INTO `sys_logininfor` VALUES (3279, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:12');
INSERT INTO `sys_logininfor` VALUES (3280, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:12');
INSERT INTO `sys_logininfor` VALUES (3281, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:12');
INSERT INTO `sys_logininfor` VALUES (3282, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:12');
INSERT INTO `sys_logininfor` VALUES (3283, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:12');
INSERT INTO `sys_logininfor` VALUES (3284, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:12');
INSERT INTO `sys_logininfor` VALUES (3285, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:12');
INSERT INTO `sys_logininfor` VALUES (3286, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:12');
INSERT INTO `sys_logininfor` VALUES (3287, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:12');
INSERT INTO `sys_logininfor` VALUES (3288, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3289, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3290, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3291, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3292, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3293, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3294, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3295, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3296, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3297, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3298, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3299, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3300, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3301, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:13');
INSERT INTO `sys_logininfor` VALUES (3302, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:14');
INSERT INTO `sys_logininfor` VALUES (3303, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:14');
INSERT INTO `sys_logininfor` VALUES (3304, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:14');
INSERT INTO `sys_logininfor` VALUES (3305, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:14');
INSERT INTO `sys_logininfor` VALUES (3306, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:14');
INSERT INTO `sys_logininfor` VALUES (3307, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:14');
INSERT INTO `sys_logininfor` VALUES (3308, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:14');
INSERT INTO `sys_logininfor` VALUES (3309, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:14');
INSERT INTO `sys_logininfor` VALUES (3310, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:14');
INSERT INTO `sys_logininfor` VALUES (3311, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:14');
INSERT INTO `sys_logininfor` VALUES (3312, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:14');
INSERT INTO `sys_logininfor` VALUES (3313, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:14');
INSERT INTO `sys_logininfor` VALUES (3314, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:15');
INSERT INTO `sys_logininfor` VALUES (3315, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:15');
INSERT INTO `sys_logininfor` VALUES (3316, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:15');
INSERT INTO `sys_logininfor` VALUES (3317, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:15');
INSERT INTO `sys_logininfor` VALUES (3318, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:15');
INSERT INTO `sys_logininfor` VALUES (3319, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:15');
INSERT INTO `sys_logininfor` VALUES (3320, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:15');
INSERT INTO `sys_logininfor` VALUES (3321, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:15');
INSERT INTO `sys_logininfor` VALUES (3322, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:15');
INSERT INTO `sys_logininfor` VALUES (3323, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:15');
INSERT INTO `sys_logininfor` VALUES (3324, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:15');
INSERT INTO `sys_logininfor` VALUES (3325, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:15');
INSERT INTO `sys_logininfor` VALUES (3326, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:16');
INSERT INTO `sys_logininfor` VALUES (3327, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:16');
INSERT INTO `sys_logininfor` VALUES (3328, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:17');
INSERT INTO `sys_logininfor` VALUES (3329, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:17');
INSERT INTO `sys_logininfor` VALUES (3330, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:17');
INSERT INTO `sys_logininfor` VALUES (3331, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:17');
INSERT INTO `sys_logininfor` VALUES (3332, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:17');
INSERT INTO `sys_logininfor` VALUES (3333, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:17');
INSERT INTO `sys_logininfor` VALUES (3334, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:17');
INSERT INTO `sys_logininfor` VALUES (3335, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:17');
INSERT INTO `sys_logininfor` VALUES (3336, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:17');
INSERT INTO `sys_logininfor` VALUES (3337, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:18');
INSERT INTO `sys_logininfor` VALUES (3338, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:18');
INSERT INTO `sys_logininfor` VALUES (3339, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:18');
INSERT INTO `sys_logininfor` VALUES (3340, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:18');
INSERT INTO `sys_logininfor` VALUES (3341, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:18');
INSERT INTO `sys_logininfor` VALUES (3342, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:18');
INSERT INTO `sys_logininfor` VALUES (3343, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:18');
INSERT INTO `sys_logininfor` VALUES (3344, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:18');
INSERT INTO `sys_logininfor` VALUES (3345, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:18');
INSERT INTO `sys_logininfor` VALUES (3346, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:18');
INSERT INTO `sys_logininfor` VALUES (3347, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3348, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3349, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3350, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3351, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3352, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3353, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3354, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3355, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3356, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3357, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3358, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3359, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:19');
INSERT INTO `sys_logininfor` VALUES (3360, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:20');
INSERT INTO `sys_logininfor` VALUES (3361, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:20');
INSERT INTO `sys_logininfor` VALUES (3362, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:20');
INSERT INTO `sys_logininfor` VALUES (3363, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:20');
INSERT INTO `sys_logininfor` VALUES (3364, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:20');
INSERT INTO `sys_logininfor` VALUES (3365, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:20');
INSERT INTO `sys_logininfor` VALUES (3366, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:20');
INSERT INTO `sys_logininfor` VALUES (3367, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:09:20');
INSERT INTO `sys_logininfor` VALUES (3368, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:10:20');
INSERT INTO `sys_logininfor` VALUES (3369, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2024-12-25 16:12:19');
INSERT INTO `sys_logininfor` VALUES (3370, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:29');
INSERT INTO `sys_logininfor` VALUES (3371, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:29');
INSERT INTO `sys_logininfor` VALUES (3372, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:29');
INSERT INTO `sys_logininfor` VALUES (3373, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:29');
INSERT INTO `sys_logininfor` VALUES (3374, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:29');
INSERT INTO `sys_logininfor` VALUES (3375, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:37');
INSERT INTO `sys_logininfor` VALUES (3376, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:37');
INSERT INTO `sys_logininfor` VALUES (3377, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:37');
INSERT INTO `sys_logininfor` VALUES (3378, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:37');
INSERT INTO `sys_logininfor` VALUES (3379, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:37');
INSERT INTO `sys_logininfor` VALUES (3380, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:37');
INSERT INTO `sys_logininfor` VALUES (3381, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:37');
INSERT INTO `sys_logininfor` VALUES (3382, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:37');
INSERT INTO `sys_logininfor` VALUES (3383, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:37');
INSERT INTO `sys_logininfor` VALUES (3384, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:37');
INSERT INTO `sys_logininfor` VALUES (3385, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3386, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3387, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3388, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3389, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3390, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3391, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3392, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3393, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3394, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3395, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3396, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3397, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:39');
INSERT INTO `sys_logininfor` VALUES (3398, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:40');
INSERT INTO `sys_logininfor` VALUES (3399, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:40');
INSERT INTO `sys_logininfor` VALUES (3400, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:40');
INSERT INTO `sys_logininfor` VALUES (3401, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:40');
INSERT INTO `sys_logininfor` VALUES (3402, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:41');
INSERT INTO `sys_logininfor` VALUES (3403, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:41');
INSERT INTO `sys_logininfor` VALUES (3404, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:41');
INSERT INTO `sys_logininfor` VALUES (3405, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:41');
INSERT INTO `sys_logininfor` VALUES (3406, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:41');
INSERT INTO `sys_logininfor` VALUES (3407, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:41');
INSERT INTO `sys_logininfor` VALUES (3408, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:42');
INSERT INTO `sys_logininfor` VALUES (3409, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:42');
INSERT INTO `sys_logininfor` VALUES (3410, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:42');
INSERT INTO `sys_logininfor` VALUES (3411, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:42');
INSERT INTO `sys_logininfor` VALUES (3412, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:42');
INSERT INTO `sys_logininfor` VALUES (3413, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:42');
INSERT INTO `sys_logininfor` VALUES (3414, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:42');
INSERT INTO `sys_logininfor` VALUES (3415, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:42');
INSERT INTO `sys_logininfor` VALUES (3416, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:42');
INSERT INTO `sys_logininfor` VALUES (3417, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:42');
INSERT INTO `sys_logininfor` VALUES (3418, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:42');
INSERT INTO `sys_logininfor` VALUES (3419, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:43');
INSERT INTO `sys_logininfor` VALUES (3420, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:43');
INSERT INTO `sys_logininfor` VALUES (3421, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:43');
INSERT INTO `sys_logininfor` VALUES (3422, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:43');
INSERT INTO `sys_logininfor` VALUES (3423, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:43');
INSERT INTO `sys_logininfor` VALUES (3424, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:43');
INSERT INTO `sys_logininfor` VALUES (3425, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:43');
INSERT INTO `sys_logininfor` VALUES (3426, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:43');
INSERT INTO `sys_logininfor` VALUES (3427, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:44');
INSERT INTO `sys_logininfor` VALUES (3428, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:44');
INSERT INTO `sys_logininfor` VALUES (3429, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:44');
INSERT INTO `sys_logininfor` VALUES (3430, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:44');
INSERT INTO `sys_logininfor` VALUES (3431, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:44');
INSERT INTO `sys_logininfor` VALUES (3432, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:44');
INSERT INTO `sys_logininfor` VALUES (3433, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:44');
INSERT INTO `sys_logininfor` VALUES (3434, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:44');
INSERT INTO `sys_logininfor` VALUES (3435, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:44');
INSERT INTO `sys_logininfor` VALUES (3436, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:44');
INSERT INTO `sys_logininfor` VALUES (3437, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:44');
INSERT INTO `sys_logininfor` VALUES (3438, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:44');
INSERT INTO `sys_logininfor` VALUES (3439, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:45');
INSERT INTO `sys_logininfor` VALUES (3440, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:45');
INSERT INTO `sys_logininfor` VALUES (3441, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:45');
INSERT INTO `sys_logininfor` VALUES (3442, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:45');
INSERT INTO `sys_logininfor` VALUES (3443, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:45');
INSERT INTO `sys_logininfor` VALUES (3444, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:45');
INSERT INTO `sys_logininfor` VALUES (3445, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:45');
INSERT INTO `sys_logininfor` VALUES (3446, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:45');
INSERT INTO `sys_logininfor` VALUES (3447, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:46');
INSERT INTO `sys_logininfor` VALUES (3448, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:46');
INSERT INTO `sys_logininfor` VALUES (3449, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:46');
INSERT INTO `sys_logininfor` VALUES (3450, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:46');
INSERT INTO `sys_logininfor` VALUES (3451, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:46');
INSERT INTO `sys_logininfor` VALUES (3452, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:46');
INSERT INTO `sys_logininfor` VALUES (3453, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:46');
INSERT INTO `sys_logininfor` VALUES (3454, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:46');
INSERT INTO `sys_logininfor` VALUES (3455, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:47');
INSERT INTO `sys_logininfor` VALUES (3456, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:47');
INSERT INTO `sys_logininfor` VALUES (3457, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:47');
INSERT INTO `sys_logininfor` VALUES (3458, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:47');
INSERT INTO `sys_logininfor` VALUES (3459, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:47');
INSERT INTO `sys_logininfor` VALUES (3460, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:47');
INSERT INTO `sys_logininfor` VALUES (3461, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:47');
INSERT INTO `sys_logininfor` VALUES (3462, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:47');
INSERT INTO `sys_logininfor` VALUES (3463, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:47');
INSERT INTO `sys_logininfor` VALUES (3464, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:48');
INSERT INTO `sys_logininfor` VALUES (3465, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:48');
INSERT INTO `sys_logininfor` VALUES (3466, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:48');
INSERT INTO `sys_logininfor` VALUES (3467, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:48');
INSERT INTO `sys_logininfor` VALUES (3468, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:48');
INSERT INTO `sys_logininfor` VALUES (3469, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:48');
INSERT INTO `sys_logininfor` VALUES (3470, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:48');
INSERT INTO `sys_logininfor` VALUES (3471, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:48');
INSERT INTO `sys_logininfor` VALUES (3472, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:49');
INSERT INTO `sys_logininfor` VALUES (3473, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:49');
INSERT INTO `sys_logininfor` VALUES (3474, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:49');
INSERT INTO `sys_logininfor` VALUES (3475, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:49');
INSERT INTO `sys_logininfor` VALUES (3476, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:49');
INSERT INTO `sys_logininfor` VALUES (3477, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:49');
INSERT INTO `sys_logininfor` VALUES (3478, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:49');
INSERT INTO `sys_logininfor` VALUES (3479, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:49');
INSERT INTO `sys_logininfor` VALUES (3480, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:49');
INSERT INTO `sys_logininfor` VALUES (3481, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:49');
INSERT INTO `sys_logininfor` VALUES (3482, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:49');
INSERT INTO `sys_logininfor` VALUES (3483, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:49');
INSERT INTO `sys_logininfor` VALUES (3484, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:50');
INSERT INTO `sys_logininfor` VALUES (3485, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:50');
INSERT INTO `sys_logininfor` VALUES (3486, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:50');
INSERT INTO `sys_logininfor` VALUES (3487, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:50');
INSERT INTO `sys_logininfor` VALUES (3488, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:50');
INSERT INTO `sys_logininfor` VALUES (3489, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:50');
INSERT INTO `sys_logininfor` VALUES (3490, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:50');
INSERT INTO `sys_logininfor` VALUES (3491, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:50');
INSERT INTO `sys_logininfor` VALUES (3492, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:50');
INSERT INTO `sys_logininfor` VALUES (3493, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:50');
INSERT INTO `sys_logininfor` VALUES (3494, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:50');
INSERT INTO `sys_logininfor` VALUES (3495, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:50');
INSERT INTO `sys_logininfor` VALUES (3496, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:51');
INSERT INTO `sys_logininfor` VALUES (3497, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:51');
INSERT INTO `sys_logininfor` VALUES (3498, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:52');
INSERT INTO `sys_logininfor` VALUES (3499, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:52');
INSERT INTO `sys_logininfor` VALUES (3500, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:52');
INSERT INTO `sys_logininfor` VALUES (3501, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:52');
INSERT INTO `sys_logininfor` VALUES (3502, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:52');
INSERT INTO `sys_logininfor` VALUES (3503, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:52');
INSERT INTO `sys_logininfor` VALUES (3504, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:53');
INSERT INTO `sys_logininfor` VALUES (3505, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:53');
INSERT INTO `sys_logininfor` VALUES (3506, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:53');
INSERT INTO `sys_logininfor` VALUES (3507, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:53');
INSERT INTO `sys_logininfor` VALUES (3508, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:53');
INSERT INTO `sys_logininfor` VALUES (3509, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:53');
INSERT INTO `sys_logininfor` VALUES (3510, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:53');
INSERT INTO `sys_logininfor` VALUES (3511, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:53');
INSERT INTO `sys_logininfor` VALUES (3512, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:53');
INSERT INTO `sys_logininfor` VALUES (3513, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:54');
INSERT INTO `sys_logininfor` VALUES (3514, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:54');
INSERT INTO `sys_logininfor` VALUES (3515, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:54');
INSERT INTO `sys_logininfor` VALUES (3516, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:54');
INSERT INTO `sys_logininfor` VALUES (3517, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:54');
INSERT INTO `sys_logininfor` VALUES (3518, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:54');
INSERT INTO `sys_logininfor` VALUES (3519, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:54');
INSERT INTO `sys_logininfor` VALUES (3520, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:54');
INSERT INTO `sys_logininfor` VALUES (3521, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:54');
INSERT INTO `sys_logininfor` VALUES (3522, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:54');
INSERT INTO `sys_logininfor` VALUES (3523, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3524, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3525, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3526, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3527, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3528, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3529, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3530, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3531, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3532, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3533, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3534, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3535, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3536, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3537, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3538, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:55');
INSERT INTO `sys_logininfor` VALUES (3539, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:56');
INSERT INTO `sys_logininfor` VALUES (3540, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:56');
INSERT INTO `sys_logininfor` VALUES (3541, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:56');
INSERT INTO `sys_logininfor` VALUES (3542, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:57');
INSERT INTO `sys_logininfor` VALUES (3543, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:57');
INSERT INTO `sys_logininfor` VALUES (3544, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:57');
INSERT INTO `sys_logininfor` VALUES (3545, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:57');
INSERT INTO `sys_logininfor` VALUES (3546, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:57');
INSERT INTO `sys_logininfor` VALUES (3547, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:57');
INSERT INTO `sys_logininfor` VALUES (3548, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:57');
INSERT INTO `sys_logininfor` VALUES (3549, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:57');
INSERT INTO `sys_logininfor` VALUES (3550, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:58');
INSERT INTO `sys_logininfor` VALUES (3551, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:58');
INSERT INTO `sys_logininfor` VALUES (3552, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:58');
INSERT INTO `sys_logininfor` VALUES (3553, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:58');
INSERT INTO `sys_logininfor` VALUES (3554, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:58');
INSERT INTO `sys_logininfor` VALUES (3555, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:58');
INSERT INTO `sys_logininfor` VALUES (3556, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:58');
INSERT INTO `sys_logininfor` VALUES (3557, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:58');
INSERT INTO `sys_logininfor` VALUES (3558, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:58');
INSERT INTO `sys_logininfor` VALUES (3559, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3560, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3561, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3562, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3563, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3564, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3565, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3566, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3567, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3568, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3569, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3570, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3571, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:15:59');
INSERT INTO `sys_logininfor` VALUES (3572, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:19:23');
INSERT INTO `sys_logininfor` VALUES (3573, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:19:23');
INSERT INTO `sys_logininfor` VALUES (3574, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:19:23');
INSERT INTO `sys_logininfor` VALUES (3575, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:19:23');
INSERT INTO `sys_logininfor` VALUES (3576, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:19:23');
INSERT INTO `sys_logininfor` VALUES (3577, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:05');
INSERT INTO `sys_logininfor` VALUES (3578, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:08');
INSERT INTO `sys_logininfor` VALUES (3579, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:23');
INSERT INTO `sys_logininfor` VALUES (3580, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:23');
INSERT INTO `sys_logininfor` VALUES (3581, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:23');
INSERT INTO `sys_logininfor` VALUES (3582, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:23');
INSERT INTO `sys_logininfor` VALUES (3583, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:23');
INSERT INTO `sys_logininfor` VALUES (3584, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:23');
INSERT INTO `sys_logininfor` VALUES (3585, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:29');
INSERT INTO `sys_logininfor` VALUES (3586, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:29');
INSERT INTO `sys_logininfor` VALUES (3587, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:29');
INSERT INTO `sys_logininfor` VALUES (3588, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:29');
INSERT INTO `sys_logininfor` VALUES (3589, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:20:29');
INSERT INTO `sys_logininfor` VALUES (3590, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:09');
INSERT INTO `sys_logininfor` VALUES (3591, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:09');
INSERT INTO `sys_logininfor` VALUES (3592, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:09');
INSERT INTO `sys_logininfor` VALUES (3593, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:09');
INSERT INTO `sys_logininfor` VALUES (3594, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:09');
INSERT INTO `sys_logininfor` VALUES (3595, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:09');
INSERT INTO `sys_logininfor` VALUES (3596, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:11');
INSERT INTO `sys_logininfor` VALUES (3597, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:11');
INSERT INTO `sys_logininfor` VALUES (3598, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:11');
INSERT INTO `sys_logininfor` VALUES (3599, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:11');
INSERT INTO `sys_logininfor` VALUES (3600, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:11');
INSERT INTO `sys_logininfor` VALUES (3601, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:12');
INSERT INTO `sys_logininfor` VALUES (3602, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:12');
INSERT INTO `sys_logininfor` VALUES (3603, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:12');
INSERT INTO `sys_logininfor` VALUES (3604, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:12');
INSERT INTO `sys_logininfor` VALUES (3605, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:12');
INSERT INTO `sys_logininfor` VALUES (3606, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:12');
INSERT INTO `sys_logininfor` VALUES (3607, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:13');
INSERT INTO `sys_logininfor` VALUES (3608, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:13');
INSERT INTO `sys_logininfor` VALUES (3609, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:13');
INSERT INTO `sys_logininfor` VALUES (3610, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:13');
INSERT INTO `sys_logininfor` VALUES (3611, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:13');
INSERT INTO `sys_logininfor` VALUES (3612, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:14');
INSERT INTO `sys_logininfor` VALUES (3613, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:14');
INSERT INTO `sys_logininfor` VALUES (3614, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:30');
INSERT INTO `sys_logininfor` VALUES (3615, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:30');
INSERT INTO `sys_logininfor` VALUES (3616, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:30');
INSERT INTO `sys_logininfor` VALUES (3617, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:30');
INSERT INTO `sys_logininfor` VALUES (3618, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:30');
INSERT INTO `sys_logininfor` VALUES (3619, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:21:30');
INSERT INTO `sys_logininfor` VALUES (3620, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:24:31');
INSERT INTO `sys_logininfor` VALUES (3621, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:24:38');
INSERT INTO `sys_logininfor` VALUES (3622, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:24:38');
INSERT INTO `sys_logininfor` VALUES (3623, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:24:38');
INSERT INTO `sys_logininfor` VALUES (3624, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:24:38');
INSERT INTO `sys_logininfor` VALUES (3625, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:24:38');
INSERT INTO `sys_logininfor` VALUES (3626, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:27:15');
INSERT INTO `sys_logininfor` VALUES (3627, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:27:15');
INSERT INTO `sys_logininfor` VALUES (3628, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:27:15');
INSERT INTO `sys_logininfor` VALUES (3629, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:27:15');
INSERT INTO `sys_logininfor` VALUES (3630, 'admin', '', '内网IP', 'Other', 'Windows', '0', '登录成功', '2024-12-25 16:27:15');
INSERT INTO `sys_logininfor` VALUES (3631, 'admin', '', '内网IP', 'Chrome 120', 'Windows 10', '0', '登录成功', '2025-01-04 09:17:56');
INSERT INTO `sys_logininfor` VALUES (3632, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2025-01-04 09:28:46');
INSERT INTO `sys_logininfor` VALUES (3633, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2025-02-08 10:28:01');
INSERT INTO `sys_logininfor` VALUES (3634, 'admin', '', '内网IP', 'Chrome 120', 'Windows 10', '0', '登录成功', '2025-02-08 10:39:42');
INSERT INTO `sys_logininfor` VALUES (3635, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2025-02-08 11:16:53');
INSERT INTO `sys_logininfor` VALUES (3636, 'admin', '', '内网IP', 'Chrome 120', 'Windows 10', '0', '登录成功', '2025-02-08 13:52:09');
INSERT INTO `sys_logininfor` VALUES (3637, 'admin', '', '内网IP', 'Other', 'Other', '0', '登录成功', '2025-02-08 14:17:56');
INSERT INTO `sys_logininfor` VALUES (3638, 'admin', '', '内网IP', 'Chrome 120', 'Windows 10', '0', '登录成功', '2025-02-19 16:20:55');
INSERT INTO `sys_logininfor` VALUES (3639, 'admin', '', '内网IP', 'Chrome 120', 'Windows 10', '0', '登录成功', '2025-02-19 17:14:36');
INSERT INTO `sys_logininfor` VALUES (3640, 'admin', '', '内网IP', 'Chrome 120', 'Windows 10', '1', '验证码错误', '2025-04-07 16:43:10');
INSERT INTO `sys_logininfor` VALUES (3641, 'admin', '', '内网IP', 'Chrome 120', 'Windows 10', '0', '登录成功', '2025-04-07 16:43:12');
INSERT INTO `sys_logininfor` VALUES (3642, 'admin', '', '内网IP', 'Chrome 135', 'Windows 10', '0', '登录成功', '2025-04-14 11:24:32');
INSERT INTO `sys_logininfor` VALUES (3643, 'admin', '', '内网IP', 'Chrome 135', 'Windows 10', '0', '登录成功', '2025-04-14 13:59:40');
INSERT INTO `sys_logininfor` VALUES (3644, 'admin', '', '内网IP', 'Chrome 135', 'Windows 10', '0', '登录成功', '2025-04-16 10:07:20');

-- ----------------------------
-- Table structure for sys_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu`  (
  `menu_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '菜单ID',
  `menu_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '菜单名称',
  `parent_id` bigint(0) NULL DEFAULT 0 COMMENT '父菜单ID',
  `order_num` int(0) NULL DEFAULT 0 COMMENT '显示顺序',
  `path` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '路由地址',
  `component` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '组件路径',
  `query` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '路由参数',
  `route_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '路由名称',
  `is_frame` int(0) NULL DEFAULT 1 COMMENT '是否为外链（0是 1否）',
  `is_cache` int(0) NULL DEFAULT 0 COMMENT '是否缓存（0缓存 1不缓存）',
  `menu_type` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '菜单类型（M目录 C菜单 F按钮）',
  `visible` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '菜单状态（0显示 1隐藏）',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '菜单状态（0正常 1停用）',
  `perms` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限标识',
  `icon` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '#' COMMENT '菜单图标',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '备注',
  PRIMARY KEY (`menu_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2043 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '菜单权限表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_menu
-- ----------------------------
INSERT INTO `sys_menu` VALUES (1, '系统管理', 0, 2, 'system', NULL, '', '', 1, 0, 'M', '0', '0', '', 'system', 'admin', '2024-08-13 18:18:19', 'admin', '2024-10-15 11:39:33', '系统管理目录');
INSERT INTO `sys_menu` VALUES (2, '系统监控', 0, 3, 'monitor', NULL, '', '', 1, 0, 'M', '0', '0', '', 'monitor', 'admin', '2024-08-13 18:18:19', 'admin', '2024-10-15 11:39:47', '系统监控目录');
INSERT INTO `sys_menu` VALUES (3, '系统工具', 0, 4, 'tool', NULL, '', '', 1, 0, 'M', '0', '0', '', 'tool', 'admin', '2024-08-13 18:18:19', 'admin', '2024-09-16 10:33:46', '系统工具目录');
INSERT INTO `sys_menu` VALUES (100, '用户管理', 1, 1, 'user', 'system/user/index', '', '', 1, 0, 'C', '0', '0', 'system:user:list', 'user', 'admin', '2024-08-13 18:18:19', '', NULL, '用户管理菜单');
INSERT INTO `sys_menu` VALUES (101, '角色管理', 1, 2, 'role', 'system/role/index', '', '', 1, 0, 'C', '0', '0', 'system:role:list', 'peoples', 'admin', '2024-08-13 18:18:19', '', NULL, '角色管理菜单');
INSERT INTO `sys_menu` VALUES (102, '菜单管理', 1, 3, 'menu', 'system/menu/index', '', '', 1, 0, 'C', '0', '0', 'system:menu:list', 'tree-table', 'admin', '2024-08-13 18:18:19', '', NULL, '菜单管理菜单');
INSERT INTO `sys_menu` VALUES (103, '部门管理', 1, 4, 'dept', 'system/dept/index', '', '', 1, 0, 'C', '0', '0', 'system:dept:list', 'tree', 'admin', '2024-08-13 18:18:19', '', NULL, '部门管理菜单');
INSERT INTO `sys_menu` VALUES (104, '岗位管理', 1, 5, 'post', 'system/post/index', '', '', 1, 0, 'C', '0', '0', 'system:post:list', 'post', 'admin', '2024-08-13 18:18:19', '', NULL, '岗位管理菜单');
INSERT INTO `sys_menu` VALUES (105, '字典管理', 1, 6, 'dict', 'system/dict/index', '', '', 1, 0, 'C', '0', '0', 'system:dict:list', 'dict', 'admin', '2024-08-13 18:18:19', '', NULL, '字典管理菜单');
INSERT INTO `sys_menu` VALUES (106, '参数设置', 1, 7, 'config', 'system/config/index', '', '', 1, 0, 'C', '0', '0', 'system:config:list', 'edit', 'admin', '2024-08-13 18:18:19', '', NULL, '参数设置菜单');
INSERT INTO `sys_menu` VALUES (107, '通知公告', 1, 8, 'notice', 'system/notice/index', '', '', 1, 0, 'C', '0', '0', 'system:notice:list', 'message', 'admin', '2024-08-13 18:18:19', '', NULL, '通知公告菜单');
INSERT INTO `sys_menu` VALUES (108, '日志管理', 1, 9, 'log', '', '', '', 1, 0, 'M', '0', '0', '', 'log', 'admin', '2024-08-13 18:18:19', '', NULL, '日志管理菜单');
INSERT INTO `sys_menu` VALUES (109, '在线用户', 2, 1, 'online', 'monitor/online/index', '', '', 1, 0, 'C', '0', '0', 'monitor:online:list', 'online', 'admin', '2024-08-13 18:18:19', '', NULL, '在线用户菜单');
INSERT INTO `sys_menu` VALUES (110, '定时任务', 2, 2, 'job', 'monitor/job/index', '', '', 1, 0, 'C', '0', '0', 'monitor:job:list', 'job', 'admin', '2024-08-13 18:18:19', '', NULL, '定时任务菜单');
INSERT INTO `sys_menu` VALUES (111, '数据监控', 2, 3, 'druid', 'monitor/druid/index', '', '', 1, 0, 'C', '0', '0', 'monitor:druid:list', 'druid', 'admin', '2024-08-13 18:18:19', '', NULL, '数据监控菜单');
INSERT INTO `sys_menu` VALUES (112, '服务监控', 2, 4, 'server', 'monitor/server/index', '', '', 1, 0, 'C', '0', '0', 'monitor:server:list', 'server', 'admin', '2024-08-13 18:18:19', '', NULL, '服务监控菜单');
INSERT INTO `sys_menu` VALUES (113, '缓存监控', 2, 5, 'cache', 'monitor/cache/index', '', '', 1, 0, 'C', '0', '0', 'monitor:cache:list', 'redis', 'admin', '2024-08-13 18:18:19', '', NULL, '缓存监控菜单');
INSERT INTO `sys_menu` VALUES (114, '缓存列表', 2, 6, 'cacheList', 'monitor/cache/list', '', '', 1, 0, 'C', '0', '0', 'monitor:cache:list', 'redis-list', 'admin', '2024-08-13 18:18:19', '', NULL, '缓存列表菜单');
INSERT INTO `sys_menu` VALUES (115, '表单构建', 3, 1, 'build', 'tool/build/index', '', '', 1, 0, 'C', '0', '0', 'tool:build:list', 'build', 'admin', '2024-08-13 18:18:19', '', NULL, '表单构建菜单');
INSERT INTO `sys_menu` VALUES (116, '代码生成', 3, 2, 'gen', 'tool/gen/index', '', '', 1, 0, 'C', '0', '0', 'tool:gen:list', 'code', 'admin', '2024-08-13 18:18:19', 'admin', '2025-02-19 16:25:53', '代码生成菜单');
INSERT INTO `sys_menu` VALUES (117, '系统接口', 3, 3, 'swagger', 'tool/swagger/index', '', '', 1, 0, 'C', '0', '0', 'tool:swagger:list', 'swagger', 'admin', '2024-08-13 18:18:19', '', NULL, '系统接口菜单');
INSERT INTO `sys_menu` VALUES (500, '操作日志', 108, 1, 'operlog', 'monitor/operlog/index', '', '', 1, 0, 'C', '0', '0', 'monitor:operlog:list', 'form', 'admin', '2024-08-13 18:18:19', '', NULL, '操作日志菜单');
INSERT INTO `sys_menu` VALUES (501, '登录日志', 108, 2, 'logininfor', 'monitor/logininfor/index', '', '', 1, 0, 'C', '0', '0', 'monitor:logininfor:list', 'logininfor', 'admin', '2024-08-13 18:18:19', '', NULL, '登录日志菜单');
INSERT INTO `sys_menu` VALUES (1000, '用户查询', 100, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1001, '用户新增', 100, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:add', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1002, '用户修改', 100, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:edit', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1003, '用户删除', 100, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:remove', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1004, '用户导出', 100, 5, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:export', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1005, '用户导入', 100, 6, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:import', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1006, '重置密码', 100, 7, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:resetPwd', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1007, '角色查询', 101, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1008, '角色新增', 101, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:add', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1009, '角色修改', 101, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:edit', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1010, '角色删除', 101, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:remove', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1011, '角色导出', 101, 5, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:export', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1012, '菜单查询', 102, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:menu:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1013, '菜单新增', 102, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:menu:add', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1014, '菜单修改', 102, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:menu:edit', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1015, '菜单删除', 102, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:menu:remove', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1016, '部门查询', 103, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:dept:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1017, '部门新增', 103, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:dept:add', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1018, '部门修改', 103, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:dept:edit', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1019, '部门删除', 103, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:dept:remove', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1020, '岗位查询', 104, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1021, '岗位新增', 104, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:add', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1022, '岗位修改', 104, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:edit', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1023, '岗位删除', 104, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:remove', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1024, '岗位导出', 104, 5, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:export', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1025, '字典查询', 105, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1026, '字典新增', 105, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:add', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1027, '字典修改', 105, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:edit', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1028, '字典删除', 105, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:remove', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1029, '字典导出', 105, 5, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:export', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1030, '参数查询', 106, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1031, '参数新增', 106, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:add', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1032, '参数修改', 106, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:edit', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1033, '参数删除', 106, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:remove', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1034, '参数导出', 106, 5, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:export', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1035, '公告查询', 107, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:notice:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1036, '公告新增', 107, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:notice:add', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1037, '公告修改', 107, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:notice:edit', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1038, '公告删除', 107, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:notice:remove', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1039, '操作查询', 500, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:operlog:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1040, '操作删除', 500, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:operlog:remove', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1041, '日志导出', 500, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:operlog:export', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1042, '登录查询', 501, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:logininfor:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1043, '登录删除', 501, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:logininfor:remove', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1044, '日志导出', 501, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:logininfor:export', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1045, '账户解锁', 501, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:logininfor:unlock', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1046, '在线查询', 109, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:online:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1047, '批量强退', 109, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:online:batchLogout', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1048, '单条强退', 109, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:online:forceLogout', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1049, '任务查询', 110, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1050, '任务新增', 110, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:add', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1051, '任务修改', 110, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:edit', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1052, '任务删除', 110, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:remove', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1053, '状态修改', 110, 5, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:changeStatus', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1054, '任务导出', 110, 6, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:export', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1055, '生成查询', 116, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:query', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1056, '生成修改', 116, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:edit', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1057, '生成删除', 116, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:remove', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1058, '导入代码', 116, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:import', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1059, '预览代码', 116, 5, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:preview', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1060, '生成代码', 116, 6, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:code', '#', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_menu` VALUES (2001, '项目/模块', 0, 0, 'project', NULL, NULL, '', 1, 0, 'M', '0', '0', NULL, 'dict', 'admin', '2024-09-10 15:30:34', 'admin', '2024-09-10 15:31:53', '');
INSERT INTO `sys_menu` VALUES (2002, '项目列表', 2001, 1, 'project', 'project/index', NULL, '', 1, 0, 'C', '0', '0', 'auto:project:list', 'date', 'admin', '2024-09-10 15:32:32', 'admin', '2024-09-10 15:40:20', '');
INSERT INTO `sys_menu` VALUES (2003, '项目新增', 2002, 1, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'auto:project:add', '#', 'admin', '2024-09-10 15:41:06', 'admin', '2024-09-10 15:42:40', '');
INSERT INTO `sys_menu` VALUES (2004, '项目编辑', 2002, 2, 'auto:project:edit', NULL, NULL, '', 1, 0, 'F', '0', '0', 'auto:project:edit', '#', 'admin', '2024-09-10 15:41:25', 'admin', '2024-09-10 15:43:35', '');
INSERT INTO `sys_menu` VALUES (2005, '项目删除', 2002, 3, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'auto:project:remove', '#', 'admin', '2024-09-10 15:41:53', 'admin', '2024-09-10 15:42:52', '');
INSERT INTO `sys_menu` VALUES (2006, '项目查询', 2002, 0, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'auto:project:query', '#', 'admin', '2024-09-10 15:42:28', 'admin', '2024-09-10 15:42:28', '');
INSERT INTO `sys_menu` VALUES (2007, '通用配置', 0, 5, 'commonConfig', NULL, NULL, '', 1, 0, 'M', '0', '0', NULL, 'slider', 'admin', '2024-09-16 10:31:57', 'admin', '2024-10-15 11:39:53', '');
INSERT INTO `sys_menu` VALUES (2008, ' 机器人管理', 2007, 0, 'robot', 'robot/index', NULL, '', 1, 0, 'C', '0', '0', 'notify:robots:list', 'message', 'admin', '2024-09-16 10:32:51', 'admin', '2024-09-18 15:26:08', '');
INSERT INTO `sys_menu` VALUES (2009, '机器人查询', 2008, 0, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'notify:robots:query', '#', 'admin', '2024-09-16 10:36:51', 'admin', '2024-09-16 10:38:55', '');
INSERT INTO `sys_menu` VALUES (2010, ' 机器人新增', 2008, 1, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'notify:robots:add', '#', 'admin', '2024-09-16 10:37:29', 'admin', '2024-09-16 10:37:29', '');
INSERT INTO `sys_menu` VALUES (2011, ' 机器人编辑', 2008, 2, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'notify:robots:edit', '#', 'admin', '2024-09-16 10:37:54', 'admin', '2024-09-16 10:37:54', '');
INSERT INTO `sys_menu` VALUES (2012, '机器人删除', 2008, 3, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'notify:robots:remove', '#', 'admin', '2024-09-16 10:38:15', 'admin', '2024-09-16 10:38:15', '');
INSERT INTO `sys_menu` VALUES (2013, '数据源管理', 2007, 1, 'dataSource', 'datasource/index', NULL, '', 1, 0, 'C', '0', '0', 'commonConfig:dataSource:list', 'date', 'admin', '2024-09-18 15:33:10', 'admin', '2024-09-18 15:34:51', '');
INSERT INTO `sys_menu` VALUES (2014, ' 数据源查询', 2013, 0, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'commonConfig:dataSource:query', '#', 'admin', '2024-09-18 18:19:06', 'admin', '2024-09-18 18:19:06', '');
INSERT INTO `sys_menu` VALUES (2016, '数据源新增', 2013, 1, '', NULL, NULL, '', 1, 0, 'F', '0', '0', '	 commonConfig:dataSource:add', '#', 'admin', '2024-09-20 22:33:00', 'admin', '2024-09-20 22:33:00', '');
INSERT INTO `sys_menu` VALUES (2017, '数据源编辑', 2013, 2, '', NULL, NULL, '', 1, 0, 'F', '0', '0', '	 commonConfig:dataSource:edit', '#', 'admin', '2024-09-20 22:33:19', 'admin', '2024-09-20 22:33:19', '');
INSERT INTO `sys_menu` VALUES (2018, '数据源删除', 2013, 3, '', NULL, NULL, '', 1, 0, 'F', '0', '0', '	 commonConfig:dataSource:remove', '#', 'admin', '2024-09-20 22:33:41', 'admin', '2024-09-20 22:33:41', '');
INSERT INTO `sys_menu` VALUES (2021, ' 数据查询', 3, 4, 'querydb', 'tool/querydb/index', NULL, '', 1, 0, 'C', '0', '0', 'commonConfig:dataSource:list', '404', 'admin', '2024-09-22 17:17:34', 'admin', '2024-10-15 17:20:00', '');
INSERT INTO `sys_menu` VALUES (2022, '执行SQL', 2021, 0, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'commonConfig:dataSource:execute', '#', 'admin', '2024-09-22 17:19:53', 'admin', '2024-10-15 17:20:59', '');
INSERT INTO `sys_menu` VALUES (2023, 'API测试', 0, 1, 'apiTest', NULL, NULL, '', 1, 0, 'M', '0', '0', NULL, 'clipboard', 'admin', '2024-10-15 11:38:42', 'admin', '2024-10-15 11:40:07', '');
INSERT INTO `sys_menu` VALUES (2024, '接口管理', 2023, 1, 'apiInfo', 'apiInfo/index', NULL, '', 1, 0, 'C', '0', '0', 'apitest:apiInfo:list', 'checkbox', 'admin', '2024-10-15 11:42:18', 'admin', '2024-10-15 13:49:05', '');
INSERT INTO `sys_menu` VALUES (2025, '接口查询', 2024, 0, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'apitest:apiInfo:query', '#', 'admin', '2024-10-15 11:42:50', 'admin', '2024-10-15 11:43:17', '');
INSERT INTO `sys_menu` VALUES (2026, '接口新增', 2024, 1, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'apitest:apiInfo:add', '#', 'admin', '2024-10-15 11:43:38', 'admin', '2024-10-15 11:43:38', '');
INSERT INTO `sys_menu` VALUES (2027, '接口编辑', 2024, 2, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'apitest:apiInfo:edit', '#', 'admin', '2024-10-15 11:43:55', 'admin', '2024-10-15 11:43:55', '');
INSERT INTO `sys_menu` VALUES (2028, '接口删除', 2024, 3, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'apitest:apiInfo:remove', '#', 'admin', '2024-10-15 11:44:12', 'admin', '2024-10-15 11:44:12', '');
INSERT INTO `sys_menu` VALUES (2029, '接口测试', 2024, 4, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'apitest:apiInfo:debug', '#', 'admin', '2024-10-15 11:44:29', 'admin', '2024-10-15 11:44:29', '');
INSERT INTO `sys_menu` VALUES (2030, '环境管理', 2007, 2, 'env', 'envinfo/index', NULL, '', 1, 0, 'C', '0', '0', 'env:envInfo:list', 'cascader', 'admin', '2024-10-31 22:07:51', 'admin', '2024-10-31 22:07:51', NULL);
INSERT INTO `sys_menu` VALUES (2031, '环境查询', 2030, 0, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'env:envInfo:query', '#', 'admin', '2024-10-31 22:08:38', 'admin', '2024-10-31 22:08:38', NULL);
INSERT INTO `sys_menu` VALUES (2032, '环境新增', 2030, 1, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'env:envInfo:add', '#', 'admin', '2024-10-31 22:09:29', 'admin', '2024-10-31 22:09:29', NULL);
INSERT INTO `sys_menu` VALUES (2033, '环境编辑', 2030, 2, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'env:envInfo:edit', '#', 'admin', '2024-10-31 22:09:46', 'admin', '2024-10-31 22:09:46', NULL);
INSERT INTO `sys_menu` VALUES (2034, '环境删除', 2030, 3, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'env:envInfo:remove', '#', 'admin', '2024-10-31 22:10:12', 'admin', '2024-10-31 22:10:12', NULL);
INSERT INTO `sys_menu` VALUES (2035, '测试用例', 2023, 2, 'apiCase', 'apiCase/index', NULL, '', 1, 0, 'C', '0', '0', 'testcase:testcaseInfo:list', 'button', 'admin', '2024-12-24 15:46:50', 'admin', '2025-01-04 09:34:01', NULL);
INSERT INTO `sys_menu` VALUES (2036, '用例查询', 2035, 0, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'testcase:testcaseInfo:query', '#', 'admin', '2025-01-04 09:35:02', 'admin', '2025-01-04 09:35:02', NULL);
INSERT INTO `sys_menu` VALUES (2038, '用例新增', 2035, 1, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'testcase:testcaseInfo:add', '#', 'admin', '2025-01-04 09:35:50', 'admin', '2025-01-04 09:35:50', NULL);
INSERT INTO `sys_menu` VALUES (2039, '用例编辑', 2035, 2, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'testcase:testcaseInfo:edit', '#', 'admin', '2025-01-04 09:36:09', 'admin', '2025-01-04 09:36:41', NULL);
INSERT INTO `sys_menu` VALUES (2040, '用例删除', 2035, 3, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'testcase:testcaseInfo:remove', '#', 'admin', '2025-01-04 09:36:34', 'admin', '2025-01-04 09:36:34', NULL);
INSERT INTO `sys_menu` VALUES (2041, '用例运行', 2035, 4, '', NULL, NULL, '', 1, 0, 'F', '0', '0', 'testcase:testcaseInfo:batch', '#', 'admin', '2025-01-04 09:37:08', 'admin', '2025-01-04 09:37:08', NULL);
INSERT INTO `sys_menu` VALUES (2042, 'AI管家', 0, 4, 'ai_chat', 'ai/chat/index', NULL, '', 1, 0, 'C', '0', '0', '', '404', 'admin', '2025-04-16 10:19:18', 'admin', '2025-04-16 10:19:49', NULL);

-- ----------------------------
-- Table structure for sys_notice
-- ----------------------------
DROP TABLE IF EXISTS `sys_notice`;
CREATE TABLE `sys_notice`  (
  `notice_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '公告ID',
  `notice_title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公告标题',
  `notice_type` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公告类型（1通知 2公告）',
  `notice_content` longblob NULL COMMENT '公告内容',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '公告状态（0正常 1关闭）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`notice_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '通知公告表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_notice
-- ----------------------------
INSERT INTO `sys_notice` VALUES (1, '温馨提醒：2018-07-01 vfadmin新版本发布啦', '2', 0xE696B0E78988E69CACE58685E5AEB9, '0', 'admin', '2024-08-13 18:18:19', '', NULL, '管理员');
INSERT INTO `sys_notice` VALUES (2, '维护通知：2018-07-01 vfadmin系统凌晨维护', '1', 0xE7BBB4E68AA4E58685E5AEB9, '0', 'admin', '2024-08-13 18:18:19', '', NULL, '管理员');

-- ----------------------------
-- Table structure for sys_oper_log
-- ----------------------------
DROP TABLE IF EXISTS `sys_oper_log`;
CREATE TABLE `sys_oper_log`  (
  `oper_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '日志主键',
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '模块标题',
  `business_type` int(0) NULL DEFAULT 0 COMMENT '业务类型（0其它 1新增 2修改 3删除）',
  `method` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '方法名称',
  `request_method` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '请求方式',
  `operator_type` int(0) NULL DEFAULT 0 COMMENT '操作类别（0其它 1后台用户 2手机端用户）',
  `oper_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '操作人员',
  `dept_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '部门名称',
  `oper_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '请求URL',
  `oper_ip` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '主机地址',
  `oper_location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '操作地点',
  `oper_param` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '请求参数',
  `json_result` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '返回参数',
  `status` int(0) NULL DEFAULT 0 COMMENT '操作状态（0正常 1异常）',
  `error_msg` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '错误消息',
  `oper_time` datetime(0) NULL DEFAULT NULL COMMENT '操作时间',
  `cost_time` bigint(0) NULL DEFAULT 0 COMMENT '消耗时间',
  PRIMARY KEY (`oper_id`) USING BTREE,
  INDEX `idx_sys_oper_log_bt`(`business_type`) USING BTREE,
  INDEX `idx_sys_oper_log_s`(`status`) USING BTREE,
  INDEX `idx_sys_oper_log_ot`(`oper_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1064 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '操作日志记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_oper_log
-- ----------------------------
INSERT INTO `sys_oper_log` VALUES (934, '接口', 1, 'module_admin.controller.api_controller.add_api()', 'POST', 0, 'admin', '研发部门', '/dev-api/apitest/apiInfo', '', '内网IP', '{\"apiId\": 90, \"apiName\": \"90\", \"projectId\": 1, \"apiMethod\": \"GET\", \"apiUrl\": \"/login\", \"apiStatus\": \"0\", \"apiLevel\": \"P1\", \"apiTags\": [\"登录\", \"注册\"], \"requestDataType\": 1, \"requestData\": [{\"name\": \"ranyong\"}], \"requestHeaders\": [{\"key\": \"Authorization\", \"value\": \"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImE1YzQ5MDhhLTNjMTgtNDE1Ni1hNTkwLWFkMGIyZDY1NDNhYSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTEyLjk2LjIyNC4xMzgiLCJsb2dpbkxvY2F0aW9uIjoiXHU0ZTlhXHU2ZDMyLVx1NWU3Zlx1NGUxY1x1NzcwMSIsImJyb3dzZXIiOiJDaHJvbWUgMTA5Iiwib3MiOiJNYWMgT1MgWCAxMCIsImxvZ2luVGltZSI6IjIwMjQtMDktMjYgMjA6NTc6MzMifSwiZXhwIjoxNzI3NDQxODUzfQ.UMV9sONUcsMOje0eMmrfwJRlzST29DsQR5XaPinsSiU\", \"remarks\": \"这是一个请求头\"}], \"createBy\": \"admin\", \"createTime\": \"2024-10-08T21:30:43\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-08T21:30:43\", \"remark\": \"string\"}', '{\"code\": 200, \"msg\": \"新增接口成功\", \"success\": true, \"time\": \"2024-10-15T10:34:17.944653\"}', 0, '', '2024-10-15 10:34:18', 0);
INSERT INTO `sys_oper_log` VALUES (935, '接口', 1, 'module_admin.controller.api_controller.add_api()', 'POST', 0, 'admin', '研发部门', '/dev-api/apitest/apiInfo', '', '内网IP', '{\"apiId\": 90, \"apiName\": \"90\", \"projectId\": 1, \"apiMethod\": \"GET\", \"apiUrl\": \"/login\", \"apiStatus\": \"0\", \"apiLevel\": \"P1\", \"apiTags\": [\"登录\", \"注册\"], \"requestDataType\": 1, \"requestData\": [{\"name\": \"ranyong\"}], \"requestHeaders\": [{\"key\": \"Authorization\", \"value\": \"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImE1YzQ5MDhhLTNjMTgtNDE1Ni1hNTkwLWFkMGIyZDY1NDNhYSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTEyLjk2LjIyNC4xMzgiLCJsb2dpbkxvY2F0aW9uIjoiXHU0ZTlhXHU2ZDMyLVx1NWU3Zlx1NGUxY1x1NzcwMSIsImJyb3dzZXIiOiJDaHJvbWUgMTA5Iiwib3MiOiJNYWMgT1MgWCAxMCIsImxvZ2luVGltZSI6IjIwMjQtMDktMjYgMjA6NTc6MzMifSwiZXhwIjoxNzI3NDQxODUzfQ.UMV9sONUcsMOje0eMmrfwJRlzST29DsQR5XaPinsSiU\", \"remarks\": \"这是一个请求头\"}], \"createBy\": \"admin\", \"createTime\": \"2024-10-08T21:30:43\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-08T21:30:43\", \"remark\": \"string\"}', '{\"code\": 200, \"msg\": \"接口:90 已存在\", \"success\": true, \"time\": \"2024-10-15T10:34:45.806322\"}', 0, '', '2024-10-15 10:34:46', 0);
INSERT INTO `sys_oper_log` VALUES (936, '接口', 3, 'module_admin.controller.api_controller.delete_api()', 'DELETE', 0, 'admin', '研发部门', '/dev-api/apitest/apiInfo/90', '', '内网IP', '', '{\"code\": 200, \"msg\": \"删除成功\", \"success\": true, \"time\": \"2024-10-15T10:35:25.609760\"}', 0, '', '2024-10-15 10:35:26', 0);
INSERT INTO `sys_oper_log` VALUES (937, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 0, \"menuName\": \"API测试\", \"icon\": \"clipboard\", \"menuType\": \"M\", \"orderNum\": 3, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"path\": \"/\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-10-15T11:38:41.888606\"}', 0, '', '2024-10-15 11:38:42', 0);
INSERT INTO `sys_oper_log` VALUES (938, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2023, \"menuName\": \"API测试\", \"parentId\": 0, \"orderNum\": 2, \"path\": \"/\", \"component\": null, \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"M\", \"visible\": \"0\", \"status\": \"0\", \"perms\": null, \"icon\": \"clipboard\", \"createBy\": \"admin\", \"createTime\": \"2024-10-15T11:38:42\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T11:38:42\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T11:38:54.043538\"}', 0, '', '2024-10-15 11:38:54', 0);
INSERT INTO `sys_oper_log` VALUES (939, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2023, \"menuName\": \"API测试\", \"parentId\": 0, \"orderNum\": 1, \"path\": \"/\", \"component\": null, \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"M\", \"visible\": \"0\", \"status\": \"0\", \"perms\": null, \"icon\": \"clipboard\", \"createBy\": \"admin\", \"createTime\": \"2024-10-15T11:38:42\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T11:38:54\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T11:39:16.395052\"}', 0, '', '2024-10-15 11:39:16', 0);
INSERT INTO `sys_oper_log` VALUES (940, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 1, \"menuName\": \"系统管理\", \"parentId\": 0, \"orderNum\": 2, \"path\": \"system\", \"component\": null, \"query\": \"\", \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"M\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"\", \"icon\": \"system\", \"createBy\": \"admin\", \"createTime\": \"2024-08-13T18:18:19\", \"updateBy\": \"\", \"updateTime\": null, \"remark\": \"系统管理目录\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T11:39:33.352719\"}', 0, '', '2024-10-15 11:39:33', 0);
INSERT INTO `sys_oper_log` VALUES (941, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2, \"menuName\": \"系统监控\", \"parentId\": 0, \"orderNum\": 3, \"path\": \"monitor\", \"component\": null, \"query\": \"\", \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"M\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"\", \"icon\": \"monitor\", \"createBy\": \"admin\", \"createTime\": \"2024-08-13T18:18:19\", \"updateBy\": \"\", \"updateTime\": null, \"remark\": \"系统监控目录\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T11:39:47.127945\"}', 0, '', '2024-10-15 11:39:47', 0);
INSERT INTO `sys_oper_log` VALUES (942, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2007, \"menuName\": \"通用配置\", \"parentId\": 0, \"orderNum\": 4, \"path\": \"commonConfig\", \"component\": null, \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"M\", \"visible\": \"0\", \"status\": \"0\", \"perms\": null, \"icon\": \"slider\", \"createBy\": \"admin\", \"createTime\": \"2024-09-16T10:31:57\", \"updateBy\": \"admin\", \"updateTime\": \"2024-09-16T10:33:37\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T11:39:50.230565\"}', 0, '', '2024-10-15 11:39:50', 0);
INSERT INTO `sys_oper_log` VALUES (943, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2007, \"menuName\": \"通用配置\", \"parentId\": 0, \"orderNum\": 5, \"path\": \"commonConfig\", \"component\": null, \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"M\", \"visible\": \"0\", \"status\": \"0\", \"perms\": null, \"icon\": \"slider\", \"createBy\": \"admin\", \"createTime\": \"2024-09-16T10:31:57\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T11:39:50\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T11:39:52.922413\"}', 0, '', '2024-10-15 11:39:53', 0);
INSERT INTO `sys_oper_log` VALUES (944, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2023, \"menuName\": \"API测试\", \"parentId\": 0, \"orderNum\": 1, \"path\": \"apiTest\", \"component\": null, \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"M\", \"visible\": \"0\", \"status\": \"0\", \"perms\": null, \"icon\": \"clipboard\", \"createBy\": \"admin\", \"createTime\": \"2024-10-15T11:38:42\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T11:39:16\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T11:40:07.158686\"}', 0, '', '2024-10-15 11:40:07', 0);
INSERT INTO `sys_oper_log` VALUES (945, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2023, \"menuName\": \"接口管理\", \"icon\": \"checkbox\", \"menuType\": \"C\", \"orderNum\": 1, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"path\": \"apiInfo\", \"component\": \"apiInfo/index\", \"perms\": \"apitest:apiInfo:list\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-10-15T11:42:18.184057\"}', 0, '', '2024-10-15 11:42:18', 0);
INSERT INTO `sys_oper_log` VALUES (946, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2024, \"menuName\": \"接口查询\", \"menuType\": \"F\", \"orderNum\": 0, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-10-15T11:42:50.408727\"}', 0, '', '2024-10-15 11:42:50', 0);
INSERT INTO `sys_oper_log` VALUES (947, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2025, \"menuName\": \"接口查询\", \"parentId\": 2024, \"orderNum\": 0, \"path\": \"\", \"component\": null, \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"F\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"apitest:apiInfo:query\", \"icon\": \"#\", \"createBy\": \"admin\", \"createTime\": \"2024-10-15T11:42:50\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T11:42:50\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T11:43:16.783894\"}', 0, '', '2024-10-15 11:43:17', 0);
INSERT INTO `sys_oper_log` VALUES (948, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2024, \"menuName\": \"接口新增\", \"menuType\": \"F\", \"orderNum\": 1, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"apitest:apiInfo:add\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-10-15T11:43:38.068892\"}', 0, '', '2024-10-15 11:43:38', 0);
INSERT INTO `sys_oper_log` VALUES (949, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2024, \"menuName\": \"接口编辑\", \"menuType\": \"F\", \"orderNum\": 2, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"apitest:apiInfo:edit\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-10-15T11:43:54.689796\"}', 0, '', '2024-10-15 11:43:55', 0);
INSERT INTO `sys_oper_log` VALUES (950, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2024, \"menuName\": \"接口删除\", \"menuType\": \"F\", \"orderNum\": 3, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"apitest:apiInfo:remove\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-10-15T11:44:11.947118\"}', 0, '', '2024-10-15 11:44:12', 1);
INSERT INTO `sys_oper_log` VALUES (951, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2024, \"menuName\": \"接口测试\", \"menuType\": \"F\", \"orderNum\": 4, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"apitest:apiInfo:debug\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-10-15T11:44:28.930209\"}', 0, '', '2024-10-15 11:44:29', 3);
INSERT INTO `sys_oper_log` VALUES (952, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2024, \"menuName\": \"接口管理\", \"parentId\": 2023, \"orderNum\": 1, \"path\": \"apiInfo\", \"component\": \"apimanage/index\", \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"C\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"apitest:apiInfo:list\", \"icon\": \"checkbox\", \"createBy\": \"admin\", \"createTime\": \"2024-10-15T11:42:18\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T11:42:18\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T13:48:06.443719\"}', 0, '', '2024-10-15 13:48:06', 0);
INSERT INTO `sys_oper_log` VALUES (953, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2024, \"menuName\": \"接口管理\", \"parentId\": 2023, \"orderNum\": 1, \"path\": \"apiInfo\", \"component\": \"apiInfo/index\", \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"C\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"apitest:apiInfo:list\", \"icon\": \"checkbox\", \"createBy\": \"admin\", \"createTime\": \"2024-10-15T11:42:18\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T13:48:06\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T13:49:04.601682\"}', 0, '', '2024-10-15 13:49:05', 0);
INSERT INTO `sys_oper_log` VALUES (954, '接口', 3, 'module_admin.controller.api_controller.delete_api()', 'DELETE', 1, 'admin', '研发部门', '/apitest/apiInfo/96', '', '内网IP', '{\"api_ids\": \"96\"}', '{\"code\": 200, \"msg\": \"删除成功\", \"success\": true, \"time\": \"2024-10-15T14:42:11.283839\"}', 0, '', '2024-10-15 14:42:11', 0);
INSERT INTO `sys_oper_log` VALUES (955, '数据源', 2, 'module_admin.controller.datasource_controller.edit_datasource()', 'PUT', 1, 'admin', '研发部门', '/commonConfig/dataSource', '', '内网IP', '{\"datasourceId\": 1, \"datasourceName\": \"本地数据库\", \"datasourceType\": \"mysql\", \"datasourceHost\": \"192.168.1.243\", \"datasourcePort\": \"3306\", \"datasourceUser\": \"root\", \"datasourcePwd\": \"Ranyong_520\", \"createBy\": \"admin\", \"createTime\": \"2024-09-21T15:53:47\", \"updateBy\": \"admin\", \"updateTime\": \"2024-09-22T10:54:55\", \"remark\": \"本地数据库测试连接\"}', '{\"code\": 200, \"msg\": \"数据源:本地数据库 更新成功\", \"success\": true, \"time\": \"2024-10-15T15:50:05.651523\"}', 0, '', '2024-10-15 15:50:06', 0);
INSERT INTO `sys_oper_log` VALUES (956, '数据源', 2, 'module_admin.controller.datasource_controller.edit_datasource()', 'PUT', 1, 'admin', '研发部门', '/commonConfig/dataSource', '', '内网IP', '{\"datasourceId\": 1, \"datasourceName\": \"本地数据库\", \"datasourceType\": \"mysql\", \"datasourceHost\": \"192.168.1.243\", \"datasourcePort\": \"3306\", \"datasourceUser\": \"root\", \"datasourcePwd\": \"123456\", \"createBy\": \"admin\", \"createTime\": \"2024-09-21T15:53:47\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T15:50:06\", \"remark\": \"本地数据库测试连接\"}', '{\"code\": 200, \"msg\": \"数据源:本地数据库 更新成功\", \"success\": true, \"time\": \"2024-10-15T15:50:21.082532\"}', 0, '', '2024-10-15 15:50:21', 0);
INSERT INTO `sys_oper_log` VALUES (957, '数据源', 2, 'module_admin.controller.datasource_controller.edit_datasource()', 'PUT', 1, 'admin', '研发部门', '/commonConfig/dataSource', '', '内网IP', '{\"datasourceId\": 1, \"datasourceName\": \"本地数据库\", \"datasourceType\": \"mysql\", \"datasourceHost\": \"192.168.1.243\", \"datasourcePort\": \"3306\", \"datasourceUser\": \"root\", \"datasourcePwd\": \"123456\", \"createBy\": \"admin\", \"createTime\": \"2024-09-21T15:53:47\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T15:50:21\", \"remark\": \"本地数据库测试连接\"}', '{\"code\": 200, \"msg\": \"数据源:本地数据库 更新成功\", \"success\": true, \"time\": \"2024-10-15T15:51:13.398916\"}', 0, '', '2024-10-15 15:51:13', 0);
INSERT INTO `sys_oper_log` VALUES (958, '数据源', 2, 'module_admin.controller.datasource_controller.edit_datasource()', 'PUT', 1, 'admin', '研发部门', '/commonConfig/dataSource', '', '内网IP', '{\"datasourceId\": 1, \"datasourceName\": \"本地数据库\", \"datasourceType\": \"mysql\", \"datasourceHost\": \"192.168.1.243\", \"datasourcePort\": \"3306\", \"datasourceUser\": \"root\", \"createBy\": \"admin\", \"createTime\": \"2024-09-21T15:53:47\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T15:51:13\", \"remark\": \"本地数据库测试连接\"}', '{\"code\": 200, \"msg\": \"数据源:本地数据库 更新成功\", \"success\": true, \"time\": \"2024-10-15T15:51:24.642942\"}', 0, '', '2024-10-15 15:51:25', 0);
INSERT INTO `sys_oper_log` VALUES (959, '数据源', 2, 'module_admin.controller.datasource_controller.edit_datasource()', 'PUT', 1, 'admin', '研发部门', '/commonConfig/dataSource', '', '内网IP', '{\"datasourceId\": 6, \"datasourceName\": \"测试加密\", \"datasourceType\": \"mysql\", \"datasourceHost\": \"127.0.0.1\", \"datasourcePort\": \"3306\", \"datasourceUser\": \"root\", \"datasourcePwd\": \"123\", \"createBy\": \"admin\", \"createTime\": \"2024-09-22T01:04:36\", \"updateBy\": \"admin\", \"updateTime\": \"2024-09-22T10:55:09\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"数据源:测试加密 更新成功\", \"success\": true, \"time\": \"2024-10-15T16:03:15.377698\"}', 0, '', '2024-10-15 16:03:15', 0);
INSERT INTO `sys_oper_log` VALUES (960, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2021, \"menuName\": \" 数据查询\", \"parentId\": 3, \"orderNum\": 4, \"path\": \"querydb\", \"component\": \"tool/querydb/index\", \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 1, \"menuType\": \"C\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"commonConfig:dataSource:databaseTable\", \"icon\": \"404\", \"createBy\": \"admin\", \"createTime\": \"2024-09-22T17:17:34\", \"updateBy\": \"admin\", \"updateTime\": \"2024-09-22T17:19:21\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T17:16:47.623140\"}', 0, '', '2024-10-15 17:16:48', 3);
INSERT INTO `sys_oper_log` VALUES (961, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2021, \"menuName\": \" 数据查询\", \"parentId\": 3, \"orderNum\": 4, \"path\": \"querydb\", \"component\": \"tool/querydb/index\", \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"C\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"\", \"icon\": \"404\", \"createBy\": \"admin\", \"createTime\": \"2024-09-22T17:17:34\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T17:16:48\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T17:18:21.870636\"}', 0, '', '2024-10-15 17:18:22', 0);
INSERT INTO `sys_oper_log` VALUES (962, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2022, \"menuName\": \"执行SQL\", \"parentId\": 2021, \"orderNum\": 1, \"path\": \"\", \"component\": null, \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"F\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"\", \"icon\": \"#\", \"createBy\": \"admin\", \"createTime\": \"2024-09-22T17:19:53\", \"updateBy\": \"admin\", \"updateTime\": \"2024-09-22T17:19:53\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T17:18:25.464423\"}', 0, '', '2024-10-15 17:18:25', 0);
INSERT INTO `sys_oper_log` VALUES (963, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2021, \"menuName\": \" 数据查询\", \"parentId\": 3, \"orderNum\": 4, \"path\": \"querydb\", \"component\": \"tool/querydb/index\", \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"C\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"commonConfig:dataSource:list\", \"icon\": \"404\", \"createBy\": \"admin\", \"createTime\": \"2024-09-22T17:17:34\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T17:18:22\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T17:20:00.223149\"}', 0, '', '2024-10-15 17:20:00', 0);
INSERT INTO `sys_oper_log` VALUES (964, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2022, \"menuName\": \"执行SQL\", \"parentId\": 2021, \"orderNum\": 1, \"path\": \"\", \"component\": null, \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"F\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"commonConfig:dataSource:execute\", \"icon\": \"#\", \"createBy\": \"admin\", \"createTime\": \"2024-09-22T17:19:53\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T17:18:25\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T17:20:53.023314\"}', 0, '', '2024-10-15 17:20:53', 0);
INSERT INTO `sys_oper_log` VALUES (965, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2022, \"menuName\": \"执行SQL\", \"parentId\": 2021, \"orderNum\": 0, \"path\": \"\", \"component\": null, \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"F\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"commonConfig:dataSource:execute\", \"icon\": \"#\", \"createBy\": \"admin\", \"createTime\": \"2024-09-22T17:19:53\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-15T17:20:53\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-10-15T17:20:58.922693\"}', 0, '', '2024-10-15 17:20:59', 0);
INSERT INTO `sys_oper_log` VALUES (966, '数据源', 1, 'module_admin/controller/datasource_controller.add_datasource()', 'POST', 1, 'admin', '研发部门', '/commonConfig/dataSource', '', '内网IP', '{\"datasourceName\": \"Docker 数据库\", \"datasourceHost\": \"beidoulab.club\", \"datasourcePort\": \"62387\", \"datasourcePwd\": \"Ranyong_520\", \"datasourceType\": \"mysql\", \"datasourceUser\": \"root\"}', '{\"code\": 200, \"msg\": \"新增数据源成功\", \"success\": true, \"time\": \"2024-10-19T15:19:12.213407\"}', 0, '', '2024-10-19 15:19:12', 1);
INSERT INTO `sys_oper_log` VALUES (967, '项目管理', 1, 'module_admin/controller/project_controller.add_project()', 'POST', 1, 'admin', '研发部门', '/auto/project', '', '内网IP', '{\"projectName\": \"ddddd\", \"responsibleName\": \"dddd\", \"testUser\": \"dddd\", \"devUser\": \"ddd\", \"publishApp\": \"dddd\", \"simpleDesc\": \"ddd\", \"remark\": \"ddd\"}', '{\"code\": 200, \"msg\": \"新增项目成功\", \"success\": true, \"time\": \"2024-10-22T23:24:17.799524\"}', 0, '', '2024-10-22 23:24:18', 1);
INSERT INTO `sys_oper_log` VALUES (968, '项目管理', 2, 'module_admin/controller/project_controller.edit_project()', 'PUT', 1, 'admin', '研发部门', '/auto/project', '', '内网IP', '{\"projectId\": 18, \"projectName\": \"ddddd\", \"responsibleName\": \"dddd\", \"testUser\": \"dddd\", \"devUser\": \"dddqweqwe\", \"publishApp\": \"dddd\", \"simpleDesc\": \"ddd\", \"createBy\": \"admin\", \"createTime\": \"2024-10-22T23:24:18\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-22T23:24:18\", \"remark\": \"ddd\"}', '{\"code\": 200, \"msg\": \"项目:ddddd 更新成功\", \"success\": true, \"time\": \"2024-10-22T23:24:22.356581\"}', 0, '', '2024-10-22 23:24:22', 1);
INSERT INTO `sys_oper_log` VALUES (969, '项目管理', 2, 'module_admin/controller/project_controller.edit_project()', 'PUT', 1, 'admin', '研发部门', '/auto/project', '', '内网IP', '{\"projectId\": 18, \"projectName\": \"ddddd\", \"responsibleName\": \"dddd\", \"testUser\": \"dddd\", \"devUser\": \"dddqweqwe\", \"publishApp\": \"dddd\", \"simpleDesc\": \"\", \"createBy\": \"admin\", \"createTime\": \"2024-10-22T23:24:18\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-22T23:24:22\", \"remark\": \"ddd\"}', '{\"code\": 200, \"msg\": \"项目:ddddd 更新成功\", \"success\": true, \"time\": \"2024-10-22T23:24:27.653489\"}', 0, '', '2024-10-22 23:24:28', 0);
INSERT INTO `sys_oper_log` VALUES (970, '项目管理', 3, 'module_admin/controller/project_controller.delete_project()', 'DELETE', 1, 'admin', '研发部门', '/auto/project/18', '', '内网IP', '{\"project_ids\": \"18\"}', '{\"code\": 200, \"msg\": \"删除成功\", \"success\": true, \"time\": \"2024-10-22T23:24:30.440979\"}', 0, '', '2024-10-22 23:24:30', 0);
INSERT INTO `sys_oper_log` VALUES (971, '接口', 1, 'module_admin/controller/api_controller.add_api()', 'POST', 1, 'admin', '研发部门', '/apitest/apiInfo', '', '内网IP', '{\"apiMethod\": \"POST\", \"apiName\": \"登录 123\", \"apiUrl\": \"/login1123\", \"projectId\": 2, \"apiTags\": [\"login\"], \"apiLevel\": \"P0\", \"remark\": \"这是一个登录接口\", \"project_module\": [2]}', '{\"code\": 200, \"msg\": \"新增接口成功\", \"success\": true, \"time\": \"2024-10-22T23:25:09.012929\"}', 0, '', '2024-10-22 23:25:09', 1);
INSERT INTO `sys_oper_log` VALUES (972, '用户管理', 5, 'module_admin/controller/user_controller.export_system_user_list()', 'POST', 1, 'admin', '研发部门', '/system/user/export', '', '内网IP', 'pageNum: 1\npageSize: 10', '{\"code\": 200, \"message\": \"获取成功\"}', 0, '', '2024-10-23 00:28:20', 3);
INSERT INTO `sys_oper_log` VALUES (973, '定时任务', 5, 'module_admin/controller/job_controller.export_system_job_list()', 'POST', 1, 'admin', '研发部门', '/monitor/job/export', '', '内网IP', 'pageNum: 1\npageSize: 10', '{\"code\": 200, \"message\": \"获取成功\"}', 0, '', '2024-10-23 00:29:05', 2);
INSERT INTO `sys_oper_log` VALUES (974, '接口', 3, 'module_admin/controller/api_controller.delete_api()', 'DELETE', 1, 'admin', '研发部门', '/apitest/apiInfo/2,1', '', '内网IP', '{\"api_ids\": \"2,1\"}', '{\"code\": 200, \"msg\": \"删除成功\", \"success\": true, \"time\": \"2024-10-24T22:05:55.684839\"}', 0, '', '2024-10-24 22:05:56', 1);
INSERT INTO `sys_oper_log` VALUES (975, '接口', 1, 'module_admin/controller/api_controller.add_api()', 'POST', 1, 'admin', '研发部门', '/apitest/apiInfo', '', '内网IP', '{\"apiMethod\": \"POST\", \"apiName\": \"查询倾角图表\", \"apiUrl\": \"/api/admin/packetInfo/getDevicePacketChart\", \"projectId\": 3, \"apiTags\": [], \"apiLevel\": \"P0\", \"remark\": \"\", \"project_module\": [3]}', '{\"code\": 200, \"msg\": \"新增接口成功\", \"success\": true, \"time\": \"2024-10-24T22:06:51.910448\"}', 0, '', '2024-10-24 22:06:52', 0);
INSERT INTO `sys_oper_log` VALUES (976, '接口', 1, 'module_admin/controller/api_controller.add_api()', 'POST', 1, 'admin', '研发部门', '/apitest/apiInfo', '', '内网IP', '{\"apiMethod\": \"POST\", \"apiName\": \"查询倾角图表\", \"apiUrl\": \"/api/admin/packetInfo/getDevicePacketChart\", \"projectId\": 3, \"apiTags\": [], \"apiLevel\": \"P0\", \"remark\": \"\", \"project_module\": [3]}', '{\"code\": 200, \"msg\": \"接口:查询倾角图表 已存在\", \"success\": true, \"time\": \"2024-10-24T22:07:07.649072\"}', 0, '', '2024-10-24 22:07:08', 0);
INSERT INTO `sys_oper_log` VALUES (977, '接口', 1, 'module_admin/controller/api_controller.add_api()', 'POST', 1, 'admin', '研发部门', '/dev-api/apitest/apiInfo', '', '内网IP', '{\"apiId\": 2, \"apiName\": \"string\", \"projectId\": 0, \"apiMethod\": \"GET\", \"apiUrl\": \"string\", \"apiStatus\": \"0\", \"apiLevel\": \"P0\", \"apiTags\": [], \"requestDataType\": 0, \"requestData\": {}, \"requestHeaders\": {}, \"createBy\": \"string\", \"createTime\": \"2024-10-24T15:32:29.081Z\", \"updateBy\": \"string\", \"updateTime\": \"2024-10-24T15:32:29.081Z\", \"remark\": \"string\"}', '{\"code\": 500, \"msg\": \"(asyncmy.errors.IntegrityError) (1062, \\\"Duplicate entry \'2\' for key \'api_info.PRIMARY\'\\\")\\n[SQL: INSERT INTO api_info (api_id, api_name, project_id, api_method, api_url, api_status, api_level, api_tags, request_data_type, request_data, request_headers, create_by, create_time, update_by, update_time, remark) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)]\\n[parameters: (2, \'string\', 0, \'GET\', \'string\', \'0\', \'P0\', \'[]\', 0, \'{}\', \'{}\', \'admin\', datetime.datetime(2024, 10, 24, 23, 32, 48, 399917), \'admin\', datetime.datetime(2024, 10, 24, 23, 32, 48, 399933), \'string\')]\\n(Background on this error at: https://sqlalche.me/e/20/gkpj)\", \"success\": false, \"time\": \"2024-10-24T23:32:48.410515\"}', 1, '(asyncmy.errors.IntegrityError) (1062, \"Duplicate entry \'2\' for key \'api_info.PRIMARY\'\")\n[SQL: INSERT INTO api_info (api_id, api_name, project_id, api_method, api_url, api_status, api_level, api_tags, request_data_type, request_data, request_headers, create_by, create_time, update_by, update_time, remark) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)]\n[parameters: (2, \'string\', 0, \'GET\', \'string\', \'0\', \'P0\', \'[]\', 0, \'{}\', \'{}\', \'admin\', datetime.datetime(2024, 10, 24, 23, 32, 48, 399917), \'admin\', datetime.datetime(2024, 10, 24, 23, 32, 48, 399933), \'string\')]\n(Background on this error at: https://sqlalche.me/e/20/gkpj)', '2024-10-24 23:32:48', 1);
INSERT INTO `sys_oper_log` VALUES (978, '接口', 1, 'module_admin/controller/api_controller.add_api()', 'POST', 1, 'admin', '研发部门', '/dev-api/apitest/apiInfo', '', '内网IP', '{\"apiId\": 3, \"apiName\": \"string\", \"projectId\": 0, \"apiMethod\": \"GET\", \"apiUrl\": \"string\", \"apiStatus\": \"0\", \"apiLevel\": \"P0\", \"apiTags\": [], \"requestDataType\": 0, \"requestData\": {}, \"requestHeaders\": {}, \"createBy\": \"string\", \"createTime\": \"2024-10-24T15:32:29.081Z\", \"updateBy\": \"string\", \"updateTime\": \"2024-10-24T15:32:29.081Z\", \"remark\": \"string\"}', '{\"code\": 200, \"msg\": \"新增接口成功\", \"success\": true, \"time\": \"2024-10-24T23:33:18.296107\"}', 0, '', '2024-10-24 23:33:18', 0);
INSERT INTO `sys_oper_log` VALUES (979, '接口', 1, 'module_admin/controller/api_controller.add_api()', 'POST', 1, 'admin', '研发部门', '/apitest/apiInfo', '', '内网IP', '{\"apiMethod\": \"POST\", \"apiName\": \"登录接口\", \"apiUrl\": \"/login\", \"projectId\": 17, \"apiTags\": [], \"apiLevel\": \"P0\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"新增接口成功\", \"success\": true, \"time\": \"2024-10-26T16:33:36.312405\"}', 0, '', '2024-10-26 16:33:36', 1);
INSERT INTO `sys_oper_log` VALUES (980, '接口', 2, 'module_admin/controller/api_controller.edit_api()', 'PUT', 1, 'admin', '研发部门', '/apitest/apiInfo', '', '内网IP', '{\"apiMethod\": \"POST\", \"apiName\": \"登录接口\", \"apiUrl\": \"/login\", \"projectId\": 17, \"apiTags\": [\"登录\"], \"apiLevel\": \"P0\", \"remark\": \"\", \"apiId\": 99, \"apiStatus\": \"0\", \"requestDataType\": 0, \"requestData\": {}, \"requestHeaders\": {}, \"createBy\": \"admin\", \"createTime\": \"2024-10-26T16:33:36\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-26T16:33:36\"}', '{\"code\": 200, \"msg\": \"接口:登录接口 更新成功\", \"success\": true, \"time\": \"2024-10-26T16:33:47.771209\"}', 0, '', '2024-10-26 16:33:48', 1);
INSERT INTO `sys_oper_log` VALUES (981, '接口', 2, 'module_admin/controller/api_controller.edit_api()', 'PUT', 1, 'admin', '研发部门', '/apitest/apiInfo', '', '内网IP', '{\"apiMethod\": \"POST\", \"apiName\": \"登录接口\", \"apiUrl\": \"/login\", \"projectId\": 17, \"apiTags\": [\"登录\"], \"apiLevel\": \"P0\", \"remark\": \"这是一个编辑功能\", \"apiId\": 99, \"apiStatus\": \"0\", \"requestDataType\": 0, \"requestData\": {}, \"requestHeaders\": {}, \"createBy\": \"admin\", \"createTime\": \"2024-10-26T16:33:36\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-26T16:33:48\"}', '{\"code\": 200, \"msg\": \"接口:登录接口 更新成功\", \"success\": true, \"time\": \"2024-10-26T16:37:07.224290\"}', 0, '', '2024-10-26 16:37:07', 1);
INSERT INTO `sys_oper_log` VALUES (982, '接口', 2, 'module_admin/controller/api_controller.edit_api()', 'PUT', 1, 'admin', '研发部门', '/apitest/apiInfo', '', '内网IP', '{\"apiMethod\": \"GET\", \"apiName\": \"登录接口\", \"apiUrl\": \"/login\", \"projectId\": 17, \"apiTags\": [\"登录\"], \"apiLevel\": \"P0\", \"remark\": \"这是一个编辑功能\", \"apiId\": 99, \"apiStatus\": \"0\", \"requestDataType\": 0, \"requestData\": {}, \"requestHeaders\": {}, \"createBy\": \"admin\", \"createTime\": \"2024-10-26T16:33:36\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-26T16:37:07\"}', '{\"code\": 200, \"msg\": \"接口:登录接口 更新成功\", \"success\": true, \"time\": \"2024-10-26T16:37:19.236269\"}', 0, '', '2024-10-26 16:37:19', 1);
INSERT INTO `sys_oper_log` VALUES (983, '接口', 2, 'module_admin/controller/api_controller.edit_api()', 'PUT', 1, 'admin', '研发部门', '/apitest/apiInfo', '', '内网IP', '{\"apiMethod\": \"DELETE\", \"apiName\": \"登录接口\", \"apiUrl\": \"/login\", \"projectId\": 17, \"apiTags\": [\"登录\"], \"apiLevel\": \"P0\", \"remark\": \"这是一个编辑功能\", \"apiId\": 99, \"apiStatus\": \"0\", \"requestDataType\": 0, \"requestData\": {}, \"requestHeaders\": {}, \"createBy\": \"admin\", \"createTime\": \"2024-10-26T16:33:36\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-26T16:37:19\"}', '{\"code\": 200, \"msg\": \"接口:登录接口 更新成功\", \"success\": true, \"time\": \"2024-10-26T16:37:24.265818\"}', 0, '', '2024-10-26 16:37:24', 0);
INSERT INTO `sys_oper_log` VALUES (984, '接口', 1, 'module_admin/controller/api_controller.add_api()', 'POST', 1, 'admin', '研发部门', '/apitest/apiInfo', '', '内网IP', '{\"apiMethod\": \"POST\", \"apiName\": \"restart\", \"apiUrl\": \"/restart\", \"projectId\": 17, \"apiTags\": [], \"apiLevel\": \"P0\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"新增接口成功\", \"success\": true, \"time\": \"2024-10-26T16:47:42.744485\"}', 0, '', '2024-10-26 16:47:43', 1);
INSERT INTO `sys_oper_log` VALUES (985, '接口', 1, 'module_admin/controller/api_controller.add_api()', 'POST', 1, 'admin', '研发部门', '/apitest/apiInfo', '', '内网IP', '{\"apiMethod\": \"POST\", \"apiName\": \"111\", \"apiUrl\": \"111\", \"projectId\": 17, \"apiTags\": [], \"apiLevel\": \"P0\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"新增接口成功\", \"success\": true, \"time\": \"2024-10-26T16:47:59.224765\"}', 0, '', '2024-10-26 16:47:59', 0);
INSERT INTO `sys_oper_log` VALUES (986, '环境', 1, 'module_admin/controller/env_controller.add_env()', 'POST', 0, 'admin', '研发部门', '/env/envInfo', '', '内网IP', '{\"envId\": 1, \"envName\": \"测试环境\", \"envUrl\": \"https://beidoulab.club:5557/\", \"envVariables\": {}, \"envHeaders\": {}, \"createBy\": \"\", \"createTime\": \"2024-10-30T14:48:57.967Z\", \"updateBy\": \"\", \"updateTime\": \"2024-10-30T14:48:57.967Z\", \"remark\": \"\"}', '{\"code\": 500, \"msg\": \"name \'api\' is not defined\", \"success\": false, \"time\": \"2024-10-30T22:53:01.389595\"}', 1, 'name \'api\' is not defined', '2024-10-30 22:53:01', 0);
INSERT INTO `sys_oper_log` VALUES (987, '环境', 1, 'module_admin/controller/env_controller.add_env()', 'POST', 1, 'admin', '研发部门', '/dev-api/env/envInfo', '', '内网IP', '{\"envId\": 1, \"envName\": \"测试环境\", \"envUrl\": \"https://beidoulab.club:5557/\", \"envVariables\": {}, \"envHeaders\": {}, \"createBy\": \"\", \"createTime\": \"2024-10-30T14:48:57.967Z\", \"updateBy\": \"\", \"updateTime\": \"2024-10-30T14:48:57.967Z\", \"remark\": \"\"}', '{\"code\": 500, \"msg\": \"name \'api\' is not defined\", \"success\": false, \"time\": \"2024-10-30T22:53:31.134824\"}', 1, 'name \'api\' is not defined', '2024-10-30 22:53:31', 0);
INSERT INTO `sys_oper_log` VALUES (988, '环境', 1, 'module_admin/controller/env_controller.add_env()', 'POST', 0, 'admin', '研发部门', '/env/envInfo', '', '内网IP', '{\"envId\": 1, \"envName\": \"测试环境\", \"envUrl\": \"https://beidoulab.club:5557/\", \"envVariables\": {}, \"envHeaders\": {}, \"createBy\": \"\", \"createTime\": \"2024-10-30T14:48:57.967Z\", \"updateBy\": \"\", \"updateTime\": \"2024-10-30T14:48:57.967Z\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"新增环境成功\", \"success\": true, \"time\": \"2024-10-30T22:54:51.153456\"}', 0, '', '2024-10-30 22:54:51', 1);
INSERT INTO `sys_oper_log` VALUES (989, '环境', 1, 'module_admin/controller/env_controller.add_env()', 'POST', 0, 'admin', '研发部门', '/env/envInfo', '', '内网IP', '{\"envId\": 2, \"envName\": \"正式环境\", \"envUrl\": \"https://convercomm.com/\", \"envVariables\": {}, \"envHeaders\": {}, \"createBy\": \"\", \"createTime\": \"2024-10-30T14:48:57.967Z\", \"updateBy\": \"\", \"updateTime\": \"2024-10-30T14:48:57.967Z\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"新增环境成功\", \"success\": true, \"time\": \"2024-10-30T22:56:37.710271\"}', 0, '', '2024-10-30 22:56:38', 0);
INSERT INTO `sys_oper_log` VALUES (990, '环境', 1, 'module_admin/controller/env_controller.add_env()', 'POST', 0, 'admin', '研发部门', '/env/envInfo', '', '内网IP', '{\"envId\": 19, \"envName\": \"测试环境\", \"envUrl\": \"https://beidoulab.club:5557/\", \"envVariables\": {}, \"envHeaders\": {}, \"createBy\": \"\", \"createTime\": \"2024-10-30T14:48:57.967Z\", \"updateBy\": \"\", \"updateTime\": \"2024-10-30T14:48:57.967Z\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"环境:测试环境 已存在\", \"success\": true, \"time\": \"2024-10-30T22:59:36.966531\"}', 0, '', '2024-10-30 22:59:37', 0);
INSERT INTO `sys_oper_log` VALUES (991, '环境', 1, 'module_admin/controller/env_controller.add_env()', 'POST', 0, 'admin', '研发部门', '/env/envInfo', '', '内网IP', '{\"envId\": 98, \"envName\": \"况\", \"envUrl\": \"https://beidoulab.club:5557/\", \"envVariables\": {}, \"envHeaders\": {}, \"createBy\": \"\", \"createTime\": \"2024-10-30T14:48:57.967Z\", \"updateBy\": \"\", \"updateTime\": \"2024-10-30T14:48:57.967Z\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"新增环境成功\", \"success\": true, \"time\": \"2024-10-30T23:00:16.555645\"}', 0, '', '2024-10-30 23:00:17', 0);
INSERT INTO `sys_oper_log` VALUES (992, '环境', 2, 'module_admin/controller/env_controller.edit_api()', 'PUT', 0, 'admin', '研发部门', '/env/envInfo', '', '内网IP', '{\"envId\": 98, \"envName\": \"string\", \"envUrl\": \"string\", \"envVariables\": {}, \"envHeaders\": {}, \"createBy\": \"string\", \"createTime\": \"2024-10-30T15:04:15.921Z\", \"updateBy\": \"string\", \"updateTime\": \"2024-10-30T15:04:15.921Z\", \"remark\": \"string\"}', '{\"code\": 200, \"msg\": \"接口:况 更新成功\", \"success\": true, \"time\": \"2024-10-30T23:04:24.355410\"}', 0, '', '2024-10-30 23:04:24', 1);
INSERT INTO `sys_oper_log` VALUES (993, '环境', 3, 'module_admin/controller/env_controller.delete_env()', 'DELETE', 0, 'admin', '研发部门', '/env/envInfo/98', '', '内网IP', '{\"env_ids\": \"98\"}', '{\"code\": 200, \"msg\": \"删除成功\", \"success\": true, \"time\": \"2024-10-30T23:04:36.047177\"}', 0, '', '2024-10-30 23:04:36', 1);
INSERT INTO `sys_oper_log` VALUES (994, '菜单管理', 1, 'module_admin/controller/menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2007, \"menuName\": \"环境管理\", \"icon\": \"cascader\", \"menuType\": \"C\", \"orderNum\": 2, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"path\": \"env\", \"component\": \"envinfo/index\", \"perms\": \"env:envInfo:list\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-10-31T22:07:51.083931\"}', 0, '', '2024-10-31 22:07:51', 1);
INSERT INTO `sys_oper_log` VALUES (995, '菜单管理', 1, 'module_admin/controller/menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2030, \"menuName\": \"环境查询\", \"menuType\": \"F\", \"orderNum\": 0, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"env:envInfo:query\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-10-31T22:08:37.938699\"}', 0, '', '2024-10-31 22:08:38', 1);
INSERT INTO `sys_oper_log` VALUES (996, '菜单管理', 1, 'module_admin/controller/menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2030, \"menuName\": \"环境新增\", \"menuType\": \"F\", \"orderNum\": 1, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"env:envInfo:add\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-10-31T22:09:29.096573\"}', 0, '', '2024-10-31 22:09:29', 1);
INSERT INTO `sys_oper_log` VALUES (997, '菜单管理', 1, 'module_admin/controller/menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2030, \"menuName\": \"环境编辑\", \"menuType\": \"F\", \"orderNum\": 2, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"env:envInfo:edit\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-10-31T22:09:45.696711\"}', 0, '', '2024-10-31 22:09:46', 0);
INSERT INTO `sys_oper_log` VALUES (998, '菜单管理', 1, 'module_admin/controller/menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2030, \"menuName\": \"环境删除\", \"menuType\": \"F\", \"orderNum\": 3, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"env:envInfo:remove\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-10-31T22:10:12.095385\"}', 0, '', '2024-10-31 22:10:12', 1);
INSERT INTO `sys_oper_log` VALUES (999, '环境', 1, 'module_admin/controller/env_controller.add_env()', 'POST', 0, 'admin', '研发部门', '/env/envInfo', '', '内网IP', '{\"envId\": 29, \"envName\": \"周\", \"envUrl\": \"https://beidoulab.club:5557/\", \"envVariables\": {}, \"envHeaders\": {}, \"createBy\": \"\", \"createTime\": \"2024-10-30T14:48:57.967Z\", \"updateBy\": \"\", \"updateTime\": \"2024-10-30T14:48:57.967Z\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"新增环境成功\", \"success\": true, \"time\": \"2024-10-31T22:31:39.850559\"}', 0, '', '2024-10-31 22:31:40', 1);
INSERT INTO `sys_oper_log` VALUES (1000, '环境', 3, 'module_admin/controller/env_controller.delete_env()', 'DELETE', 0, 'admin', '研发部门', '/env/envInfo/29', '', '内网IP', '{\"env_ids\": \"29\"}', '{\"code\": 200, \"msg\": \"删除成功\", \"success\": true, \"time\": \"2024-10-31T22:47:35.012798\"}', 0, '', '2024-10-31 22:47:35', 1);
INSERT INTO `sys_oper_log` VALUES (1001, '环境', 1, 'module_admin/controller/env_controller.add_env()', 'POST', 0, 'admin', '研发部门', '/env/envInfo', '', '内网IP', '{\"envId\": 61, \"envName\": \"方\", \"envUrl\": \"https://beidoulab.club:5557/\", \"envVariables\": {}, \"envHeaders\": {}, \"createBy\": \"\", \"createTime\": \"2024-10-30T14:48:57.967Z\", \"updateBy\": \"\", \"updateTime\": \"2024-10-30T14:48:57.967Z\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"新增环境成功\", \"success\": true, \"time\": \"2024-10-31T22:47:49.491048\"}', 0, '', '2024-10-31 22:47:49', 1);
INSERT INTO `sys_oper_log` VALUES (1002, '环境', 1, 'module_admin/controller/env_controller.add_env()', 'POST', 0, 'admin', '研发部门', '/env/envInfo', '', '内网IP', '{\"envId\": 46, \"envName\": \"眼\", \"envUrl\": \"https://beidoulab.club:5557/\", \"envVariables\": {}, \"envHeaders\": {}, \"createBy\": \"\", \"createTime\": \"2024-10-30T14:48:57.967Z\", \"updateBy\": \"\", \"updateTime\": \"2024-10-30T14:48:57.967Z\", \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"新增环境成功\", \"success\": true, \"time\": \"2024-10-31T22:47:50.402306\"}', 0, '', '2024-10-31 22:47:50', 4);
INSERT INTO `sys_oper_log` VALUES (1003, '环境', 1, 'module_admin/controller/env_controller.add_env()', 'POST', 1, 'admin', '研发部门', '/env/envInfo', '', '内网IP', '{\"envName\": \"111\", \"envUrl\": \"111\", \"envId\": null, \"envHeaders\": {}, \"envVariables\": {}, \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"新增环境成功\", \"success\": true, \"time\": \"2024-10-31T23:28:14.600171\"}', 0, '', '2024-10-31 23:28:15', 1);
INSERT INTO `sys_oper_log` VALUES (1004, '环境', 2, 'module_admin/controller/env_controller.edit_api()', 'PUT', 1, 'admin', '研发部门', '/env/envInfo', '', '内网IP', '{\"envName\": \"111\", \"envUrl\": \"111\", \"envId\": 99, \"envHeaders\": {}, \"envVariables\": {}, \"remark\": \"\", \"createBy\": \"admin\", \"createTime\": \"2024-10-31T23:28:15\", \"updateBy\": \"admin\", \"updateTime\": \"2024-10-31T23:28:15\", \"apiMethod\": \"POST\", \"apiName\": \"\", \"apiUrl\": \"\", \"projectId\": null, \"apiTags\": []}', '{\"code\": 200, \"msg\": \"接口:111 更新成功\", \"success\": true, \"time\": \"2024-10-31T23:30:52.635359\"}', 0, '', '2024-10-31 23:30:53', 1);
INSERT INTO `sys_oper_log` VALUES (1005, '环境', 3, 'module_admin/controller/env_controller.delete_env()', 'DELETE', 1, 'admin', '研发部门', '/env/envInfo/99', '', '内网IP', '{\"env_ids\": \"99\"}', '{\"code\": 200, \"msg\": \"删除成功\", \"success\": true, \"time\": \"2024-10-31T23:39:14.714497\"}', 0, '', '2024-10-31 23:39:15', 0);
INSERT INTO `sys_oper_log` VALUES (1006, '环境', 1, 'module_admin/controller/env_controller.add_env()', 'POST', 1, 'admin', '研发部门', '/env/envInfo', '', '内网IP', '{\"envName\": \"好 123\", \"envUrl\": \"https:www.hao123.com\", \"envId\": null, \"envHeaders\": {}, \"envVariables\": {}, \"remark\": \"\"}', '{\"code\": 200, \"msg\": \"新增环境成功\", \"success\": true, \"time\": \"2024-10-31T23:39:40.247456\"}', 0, '', '2024-10-31 23:39:40', 1);
INSERT INTO `sys_oper_log` VALUES (1007, '定时任务', 1, 'module_admin/controller/job_controller.add_system_job()', 'POST', 1, 'admin', '研发部门', '/monitor/job', '', '内网IP', '{\"jobName\": \"系统默认异步（无参）\", \"jobGroup\": \"default\", \"invokeTarget\": \"module_task.scheduler_test.async_job\", \"cronExpression\": \"0/10 * * * * ?\", \"misfirePolicy\": \"1\", \"concurrent\": \"1\", \"status\": \"1\", \"jobExecutor\": \"default\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-11-14T11:18:59.606118\"}', 0, '', '2024-11-14 11:19:00', 1);
INSERT INTO `sys_oper_log` VALUES (1008, '定时任务', 2, 'module_admin/controller/job_controller.edit_system_job()', 'PUT', 1, 'admin', '研发部门', '/monitor/job', '', '内网IP', '{\"jobId\": 100, \"jobName\": \"系统默认异步（无参）\", \"jobGroup\": \"default\", \"jobExecutor\": \"default\", \"invokeTarget\": \"module_task.scheduler_test.async_job\", \"jobArgs\": \"\", \"jobKwargs\": \"\", \"cronExpression\": \"0/10 * * * * ?\", \"misfirePolicy\": \"1\", \"concurrent\": \"1\", \"status\": \"0\", \"createBy\": \"admin\", \"createTime\": \"2024-11-14T11:19:00\", \"updateBy\": \"admin\", \"updateTime\": \"2024-11-14T11:19:00\", \"remark\": null}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-11-14T11:19:09.648424\"}', 0, '', '2024-11-14 11:19:10', 3);
INSERT INTO `sys_oper_log` VALUES (1009, '定时任务', 2, 'module_admin/controller/job_controller.change_system_job_status()', 'PUT', 1, 'admin', '研发部门', '/monitor/job/changeStatus', '', '内网IP', '{\"jobId\": 100, \"status\": \"1\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-11-14T11:19:48.179231\"}', 0, '', '2024-11-14 11:19:48', 1);
INSERT INTO `sys_oper_log` VALUES (1010, '定时任务', 1, 'module_admin/controller/job_controller.add_system_job()', 'POST', 1, 'admin', '研发部门', '/monitor/job', '', '内网IP', '{\"jobName\": \"系统默认异步（有参）\", \"jobGroup\": \"default\", \"invokeTarget\": \"module_task.scheduler_test.async_job\", \"cronExpression\": \"0/15 * * * * ?\", \"misfirePolicy\": \"1\", \"concurrent\": \"1\", \"status\": \"1\", \"jobExecutor\": \"default\", \"jobArgs\": \"test\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-11-14T11:21:02.784352\"}', 0, '', '2024-11-14 11:21:03', 1);
INSERT INTO `sys_oper_log` VALUES (1011, '定时任务', 2, 'module_admin/controller/job_controller.change_system_job_status()', 'PUT', 1, 'admin', '研发部门', '/monitor/job/changeStatus', '', '内网IP', '{\"jobId\": 101, \"status\": \"0\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-11-14T11:21:06.033629\"}', 0, '', '2024-11-14 11:21:06', 2);
INSERT INTO `sys_oper_log` VALUES (1012, '定时任务', 2, 'module_admin/controller/job_controller.change_system_job_status()', 'PUT', 1, 'admin', '研发部门', '/monitor/job/changeStatus', '', '内网IP', '{\"jobId\": 101, \"status\": \"1\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-11-14T11:21:42.990418\"}', 0, '', '2024-11-14 11:21:43', 1);
INSERT INTO `sys_oper_log` VALUES (1013, '定时任务', 1, 'module_admin/controller/job_controller.add_system_job()', 'POST', 1, 'admin', '研发部门', '/monitor/job', '', '内网IP', '{\"jobName\": \"系统默认异步（多参）\", \"jobGroup\": \"default\", \"invokeTarget\": \"module_task.scheduler_test.async_job\", \"cronExpression\": \"0/20 * * * * ?\", \"misfirePolicy\": \"1\", \"concurrent\": \"1\", \"status\": \"1\", \"jobExecutor\": \"default\", \"jobArgs\": \"new\", \"jobKwargs\": \"{\\\"test\\\":111}\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-11-14T11:25:48.018544\"}', 0, '', '2024-11-14 11:25:48', 2);
INSERT INTO `sys_oper_log` VALUES (1014, '定时任务', 2, 'module_admin/controller/job_controller.change_system_job_status()', 'PUT', 1, 'admin', '研发部门', '/monitor/job/changeStatus', '', '内网IP', '{\"jobId\": 102, \"status\": \"0\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-11-14T11:25:51.229321\"}', 0, '', '2024-11-14 11:25:51', 2);
INSERT INTO `sys_oper_log` VALUES (1015, '定时任务', 2, 'module_admin/controller/job_controller.change_system_job_status()', 'PUT', 1, 'admin', '研发部门', '/monitor/job/changeStatus', '', '内网IP', '{\"jobId\": 102, \"status\": \"1\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-11-14T11:26:08.892253\"}', 0, '', '2024-11-14 11:26:09', 1);
INSERT INTO `sys_oper_log` VALUES (1016, '个人信息', 2, 'module_admin/controller/user_controller.change_system_user_profile_avatar()', 'POST', 1, 'admin', '研发部门', '/docker-api/system/user/profile/avatar', '112.96.226.60', '亚洲-广东省', 'avatarfile: UploadFile(filename=\'1.png\', size=28516, headers=Headers({\'content-disposition\': \'form-data; name=\"avatarfile\"; filename=\"1.png\"\', \'content-type\': \'image/png\'}))', '{\"code\": 200, \"msg\": \"更新成功\", \"imgUrl\": \"/profile/avatar/2024/11/18/avatar_20241118130722A292.png\", \"success\": true, \"time\": \"2024-11-18T13:07:22.632409\"}', 0, '', '2024-11-18 13:07:23', 12);
INSERT INTO `sys_oper_log` VALUES (1017, '定时任务调度日志', 9, 'module_admin/controller/job_controller.clear_system_job_log()', 'DELETE', 1, 'admin', '研发部门', '/docker-api/monitor/jobLog/clean', '222.80.91.121', '亚洲-新疆维吾尔自治区', '{}', '{\"code\": 200, \"msg\": \"清除成功\", \"success\": true, \"time\": \"2024-11-22T01:35:09.759801\"}', 0, '', '2024-11-22 01:35:10', 16);
INSERT INTO `sys_oper_log` VALUES (1018, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2024, \"menuName\": \"测试用例\", \"icon\": \"button\", \"menuType\": \"C\", \"orderNum\": 2, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"path\": \"apiCase\", \"component\": \"apiCase/index\", \"perms\": \"\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2024-12-24T15:46:49.697556\"}', 0, '', '2024-12-24 15:46:50', 3);
INSERT INTO `sys_oper_log` VALUES (1019, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2023, \"menuName\": \"测试用例\", \"icon\": \"button\", \"menuType\": \"C\", \"orderNum\": 2, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"path\": \"apiCase\", \"component\": \"apiCase/index\"}', '{\"code\": 500, \"msg\": \"新增菜单测试用例失败，菜单名称已存在\", \"success\": false, \"time\": \"2024-12-24T15:47:49.013922\"}', 1, '新增菜单测试用例失败，菜单名称已存在', '2024-12-24 15:47:49', 0);
INSERT INTO `sys_oper_log` VALUES (1020, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2035, \"menuName\": \"测试用例\", \"parentId\": 2023, \"orderNum\": 2, \"path\": \"apiCase\", \"component\": \"apiCase/index\", \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"C\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"\", \"icon\": \"button\", \"createBy\": \"admin\", \"createTime\": \"2024-12-24T15:46:50\", \"updateBy\": \"admin\", \"updateTime\": \"2024-12-24T15:46:50\", \"remark\": null}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2024-12-24T15:48:07.425003\"}', 0, '', '2024-12-24 15:48:07', 1);
INSERT INTO `sys_oper_log` VALUES (1021, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2035, \"menuName\": \"测试用例\", \"parentId\": 2023, \"orderNum\": 2, \"path\": \"apiCase\", \"component\": \"apiCase/index\", \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"C\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"testcase:testcaseInfo:list\", \"icon\": \"button\", \"createBy\": \"admin\", \"createTime\": \"2024-12-24T15:46:50\", \"updateBy\": \"admin\", \"updateTime\": \"2024-12-24T15:48:07\", \"remark\": null}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2025-01-04T09:34:01.313671\"}', 0, '', '2025-01-04 09:34:01', 1);
INSERT INTO `sys_oper_log` VALUES (1022, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2035, \"menuName\": \"用例查询\", \"menuType\": \"F\", \"orderNum\": 0, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"testcase:testcaseInfo:query\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2025-01-04T09:35:01.697342\"}', 0, '', '2025-01-04 09:35:02', 1);
INSERT INTO `sys_oper_log` VALUES (1023, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2035, \"menuName\": \"testcase:testcaseInfo:add\", \"menuType\": \"F\", \"orderNum\": 1, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"用例新增\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2025-01-04T09:35:28.313795\"}', 0, '', '2025-01-04 09:35:28', 1);
INSERT INTO `sys_oper_log` VALUES (1024, '菜单管理', 3, 'module_admin.controller.menu_controller.delete_system_menu()', 'DELETE', 1, 'admin', '研发部门', '/system/menu/2037', '', '内网IP', '{\"menu_ids\": \"2037\"}', '{\"code\": 200, \"msg\": \"删除成功\", \"success\": true, \"time\": \"2025-01-04T09:35:32.747511\"}', 0, '', '2025-01-04 09:35:33', 0);
INSERT INTO `sys_oper_log` VALUES (1025, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2035, \"menuName\": \"用例新增\", \"menuType\": \"F\", \"orderNum\": 1, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"testcase:testcaseInfo:add\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2025-01-04T09:35:50.068082\"}', 0, '', '2025-01-04 09:35:50', 0);
INSERT INTO `sys_oper_log` VALUES (1026, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2035, \"menuName\": \"用例编辑\", \"menuType\": \"F\", \"orderNum\": 3, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"testcase:testcaseInfo:edit\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2025-01-04T09:36:09.182831\"}', 0, '', '2025-01-04 09:36:09', 1);
INSERT INTO `sys_oper_log` VALUES (1027, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2035, \"menuName\": \"用例删除\", \"menuType\": \"F\", \"orderNum\": 3, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"testcase:testcaseInfo:remove\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2025-01-04T09:36:34.382377\"}', 0, '', '2025-01-04 09:36:34', 4);
INSERT INTO `sys_oper_log` VALUES (1028, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2039, \"menuName\": \"用例编辑\", \"parentId\": 2035, \"orderNum\": 2, \"path\": \"\", \"component\": null, \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"F\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"testcase:testcaseInfo:edit\", \"icon\": \"#\", \"createBy\": \"admin\", \"createTime\": \"2025-01-04T09:36:09\", \"updateBy\": \"admin\", \"updateTime\": \"2025-01-04T09:36:09\", \"remark\": null}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2025-01-04T09:36:41.281463\"}', 0, '', '2025-01-04 09:36:41', 0);
INSERT INTO `sys_oper_log` VALUES (1029, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 2035, \"menuName\": \"用例运行\", \"menuType\": \"F\", \"orderNum\": 4, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"perms\": \"testcase:testcaseInfo:batch\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2025-01-04T09:37:07.811336\"}', 0, '', '2025-01-04 09:37:08', 1);
INSERT INTO `sys_oper_log` VALUES (1030, '字典类型', 2, 'module_admin.controller.dict_controller.refresh_system_dict()', 'DELETE', 1, 'admin', '研发部门', '/system/dict/type/refreshCache', '', '内网IP', '{}', '{\"code\": 200, \"msg\": \"刷新成功\", \"success\": true, \"time\": \"2025-01-04T14:22:38.299154\"}', 0, '', '2025-01-04 14:22:38', 3);
INSERT INTO `sys_oper_log` VALUES (1031, '字典类型', 1, 'module_admin.controller.dict_controller.add_system_dict_type()', 'POST', 1, 'admin', '研发部门', '/system/dict/type', '', '内网IP', '{\"dictName\": \"运行状态\", \"dictType\": \"run_status\", \"status\": \"0\", \"remark\": \"运行测试用例返回结果\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2025-01-04T14:24:48.545531\"}', 0, '', '2025-01-04 14:24:49', 0);
INSERT INTO `sys_oper_log` VALUES (1032, '字典数据', 1, 'module_admin.controller.dict_controller.add_system_dict_data()', 'POST', 1, 'admin', '研发部门', '/system/dict/data', '', '内网IP', '{\"dictLabel\": \"成功\", \"dictValue\": \"0\", \"listClass\": \"primary\", \"dictSort\": 1, \"status\": \"0\", \"remark\": \"成功状态\", \"dictType\": \"run_status\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2025-01-04T14:25:25.866877\"}', 0, '', '2025-01-04 14:25:26', 3);
INSERT INTO `sys_oper_log` VALUES (1033, '字典数据', 1, 'module_admin.controller.dict_controller.add_system_dict_data()', 'POST', 1, 'admin', '研发部门', '/system/dict/data', '', '内网IP', '{\"dictLabel\": \"失败\", \"dictValue\": \"1\", \"listClass\": \"warning\", \"dictSort\": 2, \"status\": \"0\", \"remark\": \"失败状态\", \"dictType\": \"run_status\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2025-01-04T14:25:54.715157\"}', 0, '', '2025-01-04 14:25:55', 1);
INSERT INTO `sys_oper_log` VALUES (1034, '字典数据', 2, 'module_admin.controller.dict_controller.edit_system_dict_data()', 'PUT', 1, 'admin', '研发部门', '/system/dict/data', '', '内网IP', '{\"dictCode\": 103, \"dictSort\": 2, \"dictLabel\": \"失败\", \"dictValue\": \"1\", \"dictType\": \"run_status\", \"cssClass\": null, \"listClass\": \"danger\", \"isDefault\": \"N\", \"status\": \"0\", \"createBy\": \"admin\", \"createTime\": \"2025-01-04T14:25:55\", \"updateBy\": \"admin\", \"updateTime\": \"2025-01-04T14:25:55\", \"remark\": \"失败状态\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2025-01-04T14:25:59.490234\"}', 0, '', '2025-01-04 14:25:59', 2);
INSERT INTO `sys_oper_log` VALUES (1035, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 116, \"menuName\": \"代码生成\", \"parentId\": 3, \"orderNum\": 2, \"path\": \"gen\", \"component\": \"tool/gen/index\", \"query\": \"\", \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"C\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"tool:gen:list\", \"icon\": \"code\", \"createBy\": \"admin\", \"createTime\": \"2024-08-13T18:18:19\", \"updateBy\": \"\", \"updateTime\": null, \"remark\": \"代码生成菜单\"}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2025-02-19T16:25:53.400204\"}', 0, '', '2025-02-19 16:25:53', 1);
INSERT INTO `sys_oper_log` VALUES (1036, '代码生成', 6, 'module_generator.controller.gen_controller.import_gen_table()', 'POST', 1, 'admin', '研发部门', '/tool/gen/importTable', '', '内网IP', '{}', '{\"code\": 200, \"msg\": \"导入成功\", \"success\": true, \"time\": \"2025-02-19T17:17:04.528221\"}', 0, '', '2025-02-19 17:17:04', 4);
INSERT INTO `sys_oper_log` VALUES (1037, '代码生成', 8, 'module_generator.controller.gen_controller.batch_gen_code()', 'GET', 1, 'admin', '研发部门', '/tool/gen/batchGenCode', '', '内网IP', '{}', '{\"code\": 601, \"msg\": \"请先完善生成配置信息\", \"success\": false, \"time\": \"2025-02-19T17:17:46.584012\"}', 1, '请先完善生成配置信息', '2025-02-19 17:17:47', 0);
INSERT INTO `sys_oper_log` VALUES (1038, '代码生成', 2, 'module_generator.controller.gen_controller.edit_gen_table()', 'PUT', 1, 'admin', '研发部门', '/tool/gen', '', '内网IP', '请求参数过长', '{\"code\": 500, \"msg\": \"module_generator.entity.vo.gen_vo.GenTableModel() argument after ** must be a mapping, not NoneType\", \"success\": false, \"time\": \"2025-02-19T17:21:05.291882\"}', 1, 'module_generator.entity.vo.gen_vo.GenTableModel() argument after ** must be a mapping, not NoneType', '2025-02-19 17:21:05', 8);
INSERT INTO `sys_oper_log` VALUES (1039, '代码生成', 2, 'module_generator.controller.gen_controller.edit_gen_table()', 'PUT', 1, 'admin', '研发部门', '/tool/gen', '', '内网IP', '请求参数过长', '{\"code\": 500, \"msg\": \"module_generator.entity.vo.gen_vo.GenTableModel() argument after ** must be a mapping, not NoneType\", \"success\": false, \"time\": \"2025-02-19T17:21:13.461295\"}', 1, 'module_generator.entity.vo.gen_vo.GenTableModel() argument after ** must be a mapping, not NoneType', '2025-02-19 17:21:13', 1);
INSERT INTO `sys_oper_log` VALUES (1040, '代码生成', 2, 'module_generator.controller.gen_controller.edit_gen_table()', 'PUT', 1, 'admin', '研发部门', '/tool/gen', '', '内网IP', '请求参数过长', '{\"code\": 500, \"msg\": \"module_generator.entity.vo.gen_vo.GenTableModel() argument after ** must be a mapping, not NoneType\", \"success\": false, \"time\": \"2025-02-19T17:21:47.523077\"}', 1, 'module_generator.entity.vo.gen_vo.GenTableModel() argument after ** must be a mapping, not NoneType', '2025-02-19 17:21:48', 1);
INSERT INTO `sys_oper_log` VALUES (1041, '代码生成', 2, 'module_generator.controller.gen_controller.edit_gen_table()', 'PUT', 1, 'admin', '研发部门', '/tool/gen', '', '内网IP', '请求参数过长', '{\"code\": 500, \"msg\": \"module_generator.entity.vo.gen_vo.GenTableModel() argument after ** must be a mapping, not NoneType\", \"success\": false, \"time\": \"2025-02-19T17:22:49.159012\"}', 1, 'module_generator.entity.vo.gen_vo.GenTableModel() argument after ** must be a mapping, not NoneType', '2025-02-19 17:22:49', 5);
INSERT INTO `sys_oper_log` VALUES (1042, '代码生成', 2, 'module_generator.controller.gen_controller.edit_gen_table()', 'PUT', 1, 'admin', '研发部门', '/tool/gen', '', '内网IP', '请求参数过长', '{\"code\": 500, \"msg\": \"module_generator.entity.vo.gen_vo.GenTableModel() argument after ** must be a mapping, not NoneType\", \"success\": false, \"time\": \"2025-02-19T17:24:32.165019\"}', 1, 'module_generator.entity.vo.gen_vo.GenTableModel() argument after ** must be a mapping, not NoneType', '2025-02-19 17:24:32', 6);
INSERT INTO `sys_oper_log` VALUES (1043, '代码生成', 2, 'module_generator.controller.gen_controller.edit_gen_table()', 'PUT', 1, 'admin', '研发部门', '/tool/gen', '', '内网IP', '请求参数过长', '{\"code\": 500, \"msg\": \"module_generator.entity.vo.gen_vo.GenTableModel() argument after ** must be a mapping, not NoneType\", \"success\": false, \"time\": \"2025-02-19T17:30:16.686684\"}', 1, 'module_generator.entity.vo.gen_vo.GenTableModel() argument after ** must be a mapping, not NoneType', '2025-02-19 17:30:17', 4);
INSERT INTO `sys_oper_log` VALUES (1044, '代码生成', 3, 'module_generator.controller.gen_controller.delete_gen_table()', 'DELETE', 1, 'admin', '研发部门', '/tool/gen/1', '', '内网IP', '{\"table_ids\": \"1\"}', '{\"code\": 200, \"msg\": \"删除成功\", \"success\": true, \"time\": \"2025-02-19T17:30:38.254437\"}', 0, '', '2025-02-19 17:30:38', 2);
INSERT INTO `sys_oper_log` VALUES (1045, '代码生成', 6, 'module_generator.controller.gen_controller.import_gen_table()', 'POST', 1, 'admin', '研发部门', '/tool/gen/importTable', '', '内网IP', '{}', '{\"code\": 200, \"msg\": \"导入成功\", \"success\": true, \"time\": \"2025-02-19T17:30:41.889533\"}', 0, '', '2025-02-19 17:30:42', 3);
INSERT INTO `sys_oper_log` VALUES (1046, '代码生成', 2, 'module_generator.controller.gen_controller.edit_gen_table()', 'PUT', 1, 'admin', '研发部门', '/tool/gen', '', '内网IP', '请求参数过长', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2025-02-19T17:31:06.150162\"}', 0, '', '2025-02-19 17:31:06', 2);
INSERT INTO `sys_oper_log` VALUES (1047, '代码生成', 3, 'module_generator.controller.gen_controller.delete_gen_table()', 'DELETE', 1, 'admin', '研发部门', '/tool/gen/2', '', '内网IP', '{\"table_ids\": \"2\"}', '{\"code\": 200, \"msg\": \"删除成功\", \"success\": true, \"time\": \"2025-02-21T16:30:46.246155\"}', 0, '', '2025-02-21 16:30:46', 1);
INSERT INTO `sys_oper_log` VALUES (1048, '代码生成', 6, 'module_generator.controller.gen_controller.import_gen_table()', 'POST', 1, 'admin', '研发部门', '/tool/gen/importTable', '', '内网IP', '{}', '{\"code\": 200, \"msg\": \"导入成功\", \"success\": true, \"time\": \"2025-02-21T16:30:49.737927\"}', 0, '', '2025-02-21 16:30:50', 4);
INSERT INTO `sys_oper_log` VALUES (1049, '代码生成', 2, 'module_generator.controller.gen_controller.edit_gen_table()', 'PUT', 1, 'admin', '研发部门', '/tool/gen', '', '内网IP', '请求参数过长', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2025-02-21T16:31:11.524069\"}', 0, '', '2025-02-21 16:31:11', 5);
INSERT INTO `sys_oper_log` VALUES (1050, '代码生成', 3, 'module_generator.controller.gen_controller.delete_gen_table()', 'DELETE', 1, 'admin', '研发部门', '/tool/gen/3', '', '内网IP', '{\"table_ids\": \"3\"}', '{\"code\": 200, \"msg\": \"删除成功\", \"success\": true, \"time\": \"2025-02-21T16:31:53.739546\"}', 0, '', '2025-02-21 16:31:54', 0);
INSERT INTO `sys_oper_log` VALUES (1051, '代码生成', 6, 'module_generator.controller.gen_controller.import_gen_table()', 'POST', 1, 'admin', '研发部门', '/tool/gen/importTable', '', '内网IP', '{}', '{\"code\": 200, \"msg\": \"导入成功\", \"success\": true, \"time\": \"2025-02-21T16:31:56.339913\"}', 0, '', '2025-02-21 16:31:56', 4);
INSERT INTO `sys_oper_log` VALUES (1052, '代码生成', 2, 'module_generator.controller.gen_controller.edit_gen_table()', 'PUT', 1, 'admin', '研发部门', '/tool/gen', '', '内网IP', '请求参数过长', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2025-02-21T16:35:38.955731\"}', 0, '', '2025-02-21 16:35:39', 3);
INSERT INTO `sys_oper_log` VALUES (1053, '代码生成', 3, 'module_generator.controller.gen_controller.delete_gen_table()', 'DELETE', 1, 'admin', '研发部门', '/tool/gen/4', '', '内网IP', '{\"table_ids\": \"4\"}', '{\"code\": 200, \"msg\": \"删除成功\", \"success\": true, \"time\": \"2025-02-21T16:36:08.004914\"}', 0, '', '2025-02-21 16:36:08', 0);
INSERT INTO `sys_oper_log` VALUES (1054, '代码生成', 6, 'module_generator.controller.gen_controller.import_gen_table()', 'POST', 1, 'admin', '研发部门', '/tool/gen/importTable', '', '内网IP', '{}', '{\"code\": 200, \"msg\": \"导入成功\", \"success\": true, \"time\": \"2025-02-21T16:36:17.450249\"}', 0, '', '2025-02-21 16:36:17', 1);
INSERT INTO `sys_oper_log` VALUES (1055, '代码生成', 2, 'module_generator.controller.gen_controller.edit_gen_table()', 'PUT', 1, 'admin', '研发部门', '/tool/gen', '', '内网IP', '请求参数过长', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2025-02-21T16:36:35.963854\"}', 0, '', '2025-02-21 16:36:36', 1);
INSERT INTO `sys_oper_log` VALUES (1056, '代码生成', 2, 'module_generator.controller.gen_controller.edit_gen_table()', 'PUT', 1, 'admin', '研发部门', '/tool/gen', '', '内网IP', '请求参数过长', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2025-02-21T16:37:25.761875\"}', 0, '', '2025-02-21 16:37:26', 1);
INSERT INTO `sys_oper_log` VALUES (1057, '代码生成', 2, 'module_generator.controller.gen_controller.sync_db()', 'GET', 1, 'admin', '研发部门', '/tool/gen/synchDb/demo', '', '内网IP', '{\"table_name\": \"demo\"}', '{\"code\": 200, \"msg\": \"操作成功\", \"data\": \"同步成功\", \"success\": true, \"time\": \"2025-02-21T16:37:28.623290\"}', 0, '', '2025-02-21 16:37:29', 1);
INSERT INTO `sys_oper_log` VALUES (1058, '代码生成', 2, 'module_generator.controller.gen_controller.sync_db()', 'GET', 1, 'admin', '研发部门', '/tool/gen/synchDb/demo', '', '内网IP', '{\"table_name\": \"demo\"}', '{\"code\": 200, \"msg\": \"操作成功\", \"data\": \"同步成功\", \"success\": true, \"time\": \"2025-02-21T16:37:57.126047\"}', 0, '', '2025-02-21 16:37:57', 1);
INSERT INTO `sys_oper_log` VALUES (1059, '代码生成', 2, 'module_generator.controller.gen_controller.sync_db()', 'GET', 1, 'admin', '研发部门', '/tool/gen/synchDb/demo', '', '内网IP', '{\"table_name\": \"demo\"}', '{\"code\": 200, \"msg\": \"操作成功\", \"data\": \"同步成功\", \"success\": true, \"time\": \"2025-02-21T16:38:16.692876\"}', 0, '', '2025-02-21 16:38:17', 2);
INSERT INTO `sys_oper_log` VALUES (1060, '代码生成', 8, 'module_generator.controller.gen_controller.batch_gen_code()', 'GET', 1, 'admin', '研发部门', '/tool/gen/batchGenCode', '', '内网IP', '{}', '{\"code\": 200, \"message\": \"获取成功\"}', 0, '', '2025-04-14 13:59:54', 27);
INSERT INTO `sys_oper_log` VALUES (1061, '代码生成', 2, 'module_generator.controller.gen_controller.edit_gen_table()', 'PUT', 1, 'admin', '研发部门', '/tool/gen', '', '内网IP', '请求参数过长', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2025-04-14T14:01:08.825088\"}', 0, '', '2025-04-14 14:01:09', 3);
INSERT INTO `sys_oper_log` VALUES (1062, '菜单管理', 1, 'module_admin.controller.menu_controller.add_system_menu()', 'POST', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"parentId\": 0, \"menuName\": \"AI管家\", \"icon\": \"404\", \"menuType\": \"C\", \"orderNum\": 4, \"isFrame\": 1, \"isCache\": 0, \"visible\": \"0\", \"status\": \"0\", \"path\": \"ai_chat\", \"perms\": \"ai/chat/index\"}', '{\"code\": 200, \"msg\": \"新增成功\", \"success\": true, \"time\": \"2025-04-16T10:19:17.976905\"}', 0, '', '2025-04-16 10:19:18', 2);
INSERT INTO `sys_oper_log` VALUES (1063, '菜单管理', 2, 'module_admin.controller.menu_controller.edit_system_menu()', 'PUT', 1, 'admin', '研发部门', '/system/menu', '', '内网IP', '{\"menuId\": 2042, \"menuName\": \"AI管家\", \"parentId\": 0, \"orderNum\": 4, \"path\": \"ai_chat\", \"component\": \"ai/chat/index\", \"query\": null, \"routeName\": \"\", \"isFrame\": 1, \"isCache\": 0, \"menuType\": \"C\", \"visible\": \"0\", \"status\": \"0\", \"perms\": \"\", \"icon\": \"404\", \"createBy\": \"admin\", \"createTime\": \"2025-04-16T10:19:18\", \"updateBy\": \"admin\", \"updateTime\": \"2025-04-16T10:19:18\", \"remark\": null}', '{\"code\": 200, \"msg\": \"更新成功\", \"success\": true, \"time\": \"2025-04-16T10:19:48.815649\"}', 0, '', '2025-04-16 10:19:49', 1);

-- ----------------------------
-- Table structure for sys_post
-- ----------------------------
DROP TABLE IF EXISTS `sys_post`;
CREATE TABLE `sys_post`  (
  `post_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '岗位ID',
  `post_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '岗位编码',
  `post_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '岗位名称',
  `post_sort` int(0) NOT NULL COMMENT '显示顺序',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`post_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 100 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '岗位信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_post
-- ----------------------------
INSERT INTO `sys_post` VALUES (1, 'ceo', '董事长', 1, '0', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_post` VALUES (2, 'se', '项目经理', 2, '0', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_post` VALUES (3, 'hr', '人力资源', 3, '0', 'admin', '2024-08-13 18:18:19', '', NULL, '');
INSERT INTO `sys_post` VALUES (4, 'user', '普通员工', 4, '0', 'admin', '2024-08-13 18:18:19', '', NULL, '');

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role`  (
  `role_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `role_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色名称',
  `role_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色权限字符串',
  `role_sort` int(0) NOT NULL COMMENT '显示顺序',
  `data_scope` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '1' COMMENT '数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）',
  `menu_check_strictly` tinyint(1) NULL DEFAULT 1 COMMENT '菜单树选择项是否关联显示',
  `dept_check_strictly` tinyint(1) NULL DEFAULT 1 COMMENT '部门树选择项是否关联显示',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色状态（0正常 1停用）',
  `del_flag` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`role_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 101 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO `sys_role` VALUES (1, '超级管理员', 'admin', 1, '1', 1, 1, '0', '0', 'admin', '2024-08-13 18:18:19', '', NULL, '超级管理员');
INSERT INTO `sys_role` VALUES (2, '普通角色', 'common', 3, '1', 1, 1, '0', '0', 'admin', '2024-08-13 18:18:19', 'admin', '2024-09-20 22:40:40', '普通角色');
INSERT INTO `sys_role` VALUES (100, '开发者', ' dev', 2, '1', 1, 1, '0', '0', 'admin', '2024-08-14 17:32:10', 'admin', '2024-09-20 22:41:57', '这是一个开发者权限的角色');

-- ----------------------------
-- Table structure for sys_role_dept
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_dept`;
CREATE TABLE `sys_role_dept`  (
  `role_id` bigint(0) NOT NULL COMMENT '角色ID',
  `dept_id` bigint(0) NOT NULL COMMENT '部门ID',
  PRIMARY KEY (`role_id`, `dept_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色和部门关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role_dept
-- ----------------------------

-- ----------------------------
-- Table structure for sys_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_menu`;
CREATE TABLE `sys_role_menu`  (
  `role_id` bigint(0) NOT NULL COMMENT '角色ID',
  `menu_id` bigint(0) NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`role_id`, `menu_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色和菜单关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role_menu
-- ----------------------------
INSERT INTO `sys_role_menu` VALUES (2, 2001);
INSERT INTO `sys_role_menu` VALUES (2, 2002);
INSERT INTO `sys_role_menu` VALUES (2, 2006);
INSERT INTO `sys_role_menu` VALUES (100, 1);
INSERT INTO `sys_role_menu` VALUES (100, 2);
INSERT INTO `sys_role_menu` VALUES (100, 3);
INSERT INTO `sys_role_menu` VALUES (100, 100);
INSERT INTO `sys_role_menu` VALUES (100, 101);
INSERT INTO `sys_role_menu` VALUES (100, 102);
INSERT INTO `sys_role_menu` VALUES (100, 103);
INSERT INTO `sys_role_menu` VALUES (100, 104);
INSERT INTO `sys_role_menu` VALUES (100, 105);
INSERT INTO `sys_role_menu` VALUES (100, 106);
INSERT INTO `sys_role_menu` VALUES (100, 107);
INSERT INTO `sys_role_menu` VALUES (100, 108);
INSERT INTO `sys_role_menu` VALUES (100, 109);
INSERT INTO `sys_role_menu` VALUES (100, 110);
INSERT INTO `sys_role_menu` VALUES (100, 111);
INSERT INTO `sys_role_menu` VALUES (100, 112);
INSERT INTO `sys_role_menu` VALUES (100, 113);
INSERT INTO `sys_role_menu` VALUES (100, 114);
INSERT INTO `sys_role_menu` VALUES (100, 115);
INSERT INTO `sys_role_menu` VALUES (100, 116);
INSERT INTO `sys_role_menu` VALUES (100, 117);
INSERT INTO `sys_role_menu` VALUES (100, 500);
INSERT INTO `sys_role_menu` VALUES (100, 501);
INSERT INTO `sys_role_menu` VALUES (100, 1000);
INSERT INTO `sys_role_menu` VALUES (100, 1001);
INSERT INTO `sys_role_menu` VALUES (100, 1002);
INSERT INTO `sys_role_menu` VALUES (100, 1003);
INSERT INTO `sys_role_menu` VALUES (100, 1004);
INSERT INTO `sys_role_menu` VALUES (100, 1005);
INSERT INTO `sys_role_menu` VALUES (100, 1006);
INSERT INTO `sys_role_menu` VALUES (100, 1007);
INSERT INTO `sys_role_menu` VALUES (100, 1008);
INSERT INTO `sys_role_menu` VALUES (100, 1009);
INSERT INTO `sys_role_menu` VALUES (100, 1010);
INSERT INTO `sys_role_menu` VALUES (100, 1011);
INSERT INTO `sys_role_menu` VALUES (100, 1012);
INSERT INTO `sys_role_menu` VALUES (100, 1013);
INSERT INTO `sys_role_menu` VALUES (100, 1014);
INSERT INTO `sys_role_menu` VALUES (100, 1015);
INSERT INTO `sys_role_menu` VALUES (100, 1016);
INSERT INTO `sys_role_menu` VALUES (100, 1017);
INSERT INTO `sys_role_menu` VALUES (100, 1018);
INSERT INTO `sys_role_menu` VALUES (100, 1019);
INSERT INTO `sys_role_menu` VALUES (100, 1020);
INSERT INTO `sys_role_menu` VALUES (100, 1021);
INSERT INTO `sys_role_menu` VALUES (100, 1022);
INSERT INTO `sys_role_menu` VALUES (100, 1023);
INSERT INTO `sys_role_menu` VALUES (100, 1024);
INSERT INTO `sys_role_menu` VALUES (100, 1025);
INSERT INTO `sys_role_menu` VALUES (100, 1026);
INSERT INTO `sys_role_menu` VALUES (100, 1027);
INSERT INTO `sys_role_menu` VALUES (100, 1028);
INSERT INTO `sys_role_menu` VALUES (100, 1029);
INSERT INTO `sys_role_menu` VALUES (100, 1030);
INSERT INTO `sys_role_menu` VALUES (100, 1031);
INSERT INTO `sys_role_menu` VALUES (100, 1032);
INSERT INTO `sys_role_menu` VALUES (100, 1033);
INSERT INTO `sys_role_menu` VALUES (100, 1034);
INSERT INTO `sys_role_menu` VALUES (100, 1035);
INSERT INTO `sys_role_menu` VALUES (100, 1036);
INSERT INTO `sys_role_menu` VALUES (100, 1037);
INSERT INTO `sys_role_menu` VALUES (100, 1038);
INSERT INTO `sys_role_menu` VALUES (100, 1039);
INSERT INTO `sys_role_menu` VALUES (100, 1040);
INSERT INTO `sys_role_menu` VALUES (100, 1041);
INSERT INTO `sys_role_menu` VALUES (100, 1042);
INSERT INTO `sys_role_menu` VALUES (100, 1043);
INSERT INTO `sys_role_menu` VALUES (100, 1044);
INSERT INTO `sys_role_menu` VALUES (100, 1045);
INSERT INTO `sys_role_menu` VALUES (100, 1046);
INSERT INTO `sys_role_menu` VALUES (100, 1047);
INSERT INTO `sys_role_menu` VALUES (100, 1048);
INSERT INTO `sys_role_menu` VALUES (100, 1049);
INSERT INTO `sys_role_menu` VALUES (100, 1050);
INSERT INTO `sys_role_menu` VALUES (100, 1051);
INSERT INTO `sys_role_menu` VALUES (100, 1052);
INSERT INTO `sys_role_menu` VALUES (100, 1053);
INSERT INTO `sys_role_menu` VALUES (100, 1054);
INSERT INTO `sys_role_menu` VALUES (100, 1055);
INSERT INTO `sys_role_menu` VALUES (100, 1056);
INSERT INTO `sys_role_menu` VALUES (100, 1057);
INSERT INTO `sys_role_menu` VALUES (100, 1058);
INSERT INTO `sys_role_menu` VALUES (100, 1059);
INSERT INTO `sys_role_menu` VALUES (100, 1060);
INSERT INTO `sys_role_menu` VALUES (100, 2001);
INSERT INTO `sys_role_menu` VALUES (100, 2002);
INSERT INTO `sys_role_menu` VALUES (100, 2003);
INSERT INTO `sys_role_menu` VALUES (100, 2004);
INSERT INTO `sys_role_menu` VALUES (100, 2005);
INSERT INTO `sys_role_menu` VALUES (100, 2006);
INSERT INTO `sys_role_menu` VALUES (100, 2007);
INSERT INTO `sys_role_menu` VALUES (100, 2008);
INSERT INTO `sys_role_menu` VALUES (100, 2009);
INSERT INTO `sys_role_menu` VALUES (100, 2010);
INSERT INTO `sys_role_menu` VALUES (100, 2011);
INSERT INTO `sys_role_menu` VALUES (100, 2012);
INSERT INTO `sys_role_menu` VALUES (100, 2013);
INSERT INTO `sys_role_menu` VALUES (100, 2014);
INSERT INTO `sys_role_menu` VALUES (100, 2016);
INSERT INTO `sys_role_menu` VALUES (100, 2017);
INSERT INTO `sys_role_menu` VALUES (100, 2018);

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
  `user_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `dept_id` bigint(0) NULL DEFAULT NULL COMMENT '部门ID',
  `user_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户账号',
  `nick_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户昵称',
  `user_type` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '00' COMMENT '用户类型（00系统用户）',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '用户邮箱',
  `phonenumber` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '手机号码',
  `sex` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '用户性别（0男 1女 2未知）',
  `avatar` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '头像地址',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '密码',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '帐号状态（0正常 1停用）',
  `del_flag` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  `login_ip` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '最后登录IP',
  `login_date` datetime(0) NULL DEFAULT NULL COMMENT '最后登录时间',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 106 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES (1, 103, 'admin', '超级管理员', '00', 'ranyong@163.com', '15888888888', '0', '/profile/avatar/2024/11/18/avatar_20241118130722A292.png', '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '0', '0', '172.0.29.1', '2025-04-16 10:07:20', 'admin', '2024-08-13 18:18:19', 'admin', '2024-11-18 13:07:23', '管理员');
INSERT INTO `sys_user` VALUES (2, 105, 'niangao', '年糕', '00', 'niangao@qq.com', '15666666666', '1', '', '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '0', '2', '127.0.0.1', '2024-08-13 18:18:19', 'admin', '2024-08-13 18:18:19', 'admin', '2024-09-20 22:45:06', '测试员');
INSERT INTO `sys_user` VALUES (100, 100, 'ranyong', 'ranyong', '00', '', '', '0', '', '$2b$12$iPYmQp3jjdIrZBqyaf6loOITsuvUQost39wHqNzzBCTOge7cmNblW', '0', '0', '', NULL, 'admin', '2024-08-13 20:47:13', 'admin', '2024-08-15 11:04:07', NULL);
INSERT INTO `sys_user` VALUES (101, 103, 'demo1', 'demo1', '00', '', '', '0', '', '$2b$12$bFu.K.grA9O/zrZ9aQTGzeE4PjKwRbXJMm9rgJpN8ZzT5Ri2LXsve', '0', '0', '', '2024-09-20 22:40:21', '', '2024-08-16 10:28:18', 'admin', '2024-09-20 22:44:56', NULL);
INSERT INTO `sys_user` VALUES (102, NULL, 'Jason', 'Jason', '00', '', '', '0', '', '$2b$12$bDYfcn1CtgaTCJFtZHp0Z.E2sSmwJlCjmmEe5EWy4hwbC3r3OHk7e', '0', '2', '', '2024-08-19 11:08:18', '', '2024-08-16 11:26:38', 'admin', '2024-09-20 22:33:54', NULL);
INSERT INTO `sys_user` VALUES (103, NULL, 'Robert', 'Robert', '00', '', '', '0', '', '$2b$12$wUoLMRIV5NGRiaTEnNEFv.n4xa8TySTvOm3ZTFLh2pjC6wdugN9ii', '0', '2', '', NULL, '', '2024-08-16 11:26:38', 'admin', '2024-08-19 10:09:30', NULL);
INSERT INTO `sys_user` VALUES (105, NULL, 'ranyong123', 'ranyong123', '00', '', '', '0', '', '$2b$12$NfuBd5.zv64M1XGW0KB.Ueql1AZJNBLKMtk5cOHtP0g5VkmrKXFRC', '0', '2', '', NULL, '', '2024-09-25 11:14:52', 'admin', '2024-10-02 00:35:54', NULL);

-- ----------------------------
-- Table structure for sys_user_post
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_post`;
CREATE TABLE `sys_user_post`  (
  `user_id` bigint(0) NOT NULL COMMENT '用户ID',
  `post_id` bigint(0) NOT NULL COMMENT '岗位ID',
  PRIMARY KEY (`user_id`, `post_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户与岗位关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user_post
-- ----------------------------
INSERT INTO `sys_user_post` VALUES (1, 1);

-- ----------------------------
-- Table structure for sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role`  (
  `user_id` bigint(0) NOT NULL COMMENT '用户ID',
  `role_id` bigint(0) NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`user_id`, `role_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户和角色关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user_role
-- ----------------------------
INSERT INTO `sys_user_role` VALUES (1, 1);
INSERT INTO `sys_user_role` VALUES (100, 100);
INSERT INTO `sys_user_role` VALUES (101, 2);

-- ----------------------------
-- Table structure for testcase_info
-- ----------------------------
DROP TABLE IF EXISTS `testcase_info`;
CREATE TABLE `testcase_info`  (
  `testcase_id` int(0) NOT NULL AUTO_INCREMENT COMMENT '测试用例ID',
  `testcase_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '测试用例名称',
  `project_id` int(0) NOT NULL COMMENT '项目ID',
  `testcase_list` json NOT NULL COMMENT '测试用例数组',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`testcase_id`) USING BTREE,
  INDEX `ix_testcase_info_testcase_name`(`testcase_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '测试用例表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of testcase_info
-- ----------------------------
INSERT INTO `testcase_info` VALUES (1, '测试编辑测试用例', 1, '[1, 2, 3]', 'string', '2024-11-27 10:36:17', 'admin', '2024-11-27 19:22:42', 'string');
INSERT INTO `testcase_info` VALUES (2, '测试2', 2, '[1, 2, 3]', 'admin', '2025-01-04 10:53:08', 'admin', '2025-01-04 10:53:12', '123');

-- ----------------------------
-- Table structure for user_wechat
-- ----------------------------
DROP TABLE IF EXISTS `user_wechat`;
CREATE TABLE `user_wechat`  (
  `user_id` int(0) NOT NULL COMMENT '用户ID',
  `city` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '城市',
  `country` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '国家',
  `head_img_url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '微信头像',
  `nickname` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '微信昵称',
  `openid` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'openid',
  `union_id` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'union_id',
  `user_phone` varchar(15) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '手机号',
  `province` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '省份',
  `sex` int(0) NULL DEFAULT NULL COMMENT '性别',
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(0) NOT NULL COMMENT '创建时间',
  `update_time` datetime(0) NOT NULL COMMENT '更新时间',
  `del_flag` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `openid`(`openid`) USING BTREE,
  UNIQUE INDEX `user_phone`(`user_phone`) USING BTREE,
  INDEX `ix_user_wechat_update_time`(`update_time`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_wechat
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
