/*
 Navicat Premium Dump SQL

 Source Server         : 120服务器-测试服
 Source Server Type    : MySQL
 Source Server Version : 50731 (5.7.31)
 Source Host           : 61.145.163.190:59296
 Source Schema         : bms

 Target Server Type    : MySQL
 Target Server Version : 50731 (5.7.31)
 File Encoding         : 65001

 Date: 23/05/2025 14:02:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for access_system
-- ----------------------------
DROP TABLE IF EXISTS `access_system`;
CREATE TABLE `access_system`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '接入系统名称',
  `code` char(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '接入系统编码',
  `contact_name` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系人姓名',
  `contact_phone` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系人电话',
  `enabled` tinyint(2) NULL DEFAULT NULL COMMENT '是否启用; -1 禁用; 1 启用',
  `deadline_date` date NULL DEFAULT NULL COMMENT '截止时间',
  `url` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '推送url',
  `app_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'appId',
  `app_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'appKey',
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '接入系统表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for alarm
-- ----------------------------
DROP TABLE IF EXISTS `alarm`;
CREATE TABLE `alarm`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `alarm_status` tinyint(1) NULL DEFAULT NULL COMMENT '报警处理状态（未处理、处理中、已处理）',
  `alarm_result` tinyint(1) NULL DEFAULT NULL COMMENT '处理结果/设备状态（正常、修复、报警、拆除）',
  `charge_man` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '负责人',
  `charge_phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电话号码',
  `predict_complete_time` datetime NULL DEFAULT NULL COMMENT '预计完成时间',
  `real_complete_time` datetime NULL DEFAULT NULL COMMENT '完成时间',
  `danger_score` bigint(10) NULL DEFAULT NULL COMMENT '危险评分',
  `duration` int(10) NULL DEFAULT NULL COMMENT '处理耗时（分钟）',
  `fall_index` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `swing_index` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `lean_index` decimal(10, 5) NULL DEFAULT NULL COMMENT '倾斜度数',
  `alarm_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '报警细节描述',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `handle_type` tinyint(2) NULL DEFAULT NULL COMMENT '处理类型',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `danger_level` tinyint(1) NULL DEFAULT NULL COMMENT '危险等级(1~29低级1 30~59中级2 60~100高级3 )',
  `alarm_type_number` int(50) NULL DEFAULT NULL COMMENT '报警类型10进制表示',
  `lean_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '倾斜报警值',
  `distance_x_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '三角位移报警值',
  `distance_y_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '三角沉降报警值',
  `gap_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '裂缝报警值',
  `water_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '水位报警值',
  `gradienter_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '水准仪沉降报警值',
  `displacement_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '位移报警值',
  `deep_displacement_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '深度位移报警值',
  `rtk_distance_x_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'rtk位移报警值',
  `rtk_distance_y_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'rtk沉降报警值',
  `srx` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '振动频率',
  `sry` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '振动幅度mm/s',
  `total_alarm_type_number` int(50) NULL DEFAULT NULL COMMENT '总报警类型',
  `day_alarm_type_number` int(50) NULL DEFAULT NULL COMMENT '日变化报警类型',
  `month_alarm_type_number` int(50) NULL DEFAULT NULL COMMENT '月变化报警类型',
  `total_alarm_desc` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总报警描述',
  `day_alarm_desc` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '日变化报警描述',
  `month_alarm_desc` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '月变化报警描述',
  `alarm_level` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '报警等级json',
  `device_alarm_level` tinyint(2) NULL DEFAULT NULL COMMENT '设备报警等级',
  `pre_device_alarm_level` tinyint(2) NULL DEFAULT NULL COMMENT '设备原报警等级',
  `update_level` tinyint(2) NULL DEFAULT 0 COMMENT '报警等级升级数',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `day_average_alarm_type_number` int(50) NULL DEFAULT NULL COMMENT '日均报警类型',
  `day_average_alarm_desc` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '日均报警描述',
  `rebar_stress_meter_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '钢筋应力报警值',
  `rebar_strain_gauge_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '钢筋应变报警值',
  `surface_strain_gauge_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '表面应变报警值',
  `wind_speed_direction_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '风速风向报警值',
  `vibration_value` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '振动报警值',
  `newest_time` datetime NULL DEFAULT NULL COMMENT '最新预警时间',
  `earth_pressure_meter_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '土压力计报警值',
  `rainfall_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '雨量报警值',
  `soil_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '土壤报警值',
  `slope_meter_value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '测斜仪报警值',
  `water_pressure_meter_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '水压力计报警值',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time`(`imei`, `crt_time`) USING BTREE,
  INDEX `idx_did_time`(`data_id`, `crt_time`) USING BTREE,
  INDEX `idx_did_imei_time`(`data_id`, `imei`, `crt_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1120753465950482441 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '警报表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for alarm_capture
-- ----------------------------
DROP TABLE IF EXISTS `alarm_capture`;
CREATE TABLE `alarm_capture`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `alarm_id` bigint(50) NULL DEFAULT NULL COMMENT '报警id',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备号',
  `pic_url` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '图片地址',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 129129 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报警抓拍表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for alarm_common_threshold
-- ----------------------------
DROP TABLE IF EXISTS `alarm_common_threshold`;
CREATE TABLE `alarm_common_threshold`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备位置号（用于区分一对多设备）',
  `enabled_config` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '启用的配置项',
  `timeout_threshold` int(11) NULL DEFAULT NULL COMMENT '超时报警阈值',
  `common_threshold` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '通用报警阈值',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_imei`(`imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 365 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备报警阈值配置表(通用)' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for alarm_history
-- ----------------------------
DROP TABLE IF EXISTS `alarm_history`;
CREATE TABLE `alarm_history`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `alarm_status` tinyint(1) NULL DEFAULT NULL COMMENT '报警处理状态（0：未处理 1：处理中 2：已处理）',
  `pre_device_alarm_level` tinyint(2) NULL DEFAULT NULL COMMENT '设备原报警等级',
  `total_alarm_desc` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总报警描述',
  `alarm_id` bigint(50) NOT NULL COMMENT '关联报警表id',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `device_alarm_level` tinyint(2) NULL DEFAULT NULL COMMENT '现预警等级',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time`(`imei`, `crt_time`) USING BTREE,
  INDEX `idx_alarm_id_alarm_status`(`alarm_id`, `alarm_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1123291405016641537 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '警报历史表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for alarm_task
-- ----------------------------
DROP TABLE IF EXISTS `alarm_task`;
CREATE TABLE `alarm_task`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `task_mark_id` bigint(50) NULL DEFAULT NULL COMMENT '同一个报警任务标识Id',
  `alarm_id` bigint(50) NULL DEFAULT NULL COMMENT '报警Id',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备IMEI',
  `msg_status` tinyint(2) NULL DEFAULT NULL COMMENT '是否向下传递',
  `type` tinyint(2) NULL DEFAULT NULL COMMENT '类型',
  `handle_status` tinyint(2) NULL DEFAULT NULL COMMENT '处理状态',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '处理详情',
  `handle_user_id` int(11) NULL DEFAULT NULL COMMENT '处理人id',
  `handle_user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '处理人姓名',
  `handle_time` datetime NULL DEFAULT NULL COMMENT '处理人姓名',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 343 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报警任务表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for alarm_threshold
-- ----------------------------
DROP TABLE IF EXISTS `alarm_threshold`;
CREATE TABLE `alarm_threshold`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备号',
  `enabled_config` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '启用的配置项（fall, swing, spin, lean）',
  `spin_threshold` decimal(10, 2) NULL DEFAULT NULL COMMENT '旋转报警阈值',
  `swing_threshold` int(10) NULL DEFAULT NULL COMMENT '摇摆报警阈值',
  `lean_threshold` decimal(10, 2) NULL DEFAULT NULL COMMENT '倾斜报警阈值',
  `distance_threshold` decimal(10, 2) NULL DEFAULT NULL COMMENT '位移报警阈值',
  `timeout_threshold` decimal(10, 2) NULL DEFAULT NULL COMMENT '超时阈值',
  `frequency_threshold` decimal(10, 2) NULL DEFAULT NULL COMMENT '频繁上报阈值',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  `algorithm_threshold` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '算法报警阈值配置项',
  `gap_threshold` decimal(20, 2) NULL DEFAULT NULL COMMENT '裂缝阈值',
  `water_threshold` decimal(20, 0) NULL DEFAULT NULL COMMENT '水位阈值',
  `gradienter_threshold` decimal(20, 2) NULL DEFAULT NULL COMMENT '水准沉降阈值',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_imei`(`imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1888 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备报警阈值配置表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for alarm_threshold_plus
-- ----------------------------
DROP TABLE IF EXISTS `alarm_threshold_plus`;
CREATE TABLE `alarm_threshold_plus`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `enabled_config` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '启用的配置项',
  `timeout_threshold` int(11) NULL DEFAULT NULL COMMENT '超时报警阈值',
  `lean_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '倾斜报警阈值',
  `distance_x_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '三角位移报警阈值',
  `distance_y_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '三角沉降报警阈值',
  `gap_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '裂缝报警阈值',
  `water_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '水位报警阈值',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  `rebar_stress_meter_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '钢筋应力报警阈值',
  `rebar_strain_gauge_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '钢筋应变报警阈值',
  `surface_strain_gauge_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '表面应变报警阈值',
  `wind_speed_direction_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '风速风向报警阈值',
  `earth_pressure_meter_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '土压力计报警阈值',
  `rainfall_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '雨量报警阈值',
  `soil_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '土壤报警阈值',
  `vibration_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '振动仪频率报警阈值',
  `slope_meter_threshold` varchar(5120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '深部测斜仪报警阈值',
  `water_pressure_meter_threshold` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '水压力计报警阈值',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_imei`(`imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15612 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备报警阈值配置表(新)' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for alarm_threshold_template
-- ----------------------------
DROP TABLE IF EXISTS `alarm_threshold_template`;
CREATE TABLE `alarm_threshold_template`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(10) NOT NULL COMMENT '所属组织',
  `config_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '名称',
  `alarm_threshold_config` varchar(15000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '报警阈值',
  `reference_standard` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '参考标准',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_group_id`(`group_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 358 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报警阈值模板' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for alarm_track
-- ----------------------------
DROP TABLE IF EXISTS `alarm_track`;
CREATE TABLE `alarm_track`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT 'Id',
  `alarm_id` bigint(50) NULL DEFAULT NULL COMMENT '预警id',
  `track_status` tinyint(2) NULL DEFAULT NULL COMMENT '追踪状态（0-未处理 2-已处理）',
  `result` decimal(10, 5) NULL DEFAULT NULL COMMENT '计算结果',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1117494273965830145 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报警追踪表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for alarm_user
-- ----------------------------
DROP TABLE IF EXISTS `alarm_user`;
CREATE TABLE `alarm_user`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `group_id` int(50) NULL DEFAULT NULL COMMENT '组织列表id',
  `alarm_user_id` int(50) NULL DEFAULT NULL COMMENT '报警处理人员',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报警人员处理表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for alarm_value_record
-- ----------------------------
DROP TABLE IF EXISTS `alarm_value_record`;
CREATE TABLE `alarm_value_record`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `alarm_value` decimal(10, 6) NULL DEFAULT NULL COMMENT '预警结果',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备IMEI',
  `alarm_type` tinyint(4) NULL DEFAULT NULL COMMENT '预警类型',
  `crt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `alarm_id` bigint(50) NULL DEFAULT NULL COMMENT '报警Id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_imei`(`imei`) USING BTREE,
  INDEX `index_alarm_id`(`alarm_id`) USING BTREE,
  INDEX `idx_imei`(`imei`) USING BTREE,
  INDEX `idx_alarm_id`(`alarm_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1120000461118910465 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '预警记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for algorithm
-- ----------------------------
DROP TABLE IF EXISTS `algorithm`;
CREATE TABLE `algorithm`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '算法名称',
  `type` tinyint(2) NULL DEFAULT NULL COMMENT '类型',
  `identify_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '标识（与Java函数对应）',
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  `be_union` tinyint(4) NULL DEFAULT NULL COMMENT '是否联合算法',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '算法表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for algorithm_config
-- ----------------------------
DROP TABLE IF EXISTS `algorithm_config`;
CREATE TABLE `algorithm_config`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `algorithm_id` int(11) NOT NULL COMMENT '算法id',
  `zh_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '配置项名称',
  `en_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '字段名称(计算时使用的字段)',
  `max_value` int(11) NULL DEFAULT NULL COMMENT '最大值',
  `min_value` int(11) NULL DEFAULT NULL COMMENT '最小值',
  `default_value` int(11) NULL DEFAULT NULL COMMENT '默认值',
  `required` tinyint(1) NULL DEFAULT NULL COMMENT '是否必填',
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '算法配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for application_scene
-- ----------------------------
DROP TABLE IF EXISTS `application_scene`;
CREATE TABLE `application_scene`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(10) NOT NULL COMMENT '所属组织',
  `config_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '类型',
  `config_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '名称',
  `alarm_threshold_config` varchar(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '报警阈值',
  `reference_standard` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '参考标准',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 412 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '应用场景' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for audible_alarm
-- ----------------------------
DROP TABLE IF EXISTS `audible_alarm`;
CREATE TABLE `audible_alarm`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `audible_alarm_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '声光报警器id',
  `audible_alarm_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备key',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备名称',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `group_id` int(11) NOT NULL COMMENT '所属组织',
  `alarm_desc` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '播报内容',
  `alarm_level_combo` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预警等级(组合)',
  `play_count` int(4) NULL DEFAULT 1 COMMENT '播放次数',
  `volume` int(3) NULL DEFAULT 30 COMMENT '音量大小',
  `iot_card` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '物联网卡卡号',
  `period_start` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '07:00' COMMENT '报警时段开始',
  `period_end` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '22:00' COMMENT '报警时段开始',
  `play_days` int(3) NULL DEFAULT 3 COMMENT '持续播放天数',
  `play_interval` int(5) NULL DEFAULT 30 COMMENT '播放间隔(分钟)',
  `status` tinyint(2) NULL DEFAULT 0 COMMENT '是否在线 1-是 0-否',
  `alarm_status` tinyint(2) NULL DEFAULT 0 COMMENT '是否报警状态 1-是 0-否',
  `flash_status` tinyint(2) NULL DEFAULT 0 COMMENT '在报警期是否一直闪灯 1-是 0-否',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_audible_alarm_id`(`audible_alarm_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '声光报警器表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for audible_alarm_device
-- ----------------------------
DROP TABLE IF EXISTS `audible_alarm_device`;
CREATE TABLE `audible_alarm_device`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `audible_alarm_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '声光报警器id',
  `device_imei` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备imei',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '声光报警器与设备关联表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for auth_client
-- ----------------------------
DROP TABLE IF EXISTS `auth_client`;
CREATE TABLE `auth_client`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '服务编码',
  `secret` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '服务密钥',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '服务�?',
  `locked` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '是否锁定',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建�?',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓�?',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新�?',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_code`(`code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_client_service
-- ----------------------------
DROP TABLE IF EXISTS `auth_client_service`;
CREATE TABLE `auth_client_service`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `client_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_time` datetime NULL DEFAULT NULL,
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_client_id`(`client_id`) USING BTREE,
  INDEX `idx_service_id`(`service_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 43 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for base_area
-- ----------------------------
DROP TABLE IF EXISTS `base_area`;
CREATE TABLE `base_area`  (
  `node_code` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '地址编码',
  `node_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '地区名称',
  `node_full_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '地区全称',
  `parent_code` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `node_initialisation` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '默认值(预留)',
  `node_spell` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '首字母',
  `node_type` decimal(2, 0) NOT NULL COMMENT '类型：1是省会，2直辖市,3港澳台,4其它',
  `node_order` decimal(3, 0) NOT NULL COMMENT '同级下排序',
  `node_level` decimal(2, 0) NOT NULL COMMENT '0全国、1省、2市区、3郊县、4街道、5居委会',
  `node_remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `village_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '城乡分类代码',
  `nation_name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所属国家名',
  `province_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所属省名称',
  `city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所属市名称',
  `county_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所属区县名称',
  `town_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所属街道名称',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `map_type` decimal(2, 0) NULL DEFAULT NULL COMMENT '来源地图，百度1,高德2',
  PRIMARY KEY (`node_code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '地区表(从统计局上抓取的数据 更新维护至2023-12-30)' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for base_element
-- ----------------------------
DROP TABLE IF EXISTS `base_element`;
CREATE TABLE `base_element`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源编码',
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源类型',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源名称',
  `uri` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源路径',
  `menu_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源关联菜单',
  `parent_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `path` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源树状检索路径',
  `method` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源请求类型',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `crt_time` datetime NULL DEFAULT NULL,
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 222 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for base_group
-- ----------------------------
DROP TABLE IF EXISTS `base_group`;
CREATE TABLE `base_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '部门编码',
  `identifier_code` char(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'GD0000000' COMMENT '组织标识编号',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '部门名称',
  `full_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `parent_id` int(11) NOT NULL COMMENT '上级节点',
  `path` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '树状关系',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_time` datetime NULL DEFAULT NULL,
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upd_time` datetime NULL DEFAULT NULL,
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `service_type` tinyint(2) NULL DEFAULT NULL COMMENT '服务类型',
  `extendable` tinyint(1) NOT NULL DEFAULT 1 COMMENT '节点类型',
  `introduce` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '背景介绍',
  `address` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '地址',
  `district` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '行政区',
  `entrust_company` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '委托单位',
  `entrust_contacts` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '委托单位联系人',
  `entrust_contacts_phone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '委托单位联系电话',
  `installation_company` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '安装单位',
  `installation_contacts` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '安装负责人',
  `installation_contacts_phone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '安装负责人联系电话',
  `building_code` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '房屋编码',
  `implement_company` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '实施单位',
  `config_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '应用场景类型',
  `report_type` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '报告类型',
  `annual_fee` decimal(8, 2) NULL DEFAULT NULL COMMENT '年费',
  `deadline` datetime NULL DEFAULT NULL COMMENT '截止时间',
  `arrears_reminder_time` int(11) NULL DEFAULT NULL COMMENT '欠费提示时间',
  `pic_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '监测点图片地址',
  `alarm_threshold_config` varbinary(15000) NULL DEFAULT NULL COMMENT '报警阈值',
  `report_template_type` tinyint(2) NULL DEFAULT 1 COMMENT '报告模板类型 1房屋 2边坡 3矿坑 4桥梁',
  `province_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '行政编码(省)',
  `city_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '行政编码(市)',
  `area_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '行政编码(区)',
  `action_alarm` tinyint(2) NULL DEFAULT NULL COMMENT '是否配置监测物报警联动',
  `three_to_two` tinyint(2) NULL DEFAULT NULL COMMENT '监测物三级升二级的个监测点个数',
  `two_to_one` tinyint(2) NULL DEFAULT NULL COMMENT '监测物二级升一升级的个监测点个数',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_name`(`name`) USING BTREE,
  INDEX `idx_identifier_code`(`identifier_code`) USING BTREE,
  INDEX `idx_path`(`path`(255)) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5016 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for base_menu
-- ----------------------------
DROP TABLE IF EXISTS `base_menu`;
CREATE TABLE `base_menu`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '路径编码',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '标题',
  `parent_id` int(11) NOT NULL COMMENT '父级节点',
  `href` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源路径',
  `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '图标',
  `type` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `order_num` int(11) NOT NULL DEFAULT 0 COMMENT '排序',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '菜单上下级关系',
  `enabled` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '启用禁用',
  `crt_time` datetime NULL DEFAULT NULL,
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upd_time` datetime NULL DEFAULT NULL,
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `component` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '组件名称',
  `component_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '名称路径',
  `meta` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 156 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for base_resource_authority
-- ----------------------------
DROP TABLE IF EXISTS `base_resource_authority`;
CREATE TABLE `base_resource_authority`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '角色ID',
  `resource_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源ID',
  `resource_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源类型',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19507 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for base_role
-- ----------------------------
DROP TABLE IF EXISTS `base_role`;
CREATE TABLE `base_role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(10) NOT NULL COMMENT '组织Id',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源编码',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源名称',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `crt_time` datetime NULL DEFAULT NULL,
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upd_time` datetime NULL DEFAULT NULL,
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 55 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for base_user
-- ----------------------------
DROP TABLE IF EXISTS `base_user`;
CREATE TABLE `base_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '账号',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户名称',
  `mobile_phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电话号码',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '状态',
  `group_id` int(11) NULL DEFAULT NULL COMMENT '所属组织',
  `open_id` varchar(127) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '微信用户id',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `location_auto_expand` tinyint(2) NULL DEFAULT NULL COMMENT '设备位置自动展开',
  `crt_time` datetime NULL DEFAULT NULL,
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upd_time` datetime NULL DEFAULT NULL,
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `login_time` datetime NULL DEFAULT NULL COMMENT '最新登录时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_username`(`username`) USING BTREE COMMENT '用户名唯一索引',
  INDEX `idx_group_id`(`group_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 852 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for base_user_role
-- ----------------------------
DROP TABLE IF EXISTS `base_user_role`;
CREATE TABLE `base_user_role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '已弃用' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for batch
-- ----------------------------
DROP TABLE IF EXISTS `batch`;
CREATE TABLE `batch`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `batch_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '批次号（bd+产品型号+硬件版本+生产日期）',
  `hard_version` int(10) NULL DEFAULT NULL COMMENT '硬件版本',
  `product_model` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '产品型号',
  `production_date` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '生产日期',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '批次号描述',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 48 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '批次号管理表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for common_config
-- ----------------------------
DROP TABLE IF EXISTS `common_config`;
CREATE TABLE `common_config`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `threshold` int(10) NOT NULL DEFAULT 0 COMMENT '报警阈值（默认0）',
  `push_interval` int(10) NOT NULL DEFAULT 10 COMMENT '推送间隔（默认10s）',
  `fall_standard` int(10) NOT NULL DEFAULT 50 COMMENT '跌落满分分数（默认50）',
  `lean_standard` int(10) NOT NULL DEFAULT 30 COMMENT '倾斜满分分数（默认30）',
  `loosen_standard` int(10) NOT NULL DEFAULT 10 COMMENT '松动满分分数（默认10）',
  `spin_standard` int(10) NOT NULL DEFAULT 10 COMMENT '旋转满分分数（默认10）',
  `lean_threshold` int(10) NOT NULL DEFAULT 10 COMMENT '倾斜角偏转角度（默认5）',
  `heading_degree_standard` int(10) NOT NULL DEFAULT 10 COMMENT '磁偏角偏转角度（默认10）',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '配置信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for constants_config
-- ----------------------------
DROP TABLE IF EXISTS `constants_config`;
CREATE TABLE `constants_config`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `group_id` int(10) NULL DEFAULT NULL COMMENT '组织Id',
  `config_key` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '配置键',
  `config_value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '配置值',
  `type` int(20) NULL DEFAULT NULL COMMENT '类型',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 438 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for consult_record
-- ----------------------------
DROP TABLE IF EXISTS `consult_record`;
CREATE TABLE `consult_record`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `consult_content` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '咨询内容',
  `phone_number` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系电话',
  `company_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '公司名称',
  `name` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `type` tinyint(2) NULL DEFAULT NULL COMMENT '类型',
  `mp_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '公众号id',
  `open_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户在公众号的唯一标识',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '公众号咨询记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for data_push_config
-- ----------------------------
DROP TABLE IF EXISTS `data_push_config`;
CREATE TABLE `data_push_config`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `group_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '组织Id',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '数据推送配置' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for deep_displacement_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `deep_displacement_packet_info`;
CREATE TABLE `deep_displacement_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `x_range_value` decimal(20, 2) NULL DEFAULT NULL COMMENT 'x位移变换量',
  `y_range_value` decimal(20, 2) NULL DEFAULT NULL COMMENT 'y位移变换量',
  `z_range_value` decimal(20, 2) NULL DEFAULT NULL COMMENT 'z位移变换量',
  `x_current_value` decimal(20, 2) NULL DEFAULT NULL COMMENT 'x位移当前值',
  `y_current_value` decimal(20, 2) NULL DEFAULT NULL COMMENT 'y位移当前值',
  `z_current_value` decimal(20, 2) NULL DEFAULT NULL COMMENT 'z位移当前值',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `x_angle` decimal(20, 2) NULL DEFAULT NULL COMMENT 'x角度值',
  `y_angle` decimal(20, 2) NULL DEFAULT NULL COMMENT 'y角度值',
  `z_angle` decimal(20, 2) NULL DEFAULT NULL COMMENT 'z角度值',
  `x_direction_angle` decimal(20, 2) NULL DEFAULT NULL COMMENT 'x方向偏转角',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_dis_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12231 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '深部位移上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_bind_record
-- ----------------------------
DROP TABLE IF EXISTS `device_bind_record`;
CREATE TABLE `device_bind_record`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `group_id` int(10) NOT NULL COMMENT '所属组织',
  `bind_time` datetime NOT NULL COMMENT '绑定时间',
  `un_bind_time` datetime NULL DEFAULT NULL COMMENT '解绑时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_group_imei_id`(`group_id`, `imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11986 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备-组织最新绑定关系' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_cmd_status
-- ----------------------------
DROP TABLE IF EXISTS `device_cmd_status`;
CREATE TABLE `device_cmd_status`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备号',
  `cmd_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '指令名称',
  `cmd_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '指令代码',
  `cmd_status` tinyint(1) NULL DEFAULT NULL COMMENT '指令状态（0-下发中 1-成功 2-失败 3-超时）',
  `cmd_crt_time` datetime NULL DEFAULT NULL COMMENT '指令创建时间',
  `resp_time` datetime NULL DEFAULT NULL COMMENT '设备响应时间',
  `cmd_send_time` datetime NULL DEFAULT NULL COMMENT '平台发送时间',
  `cmd_config` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '下发指令',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9284 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '指令状态表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_command
-- ----------------------------
DROP TABLE IF EXISTS `device_command`;
CREATE TABLE `device_command`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `command_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '指令名称',
  `command_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '指令编码',
  `resp_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '响应码',
  `command_version` int(10) NULL DEFAULT NULL COMMENT '指令版本',
  `command_type` tinyint(1) NULL DEFAULT NULL COMMENT '指令类型（1- 操作类；2-设置类；3-查询类）',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 59 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备指令表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for device_command_param
-- ----------------------------
DROP TABLE IF EXISTS `device_command_param`;
CREATE TABLE `device_command_param`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `command_id` int(10) NULL DEFAULT NULL COMMENT '指令id',
  `param_seq` int(10) NULL DEFAULT NULL COMMENT '参数序号',
  `param_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '参数名称',
  `param_type` tinyint(1) NULL DEFAULT NULL COMMENT '参数类型（1- 数值类；2- 字符类；3- 枚举类）',
  `default_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '默认值',
  `min_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '最小值',
  `max_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '最大值',
  `options_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '枚举值(举例：1-开机,2-关机,3-报警)',
  `param_unit` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '参数单位',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 41 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备指令参数表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for device_day_average_value
-- ----------------------------
DROP TABLE IF EXISTS `device_day_average_value`;
CREATE TABLE `device_day_average_value`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备号',
  `type` int(11) NULL DEFAULT NULL COMMENT '值的类型',
  `average_value` decimal(13, 6) NULL DEFAULT NULL COMMENT '平均值',
  `second_average_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第二个平均值',
  `degree` int(11) NULL DEFAULT NULL COMMENT '倾斜方向平均值',
  `report_date` date NOT NULL COMMENT '日期',
  `three_average_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第三个平均值',
  `four_average_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第四个平均值',
  `five_average_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第五个平均值',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_imei_type_date`(`imei`, `type`, `report_date`) USING BTREE,
  INDEX `idx_did_t_date`(`data_id`, `type`, `report_date`) USING BTREE,
  INDEX `idx_did_imei_t_date`(`data_id`, `imei`, `type`, `report_date`) USING BTREE,
  INDEX `idx_report_date`(`report_date`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 375695 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备日均值' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_day_variation_value
-- ----------------------------
DROP TABLE IF EXISTS `device_day_variation_value`;
CREATE TABLE `device_day_variation_value`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备号',
  `type` int(11) NULL DEFAULT NULL COMMENT '值的类型',
  `variation_value` decimal(9, 3) NOT NULL COMMENT '变化量',
  `second_variation_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第二个变化量',
  `report_date` date NOT NULL COMMENT '日期',
  `three_variation_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第三个变化量',
  `four_variation_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第四个变化量',
  `five_variation_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第五个变化量',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_imei_type_date`(`imei`, `type`, `report_date`) USING BTREE,
  INDEX `idx_did_t_date`(`data_id`, `type`, `report_date`) USING BTREE,
  INDEX `idx_did_imei_t_date`(`data_id`, `imei`, `type`, `report_date`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 150322 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备日变化量' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_extra_config
-- ----------------------------
DROP TABLE IF EXISTS `device_extra_config`;
CREATE TABLE `device_extra_config`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备号',
  `config_key` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '配置项',
  `config_value` decimal(40, 10) NULL DEFAULT NULL COMMENT '配置数值',
  `type` int(20) NULL DEFAULT NULL COMMENT '类型（0 - 旋转配置项 1 - 倾斜配置项 2 - 旋转基准值 3 - 倾斜基准值）',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_imei_type_key`(`imei`, `type`, `config_key`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 407721 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备额外配置表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for device_extra_config_rollback
-- ----------------------------
DROP TABLE IF EXISTS `device_extra_config_rollback`;
CREATE TABLE `device_extra_config_rollback`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备号',
  `config_key` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '配置项',
  `config_value` decimal(40, 10) NULL DEFAULT NULL COMMENT '配置数值',
  `type` int(20) NULL DEFAULT NULL COMMENT '类型（0 - 旋转配置项 1 - 倾斜配置项 2 - 旋转基准值 3 - 倾斜基准值）',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `start_time` datetime NULL DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime NULL DEFAULT NULL COMMENT '结束时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_start_end`(`imei`, `start_time`, `end_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2359094 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备额外配置回退表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for device_extra_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `device_extra_packet_info`;
CREATE TABLE `device_extra_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `low_power` tinyint(2) NULL DEFAULT 0 COMMENT '是否低电 1是 0否',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei`(`imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1758905 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备额外信息上报记录(如是否低电)' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_extra_platform_code_relation
-- ----------------------------
DROP TABLE IF EXISTS `device_extra_platform_code_relation`;
CREATE TABLE `device_extra_platform_code_relation`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `platform_type` tinyint(2) NOT NULL COMMENT '外接平台类型',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `device_type` int(11) NOT NULL COMMENT '设备类型',
  `extra_platform_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '外接平台编码',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_pt_imei_dt`(`platform_type`, `imei`, `device_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 195 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备号-外接平台唯一编码关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_info
-- ----------------------------
DROP TABLE IF EXISTS `device_info`;
CREATE TABLE `device_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `device_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备名称',
  `info_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '设备类型',
  `use_case` int(10) NULL DEFAULT 0 COMMENT '设备类型（之后将替换device_type）',
  `device_type` int(10) NULL DEFAULT NULL COMMENT '应用场景',
  `batch` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '批次号',
  `hard_version` int(10) NULL DEFAULT NULL COMMENT '硬件版本（冗余批次号，便于检索）',
  `group_id` int(10) NOT NULL COMMENT '所属组织',
  `address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '地址',
  `logistics_status` tinyint(1) NULL DEFAULT NULL COMMENT '物流状态(0-库存、1-出库)',
  `install_status` tinyint(1) NULL DEFAULT NULL COMMENT '安装状态(安装状态: 0-生产 1-库存 2-未激活 3-已激活 4-停用 5-维修 6-报废)',
  `running_status` tinyint(1) NULL DEFAULT NULL COMMENT '运行状态(运行状态(0-正常、1-报警、2-恢复、3-拆除))',
  `algorithm_id` int(11) NULL DEFAULT NULL COMMENT '算法Id',
  `virtual_device` tinyint(1) NULL DEFAULT 0 COMMENT '真实/虚拟设备(0-真实设备、1-虚拟设备)',
  `unofficial_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '关联的其他平台设备编号',
  `basic_config` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '基本配置项（以后考虑通用，将专属设备的字段该字段JSON表示）',
  `extra_config` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '额外配置项（如：报警阈值配置项）',
  `rtk_suppliers_type` tinyint(2) NULL DEFAULT NULL COMMENT 'rtk设备供应商类型',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `sphere_center_x` decimal(10, 5) NULL DEFAULT NULL COMMENT '球心x轴坐标',
  `sphere_center_y` decimal(10, 5) NULL DEFAULT NULL COMMENT '球心y轴坐标',
  `sphere_center_z` decimal(10, 5) NULL DEFAULT NULL COMMENT '球心z轴坐标',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  `height` decimal(6, 2) NULL DEFAULT NULL COMMENT '高度',
  `monitoring_direction` tinyint(2) NULL DEFAULT 1 COMMENT '监测方向 1-全向 2-横向 3-纵向',
  `height_visible` tinyint(4) NULL DEFAULT 1 COMMENT '高度显示：0：否 1：是',
  `direction_type` tinyint(2) NULL DEFAULT 0 COMMENT '安装方式 0-无方向要求 1-有方向要求',
  `direction_value` decimal(10, 4) NULL DEFAULT 0.0000 COMMENT '监测物朝向值',
  `slope_meter_config` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '深部测斜仪配置(地址步长深度)',
  `temperature_module` tinyint(2) NULL DEFAULT 0 COMMENT '表面应变计是否有温度模块 1-是 0-否',
  `depth` decimal(10, 2) NULL DEFAULT 0.00 COMMENT '深度(m)',
  `repair_start_time` datetime NULL DEFAULT NULL COMMENT '维修开始时间',
  `repair_end_time` datetime NULL DEFAULT NULL COMMENT '维修结束时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_imei`(`imei`) USING BTREE,
  INDEX `idx_group_id_imei`(`group_id`, `imei`) USING BTREE,
  INDEX `idx_install_status_repair_end_time`(`install_status`, `repair_end_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14566 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for device_monitor_data_id_relation
-- ----------------------------
DROP TABLE IF EXISTS `device_monitor_data_id_relation`;
CREATE TABLE `device_monitor_data_id_relation`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备号',
  `identifier_code` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '组织标识编号',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_imei_data_identifier_code`(`imei`, `data_id`, `identifier_code`) USING BTREE,
  INDEX `idx_identifier_code_data`(`identifier_code`, `data_id`) USING BTREE,
  INDEX `idx_data_imei`(`data_id`, `imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5312 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备-组织-数据标识关系表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_month_average_value
-- ----------------------------
DROP TABLE IF EXISTS `device_month_average_value`;
CREATE TABLE `device_month_average_value`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备号',
  `type` int(11) NULL DEFAULT NULL COMMENT '值的类型',
  `average_value` decimal(9, 3) NOT NULL COMMENT '平均值',
  `second_average_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第二个平均值',
  `degree` int(11) NULL DEFAULT NULL COMMENT '倾斜方向平均值',
  `report_date` date NOT NULL COMMENT '日期',
  `three_average_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第三个平均值',
  `four_average_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第四个平均值',
  `five_average_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第五个平均值',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_imei_type_date`(`imei`, `type`, `report_date`) USING BTREE,
  INDEX `idx_did_t_date`(`data_id`, `type`, `report_date`) USING BTREE,
  INDEX `idx_did_imei_t_date`(`data_id`, `imei`, `type`, `report_date`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23889 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备月均值' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_month_variation_value
-- ----------------------------
DROP TABLE IF EXISTS `device_month_variation_value`;
CREATE TABLE `device_month_variation_value`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备号',
  `type` int(11) NULL DEFAULT NULL COMMENT '值的类型',
  `variation_value` decimal(9, 3) NOT NULL COMMENT '变化量',
  `second_variation_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第二个变化量',
  `report_date` date NOT NULL COMMENT '日期',
  `three_variation_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第三个变化量',
  `four_variation_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第四个变化量',
  `five_variation_value` decimal(9, 3) NULL DEFAULT NULL COMMENT '第五个变化量',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_imei_type_date`(`imei`, `type`, `report_date`) USING BTREE,
  INDEX `idx_did_t_date`(`data_id`, `type`, `report_date`) USING BTREE,
  INDEX `idx_did_imei_t_date`(`data_id`, `imei`, `type`, `report_date`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15860 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备月变化量' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_other_info
-- ----------------------------
DROP TABLE IF EXISTS `device_other_info`;
CREATE TABLE `device_other_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '数据id',
  `imei` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '组织id',
  `acquire_location` tinyint(4) NOT NULL DEFAULT 1 COMMENT '是否能获取定位 0：否  1：是',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  `crt_user` int(11) NULL DEFAULT NULL COMMENT '操作人ID',
  `upt_user` int(11) NULL DEFAULT NULL COMMENT '更新人id',
  `upt_time` datetime NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `device_other_info_imei_index`(`imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备其它信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_repair_record
-- ----------------------------
DROP TABLE IF EXISTS `device_repair_record`;
CREATE TABLE `device_repair_record`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备号',
  `description` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '描述',
  `repair_start_time` datetime NULL DEFAULT NULL COMMENT '维修开始时间',
  `repair_end_time` datetime NULL DEFAULT NULL COMMENT '维修结束时间',
  `crt_time` datetime NOT NULL COMMENT '创建时间',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '修改时间',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 571 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备维修记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_replace_record
-- ----------------------------
DROP TABLE IF EXISTS `device_replace_record`;
CREATE TABLE `device_replace_record`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `old_imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '旧设备号',
  `new_imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '新设备号',
  `group_id` int(10) NOT NULL COMMENT '所属组织',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '替换时间',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '替换人',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 56 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备替换记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_replace_relation
-- ----------------------------
DROP TABLE IF EXISTS `device_replace_relation`;
CREATE TABLE `device_replace_relation`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `old_imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '旧设备号',
  `new_imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '新设备号',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `new_imei`(`new_imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备替换关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_status
-- ----------------------------
DROP TABLE IF EXISTS `device_status`;
CREATE TABLE `device_status`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备号',
  `frequency_status` tinyint(1) NULL DEFAULT NULL COMMENT '是否频繁上报',
  `frequency_detail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '频繁上报详情',
  `frequency_moment` datetime NULL DEFAULT NULL COMMENT '频繁上报执行时间',
  `timeout_status` tinyint(1) NULL DEFAULT NULL COMMENT '是否超时上报',
  `timeout_detail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '超时上报详情',
  `timeout_moment` datetime NULL DEFAULT NULL COMMENT '超时执行时间',
  `final_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'frequency or timeout：冗余状态，不再进行判断后得出',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_imei`(`imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2883 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备状态表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for device_status_change_record
-- ----------------------------
DROP TABLE IF EXISTS `device_status_change_record`;
CREATE TABLE `device_status_change_record`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备号',
  `status` tinyint(1) NOT NULL COMMENT '设备状态',
  `change_time` datetime NOT NULL COMMENT '修改日期',
  `has_rollback_data` tinyint(1) NULL DEFAULT 0 COMMENT '是否有存回退的数据',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1680 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备状态变更记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for device_value_renovate_record
-- ----------------------------
DROP TABLE IF EXISTS `device_value_renovate_record`;
CREATE TABLE `device_value_renovate_record`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `renovate_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '翻新类型',
  `renovate_param` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '翻新参数',
  `renovate_status` tinyint(1) NOT NULL COMMENT '翻新状态',
  `renovate_time` datetime NOT NULL COMMENT '翻新时间',
  `renovate_user` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '翻新人',
  `complete_time` datetime NULL DEFAULT NULL COMMENT '完成时间 ',
  `fail_msg` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '失败原因 ',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1835 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备上报数据翻新记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for displacement_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `displacement_packet_info`;
CREATE TABLE `displacement_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `length` int(10) NULL DEFAULT NULL COMMENT '位移长度',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `range_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '位移变换量',
  `current_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '位移当前值',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `final_range_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '最终变化量',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_dis_time_value`(`imei`, `data_status`, `create_time`, `final_range_value`) USING BTREE,
  INDEX `idx_dis_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11385 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '位移上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for dtu_device
-- ----------------------------
DROP TABLE IF EXISTS `dtu_device`;
CREATE TABLE `dtu_device`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(10) NULL DEFAULT NULL COMMENT '组织Id',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_imei`(`imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 195 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'dtu设备表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for dtu_extra_device_relation
-- ----------------------------
DROP TABLE IF EXISTS `dtu_extra_device_relation`;
CREATE TABLE `dtu_extra_device_relation`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'dtu的imei',
  `extra_imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '外接传感器imei',
  `relation_type` tinyint(4) NOT NULL COMMENT '关联类型',
  `baseline_imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '基准外接传感器imei',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_extra_imei`(`extra_imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7828 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'dtu和外接传感器关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for earth_pressure_meter_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `earth_pressure_meter_packet_info`;
CREATE TABLE `earth_pressure_meter_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `temperature` decimal(5, 2) NULL DEFAULT NULL COMMENT '温度',
  `battery_level` bigint(10) NULL DEFAULT NULL COMMENT '电池电量',
  `strain_range_value` decimal(20, 7) NULL DEFAULT NULL COMMENT '应变变化量',
  `strain_current_value` decimal(20, 7) NULL DEFAULT NULL COMMENT '应变当前值',
  `strain_init_value` decimal(20, 7) NULL DEFAULT NULL COMMENT '应变初始值',
  `strain_frequency_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '上报的频率',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_status`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1122993819336585217 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '土压力计上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for extra_device_info
-- ----------------------------
DROP TABLE IF EXISTS `extra_device_info`;
CREATE TABLE `extra_device_info`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `type` tinyint(1) NOT NULL COMMENT '传感器类型',
  `address` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '传感器地址',
  `customer` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '客户',
  `device_factory` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备厂家',
  `delivery_date` date NULL DEFAULT NULL COMMENT '交付日期',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 65 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '外接设备信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for extra_platform_code_mapping
-- ----------------------------
DROP TABLE IF EXISTS `extra_platform_code_mapping`;
CREATE TABLE `extra_platform_code_mapping`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `platform_type` tinyint(2) NOT NULL COMMENT '外接平台类型',
  `device_type` int(11) NOT NULL COMMENT '设备类型',
  `monitor_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '监测项编码',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_pt_dt_mc`(`platform_type`, `device_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '外接平台监测项编码映射' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for extra_platform_info
-- ----------------------------
DROP TABLE IF EXISTS `extra_platform_info`;
CREATE TABLE `extra_platform_info`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `platform_type` tinyint(2) NOT NULL COMMENT '外接平台类型',
  `platform_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '外接平台名称',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_platform_type`(`platform_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '外接平台信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for fee_config
-- ----------------------------
DROP TABLE IF EXISTS `fee_config`;
CREATE TABLE `fee_config`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备IMEI',
  `annual_fee` decimal(8, 2) NULL DEFAULT NULL COMMENT '年费',
  `deadline` datetime NULL DEFAULT NULL COMMENT '截止时间',
  `arrears_reminder_time` int(11) NULL DEFAULT NULL COMMENT '欠费提示时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_imei`(`imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2166 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '费用配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for fee_imei
-- ----------------------------
DROP TABLE IF EXISTS `fee_imei`;
CREATE TABLE `fee_imei`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `batch` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '批次号',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备号',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_batch_imei`(`batch`, `imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '费用批次与设备绑定' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for file_record
-- ----------------------------
DROP TABLE IF EXISTS `file_record`;
CREATE TABLE `file_record`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(10) NOT NULL COMMENT '操作组织',
  `file_type` tinyint(2) NULL DEFAULT NULL COMMENT '文件类型',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '预下载时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人账号',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件路径',
  `complete_time` datetime NULL DEFAULT NULL COMMENT '完成时间',
  `remark` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `generate_status` tinyint(1) NULL DEFAULT NULL COMMENT '生成状态',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8027 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '文件下载记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for gap_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `gap_packet_info`;
CREATE TABLE `gap_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `gap_range_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '裂缝变换量',
  `gap_current_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '裂缝当前值',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `final_range_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '最终变化量',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_gap_time_value`(`imei`, `data_status`, `create_time`, `final_range_value`) USING BTREE,
  INDEX `idx_gap_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1123184488344727553 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '裂缝上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for gate_log
-- ----------------------------
DROP TABLE IF EXISTS `gate_log`;
CREATE TABLE `gate_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '序号',
  `menu` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '菜单',
  `opt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作',
  `uri` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '资源路径',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '操作时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人ID',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作主机',
  `body` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `request_uri` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '请求路径',
  `token_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '会话编号',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1441509 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for gb_license
-- ----------------------------
DROP TABLE IF EXISTS `gb_license`;
CREATE TABLE `gb_license`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '组织Id',
  `count` int(11) NULL DEFAULT NULL COMMENT '接入监控数',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '国标通道申请' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for gb_license_monitor
-- ----------------------------
DROP TABLE IF EXISTS `gb_license_monitor`;
CREATE TABLE `gb_license_monitor`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `license_id` int(11) NOT NULL COMMENT 'license_id',
  `device_serial` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '分配设备编号',
  `status` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否接入',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_device_serial`(`device_serial`) USING BTREE,
  INDEX `idx_license_id`(`license_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 149 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '国标通道分配设备编码' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for gb_monitor
-- ----------------------------
DROP TABLE IF EXISTS `gb_monitor`;
CREATE TABLE `gb_monitor`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '所属组织',
  `banner_weight` int(11) NULL DEFAULT NULL COMMENT '首页播放权重',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备名称',
  `device_serial` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备编号',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  `online` tinyint(2) NULL DEFAULT 0 COMMENT '0不在线，1为在线',
  `schedule_snap` tinyint(2) NULL DEFAULT 0 COMMENT '定时抓拍，0否，1为是',
  `is_alarm` tinyint(2) NULL DEFAULT 0 COMMENT '报警布防，0撤防，1为布防',
  `iot_card` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '物联网卡卡号',
  `activate_time` datetime NULL DEFAULT NULL COMMENT '启用时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_group_id`(`group_id`) USING BTREE,
  INDEX `idx_device_serial`(`device_serial`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 73 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '国标监控设备表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for gradienter_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `gradienter_packet_info`;
CREATE TABLE `gradienter_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `gradienter_current_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '当前值',
  `gradienter_diff_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '液位差',
  `gradienter_range_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '沉降量',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `be_supplementary` tinyint(1) NULL DEFAULT -1 COMMENT '是否补传数据',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_dst_time_value`(`imei`, `data_status`, `create_time`, `gradienter_range_value`) USING BTREE,
  INDEX `idx_gra_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12278 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '水准仪上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_alarm
-- ----------------------------
DROP TABLE IF EXISTS `group_alarm`;
CREATE TABLE `group_alarm`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '组织Id',
  `alarm_status` tinyint(1) NULL DEFAULT NULL COMMENT '报警处理状态',
  `alarm_result` tinyint(1) NULL DEFAULT NULL COMMENT '处理结果/设备状态',
  `charge_man` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '负责人',
  `charge_phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电话号码',
  `predict_complete_time` datetime NULL DEFAULT NULL COMMENT '预计完成时间',
  `real_complete_time` datetime NULL DEFAULT NULL COMMENT '完成时间',
  `total_alarm_type_number` int(50) NULL DEFAULT NULL COMMENT '总报警类型',
  `alarm_type_number` int(50) NULL DEFAULT NULL COMMENT '报警类型',
  `day_alarm_type_number` int(50) NULL DEFAULT NULL COMMENT '日变化报警类型',
  `month_alarm_type_number` int(50) NULL DEFAULT NULL COMMENT '月变化报警类型',
  `total_alarm_desc` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '总报警描述',
  `alarm_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '报警细节描述',
  `day_alarm_desc` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '日变化报警描述',
  `month_alarm_desc` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '月变化报警描述',
  `alarm_level` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '报警等级json',
  `group_alarm_level` tinyint(2) NULL DEFAULT NULL COMMENT '设备报警等级',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `handle_type` tinyint(2) NULL DEFAULT NULL COMMENT '处理类型',
  `fall_index` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `swing_index` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `lean_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '倾斜报警值',
  `distance_x_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '三角位移报警值',
  `distance_y_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '三角沉降报警值',
  `gap_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '裂缝报警值',
  `water_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '水位报警值',
  `gradienter_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '水准仪沉降报警值',
  `displacement_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '位移报警值',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `day_average_alarm_type_number` int(50) NULL DEFAULT NULL COMMENT '日均报警类型',
  `day_average_alarm_desc` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '日均报警描述',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 164 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '监测物报警表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_fee_config
-- ----------------------------
DROP TABLE IF EXISTS `group_fee_config`;
CREATE TABLE `group_fee_config`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `batch` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '批次号',
  `group_id` int(11) NOT NULL COMMENT '组织Id',
  `annual_fee` decimal(8, 2) NULL DEFAULT NULL COMMENT '年费',
  `deadline` datetime NULL DEFAULT NULL COMMENT '截止时间',
  `arrears_reminder_time` int(11) NULL DEFAULT NULL COMMENT '欠费提示时间',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_batch`(`batch`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 178 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '组织费用配置' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_judgment_user_sms
-- ----------------------------
DROP TABLE IF EXISTS `group_judgment_user_sms`;
CREATE TABLE `group_judgment_user_sms`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '组织Id',
  `user_id` int(11) NOT NULL COMMENT '用户id',
  `template_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '1' COMMENT '模板id',
  `function_type` tinyint(2) NULL DEFAULT 1 COMMENT '功能类型 1-短信 2-语音',
  `delete_flag` tinyint(4) NULL DEFAULT 1 COMMENT '是否删除  -1：已删除  1：未删除',
  `crt_user` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `upt_user` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_group_id`(`group_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 616 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '组织研判用户短信接收关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_monitor_data_id_relation
-- ----------------------------
DROP TABLE IF EXISTS `group_monitor_data_id_relation`;
CREATE TABLE `group_monitor_data_id_relation`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(10) NOT NULL COMMENT '祖先组织',
  `identifier_code` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '组织标识编号',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据标识',
  `be_current` tinyint(2) NOT NULL COMMENT '是否当前值',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_group_identifier_code_data`(`group_id`, `identifier_code`, `data_id`) USING BTREE,
  INDEX `idx_group_be_current`(`group_id`, `be_current`) USING BTREE,
  INDEX `idx_data_id`(`data_id`) USING BTREE,
  INDEX `idx_identifier_code`(`identifier_code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14077 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '组织-组织-数据标识关系表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_mp
-- ----------------------------
DROP TABLE IF EXISTS `group_mp`;
CREATE TABLE `group_mp`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '组织Id',
  `mp_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '公众号Id',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `group_mp_id_idx`(`group_id`) USING BTREE COMMENT '组织唯一索引',
  UNIQUE INDEX `idx_u_mp_group_id`(`group_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '组织公众号关系表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_relation
-- ----------------------------
DROP TABLE IF EXISTS `group_relation`;
CREATE TABLE `group_relation`  (
  `ancestor` int(11) NOT NULL,
  `descendant` int(11) NOT NULL,
  PRIMARY KEY (`ancestor`, `descendant`) USING BTREE,
  INDEX `idx1`(`ancestor`) USING BTREE,
  INDEX `idx2`(`descendant`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '组织关系表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_sms
-- ----------------------------
DROP TABLE IF EXISTS `group_sms`;
CREATE TABLE `group_sms`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '组织Id',
  `sms_info_id` int(11) NOT NULL COMMENT '短信服务id',
  `function_type` tinyint(2) NULL DEFAULT 1 COMMENT '功能类型 1-短信 2-语音',
  `voice_status` tinyint(2) NULL DEFAULT NULL COMMENT '状态 1 开启禁语音时间段 0关闭',
  `ban_start_time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '禁止语音拨打开始时间',
  `ban_end_time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '禁止语音拨打结束时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_u_sms_group_id`(`group_id`, `function_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 61 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '组织短信服务关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_user_mp
-- ----------------------------
DROP TABLE IF EXISTS `group_user_mp`;
CREATE TABLE `group_user_mp`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '组织Id',
  `user_id` int(50) NOT NULL COMMENT '用户id',
  `alarm_level` tinyint(4) NOT NULL DEFAULT 3 COMMENT '报警等级',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_u_gu`(`group_id`, `user_id`, `alarm_level`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '组织用户公众号接收关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for group_user_record
-- ----------------------------
DROP TABLE IF EXISTS `group_user_record`;
CREATE TABLE `group_user_record`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `group_id` bigint(50) NULL DEFAULT NULL COMMENT '组织id',
  `user_id` bigint(50) NULL DEFAULT NULL COMMENT '用户id',
  `status` tinyint(1) NULL DEFAULT NULL COMMENT '状态：0 待审核 1 审核通过 2 审核不通过',
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '来源',
  `enabled` tinyint(1) NULL DEFAULT NULL COMMENT '启用状态 0 不启用 1 启用',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 71 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '组织用户记录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for group_user_role
-- ----------------------------
DROP TABLE IF EXISTS `group_user_role`;
CREATE TABLE `group_user_role`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `group_id` bigint(50) NULL DEFAULT NULL COMMENT '组织id',
  `user_id` bigint(50) NULL DEFAULT NULL COMMENT '用户id',
  `role_id` bigint(50) NULL DEFAULT NULL COMMENT '角色id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3972 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '组织用户角色关系表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for group_user_sms
-- ----------------------------
DROP TABLE IF EXISTS `group_user_sms`;
CREATE TABLE `group_user_sms`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '组织Id',
  `user_id` int(11) NOT NULL COMMENT '用户id',
  `alarm_level` tinyint(4) NOT NULL DEFAULT 3 COMMENT '报警等级',
  `alarm_type` tinyint(4) NULL DEFAULT 1 COMMENT '预警短信模板类型',
  `function_type` tinyint(2) NULL DEFAULT 1 COMMENT '功能类型 1-短信 2-语音',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_u_sms`(`group_id`, `user_id`, `alarm_level`, `function_type`, `alarm_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 258 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '组织用户短信接收关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for history_identifier_code
-- ----------------------------
DROP TABLE IF EXISTS `history_identifier_code`;
CREATE TABLE `history_identifier_code`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `identifier_code` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '组织标识编号',
  `group_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '组织名称',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_code`(`identifier_code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3486 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '历史组织标识编号' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for initial_angle_rollback
-- ----------------------------
DROP TABLE IF EXISTS `initial_angle_rollback`;
CREATE TABLE `initial_angle_rollback`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备号',
  `initial_config` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `start_time` datetime NULL DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime NULL DEFAULT NULL COMMENT '结束时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei__start_end`(`imei`, `start_time`, `end_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1070 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备初始redis回退表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for inspection_task_info
-- ----------------------------
DROP TABLE IF EXISTS `inspection_task_info`;
CREATE TABLE `inspection_task_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '数据id',
  `group_id` int(11) NULL DEFAULT NULL COMMENT '组织id',
  `user_id` int(11) NOT NULL COMMENT '巡检人员id',
  `quartz_corn_id` int(11) NULL DEFAULT NULL COMMENT '巡检配置id',
  `task_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '巡检任务名称',
  `task_type` tinyint(4) NOT NULL DEFAULT 0 COMMENT '任务类型 0：常规  1：临时',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `job_status` int(10) NULL DEFAULT 0 COMMENT '状态 -1：已删除 0：未开始 1：已开始 200：完成',
  `execution_start_time` datetime NULL DEFAULT NULL COMMENT '任务开始时间',
  `execution_end_time` datetime NULL DEFAULT NULL COMMENT '任务结束时间',
  `crt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人ID',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人',
  `upt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `inspection_task_info_groupId_index`(`group_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13462 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '巡检任务' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for inspection_task_user_relation
-- ----------------------------
DROP TABLE IF EXISTS `inspection_task_user_relation`;
CREATE TABLE `inspection_task_user_relation`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '数据id',
  `quartz_corn_id` int(11) NOT NULL COMMENT '巡检配置id',
  `user_id` int(11) NOT NULL COMMENT '巡检人员id',
  `monitoring_point_id` int(11) NOT NULL COMMENT '巡检人员负责巡检的组织id(监测点id)',
  `delete_flag` tinyint(4) NOT NULL DEFAULT 1 COMMENT '是否已删除：-1已删除  1未删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `inspection_task_user_relation_task_id`(`quartz_corn_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11435 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '巡检人员，巡检点（监测点）关系表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for inspection_user_task_finish
-- ----------------------------
DROP TABLE IF EXISTS `inspection_user_task_finish`;
CREATE TABLE `inspection_user_task_finish`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT 'Id',
  `quartz_corn_id` int(11) NULL DEFAULT NULL COMMENT '巡检配置id',
  `task_id` bigint(50) NULL DEFAULT NULL COMMENT '巡检任务id',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '巡检人员id',
  `monitoring_point_id` int(11) NOT NULL COMMENT '监测点id',
  `user_task_status` int(10) NULL DEFAULT NULL COMMENT '人员巡检任务状态 0：未完成 200：已完成',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `delete_flag` tinyint(4) NULL DEFAULT 1 COMMENT '是否删除 -1：删除  0：未删除',
  `crt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  `crt_user` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人ID',
  `upt_user` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `inspection_user_task_finish_task_id`(`task_id`) USING BTREE,
  INDEX `idx_crt_time`(`crt_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 229478 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '巡检人员任务完成表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for installation_record
-- ----------------------------
DROP TABLE IF EXISTS `installation_record`;
CREATE TABLE `installation_record`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备IMEI',
  `installer` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '安装人员',
  `installer_phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '安装人员电话号码',
  `site` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '安装地点',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 94 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '安装记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for installation_record_picture
-- ----------------------------
DROP TABLE IF EXISTS `installation_record_picture`;
CREATE TABLE `installation_record_picture`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `installation_record_id` bigint(50) NULL DEFAULT NULL COMMENT '安裝记录id',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备号',
  `pic_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '图片地址',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 259 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '现场设备环境照片' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for latest_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `latest_packet_info`;
CREATE TABLE `latest_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_imei_unique`(`imei`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1119672893798887425 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '最新报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for licensed_group_extra_platform
-- ----------------------------
DROP TABLE IF EXISTS `licensed_group_extra_platform`;
CREATE TABLE `licensed_group_extra_platform`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `platform_type` tinyint(2) NOT NULL COMMENT '外接平台类型',
  `licensed_group_id` int(11) NOT NULL COMMENT '被授权组织Id',
  `push_group` tinyint(2) NULL DEFAULT 1 COMMENT '是否按组组织推送1是0否',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_ep_licensed_id`(`platform_type`, `licensed_group_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1240 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '外接平台和被授权组织关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for licensed_group_mp
-- ----------------------------
DROP TABLE IF EXISTS `licensed_group_mp`;
CREATE TABLE `licensed_group_mp`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `mp_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '公众号Id',
  `licensed_group_id` int(11) NOT NULL COMMENT '被授权组织Id',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_mp_licensed_id`(`mp_id`, `licensed_group_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1924 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '公众号和被授权组织关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for licensed_group_sms
-- ----------------------------
DROP TABLE IF EXISTS `licensed_group_sms`;
CREATE TABLE `licensed_group_sms`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `sms_info_id` int(11) NOT NULL COMMENT '短信服务id',
  `licensed_group_id` int(11) NOT NULL COMMENT '被授权组织Id',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_mp_licensed_id`(`sms_info_id`, `licensed_group_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4269 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '短信和被授权组织关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for location_rectify
-- ----------------------------
DROP TABLE IF EXISTS `location_rectify`;
CREATE TABLE `location_rectify`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备号',
  `latitude` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '维度',
  `longitude` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '经度',
  `real_coord` tinyint(1) NULL DEFAULT NULL COMMENT '是否不需要转换坐标',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `location_time` datetime NULL DEFAULT NULL COMMENT '定位时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei`(`imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 909 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '定位矫正表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for machine_device
-- ----------------------------
DROP TABLE IF EXISTS `machine_device`;
CREATE TABLE `machine_device`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `machine_id` bigint(50) NULL DEFAULT NULL COMMENT '唯一标识id',
  `device_id` bigint(50) NULL DEFAULT NULL COMMENT '设备id',
  `device_config` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备配置（用于算法计算时的配置）',
  `imei` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余实体设备的imei，减小查询量',
  `algorithm_id` int(11) NULL DEFAULT NULL COMMENT '算法id',
  `group_id` int(50) NULL DEFAULT NULL COMMENT '所属组织',
  `status` tinyint(4) NULL DEFAULT NULL COMMENT '状态',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_machine_id`(`machine_id`) USING BTREE,
  INDEX `idx_imei`(`imei`) USING BTREE,
  INDEX `idx_algorithm_id`(`algorithm_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14170 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '机器-设备中间表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for machine_info
-- ----------------------------
DROP TABLE IF EXISTS `machine_info`;
CREATE TABLE `machine_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `algorithm_id` int(11) NULL DEFAULT NULL COMMENT '算法id',
  `device_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备名称',
  `device_type` int(10) NULL DEFAULT NULL COMMENT '设备类型(0-倾角仪 1-裂缝仪 2-位移监测仪 3-沉降仪)',
  `use_case` int(10) NULL DEFAULT NULL COMMENT '应用场景(0-射灯广告牌 1-单立柱广告牌 2-大型灯箱 3-候车厅广告牌 4-霓虹灯广告牌)',
  `group_id` int(10) NOT NULL COMMENT '所属组织',
  `install_status` tinyint(1) NULL DEFAULT 0 COMMENT '安装状态(0-未激活、1-已激活)',
  `running_status` tinyint(1) NULL DEFAULT 0 COMMENT '运行状态(运行状态(0-正常、1-报警、2-恢复、3-拆除)',
  `virtual_device` tinyint(1) NULL DEFAULT 0 COMMENT '安装状态(0-真实设备、1-虚拟设备)',
  `basic_config` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '基本配置项',
  `extra_config` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '额外配置项',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei`(`imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备总表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for monitor
-- ----------------------------
DROP TABLE IF EXISTS `monitor`;
CREATE TABLE `monitor`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `monitor_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '监控设备名称',
  `group_id` int(10) NULL DEFAULT NULL COMMENT '所属组织',
  `device_serial` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备序列号',
  `validate_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备验证码',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 177 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '监控设备表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for monitor_alarm
-- ----------------------------
DROP TABLE IF EXISTS `monitor_alarm`;
CREATE TABLE `monitor_alarm`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `device_serial` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备编号',
  `alarm_status` tinyint(1) NULL DEFAULT NULL COMMENT '报警处理状态（未处理、处理中、已处理）',
  `alarm_result` tinyint(1) NULL DEFAULT NULL COMMENT '处理结果/设备状态（正常、修复、报警、拆除）',
  `charge_man` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '负责人',
  `charge_phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电话号码',
  `alarm_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '报警细节描述',
  `pic_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '图片地址',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `alarm_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `handle_time` datetime NULL DEFAULT NULL COMMENT '处理时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1002 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '监控报警表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for monitor_device
-- ----------------------------
DROP TABLE IF EXISTS `monitor_device`;
CREATE TABLE `monitor_device`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `monitor_id` bigint(50) NULL DEFAULT NULL COMMENT '监控id',
  `device_id` bigint(50) NULL DEFAULT NULL COMMENT '设备id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 856 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '监控-设备中间表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for monitor_snap_job
-- ----------------------------
DROP TABLE IF EXISTS `monitor_snap_job`;
CREATE TABLE `monitor_snap_job`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `device_serial` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备编号',
  `job_id` int(10) NOT NULL COMMENT '定时任务的id',
  `schedule_hour` int(11) NULL DEFAULT NULL COMMENT '定时抓拍的时',
  `schedule_minute` int(11) NULL DEFAULT NULL COMMENT '定时抓拍的分',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_device_job`(`device_serial`, `job_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '监控定时抓拍配置表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for monitor_snap_record
-- ----------------------------
DROP TABLE IF EXISTS `monitor_snap_record`;
CREATE TABLE `monitor_snap_record`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `device_serial` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备编号',
  `pic_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '图片地址',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '监控定时抓拍记录' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for monitor_type_relation
-- ----------------------------
DROP TABLE IF EXISTS `monitor_type_relation`;
CREATE TABLE `monitor_type_relation`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `identifier_code` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '组织标识编号',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备号',
  `monitory_type` int(11) NOT NULL COMMENT '监测类型',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_imei_code_type`(`identifier_code`, `imei`, `monitory_type`) USING BTREE,
  INDEX `idx_imei`(`imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20393 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '监测点-设备-监测类型关联关系表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mqtt_config
-- ----------------------------
DROP TABLE IF EXISTS `mqtt_config`;
CREATE TABLE `mqtt_config`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'mqtt名称',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码',
  `host` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '地址',
  `client_id` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '客户端id',
  `topic` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '主题',
  `type` tinyint(1) NOT NULL COMMENT 'mqtt类型',
  `push_type` tinyint(1) NULL DEFAULT 1 COMMENT '推送类型:1:MQTT推送,2:http推送',
  `token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'http推送的token',
  `url` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '推送url',
  `json_type` tinyint(1) NULL DEFAULT NULL COMMENT '是否使用通用的JSON返回:1:是,0:否',
  `enabled` tinyint(1) NULL DEFAULT 1 COMMENT '是否启用; 0 禁用; 1 启用',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 101 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'mqtt配置' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for operation_latest_record
-- ----------------------------
DROP TABLE IF EXISTS `operation_latest_record`;
CREATE TABLE `operation_latest_record`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备号',
  `head` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '报文头',
  `version` int(10) NULL DEFAULT NULL COMMENT '版本',
  `command_type` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '指令类型',
  `command_param` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '指令参数',
  `origin_packet` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '完整报文',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_c_h_time`(`imei`, `command_type`, `head`, `crt_time`) USING BTREE,
  INDEX `idx_time_type`(`crt_time`, `command_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3606 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备操作指令最新记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for operation_log
-- ----------------------------
DROP TABLE IF EXISTS `operation_log`;
CREATE TABLE `operation_log`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '操作人所属组织',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '用户id',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '操作时间',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人账号',
  `opt_result` tinyint(1) NULL DEFAULT NULL COMMENT '操作结果（成功，失败）',
  `opt_type` int(11) NULL DEFAULT NULL COMMENT '操作类型',
  `opt_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '操作内容',
  `opt_object` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作对象',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 52465 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '操作日志' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for operation_log_2025_1
-- ----------------------------
DROP TABLE IF EXISTS `operation_log_2025_1`;
CREATE TABLE `operation_log_2025_1`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '操作人所属组织',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '用户id',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '操作时间',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人账号',
  `opt_result` tinyint(1) NULL DEFAULT NULL COMMENT '操作结果（成功，失败）',
  `opt_type` int(11) NULL DEFAULT NULL COMMENT '操作类型',
  `opt_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '操作内容',
  `opt_object` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作对象',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 91 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '操作日志' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for operation_log_2025_2
-- ----------------------------
DROP TABLE IF EXISTS `operation_log_2025_2`;
CREATE TABLE `operation_log_2025_2`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '操作人所属组织',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '用户id',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '操作时间',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人账号',
  `opt_result` tinyint(1) NULL DEFAULT NULL COMMENT '操作结果（成功，失败）',
  `opt_type` int(11) NULL DEFAULT NULL COMMENT '操作类型',
  `opt_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '操作内容',
  `opt_object` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作对象',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22008 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '操作日志' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for operation_log_2025_3
-- ----------------------------
DROP TABLE IF EXISTS `operation_log_2025_3`;
CREATE TABLE `operation_log_2025_3`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '操作人所属组织',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '用户id',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '操作时间',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人账号',
  `opt_result` tinyint(1) NULL DEFAULT NULL COMMENT '操作结果（成功，失败）',
  `opt_type` int(11) NULL DEFAULT NULL COMMENT '操作类型',
  `opt_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '操作内容',
  `opt_object` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作对象',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 57 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '操作日志' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for operation_record
-- ----------------------------
DROP TABLE IF EXISTS `operation_record`;
CREATE TABLE `operation_record`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备号',
  `head` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '报文头',
  `version` int(10) NULL DEFAULT NULL COMMENT '版本',
  `command_type` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '指令类型',
  `command_param` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '指令参数',
  `origin_packet` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '完整报文',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_c_h_time`(`imei`, `command_type`, `head`, `crt_time`) USING BTREE,
  INDEX `idx_time_type`(`crt_time`, `command_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 224441 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备操作指令记录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for packet_info
-- ----------------------------
DROP TABLE IF EXISTS `packet_info`;
CREATE TABLE `packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1117198893667594241 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for packet_info_2025_1
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_2025_1`;
CREATE TABLE `packet_info_2025_1`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1117189852581081089 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for packet_info_2025_10
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_2025_10`;
CREATE TABLE `packet_info_2025_10`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1117198504025141249 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for packet_info_2025_11
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_2025_11`;
CREATE TABLE `packet_info_2025_11`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1123291065290600449 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for packet_info_2025_12
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_2025_12`;
CREATE TABLE `packet_info_2025_12`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for packet_info_2025_2
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_2025_2`;
CREATE TABLE `packet_info_2025_2`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1117193293923627009 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for packet_info_2025_3
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_2025_3`;
CREATE TABLE `packet_info_2025_3`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1117197506439294977 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for packet_info_2025_4
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_2025_4`;
CREATE TABLE `packet_info_2025_4`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1117198658736238593 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for packet_info_2025_5
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_2025_5`;
CREATE TABLE `packet_info_2025_5`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1117193895428763649 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for packet_info_2025_6
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_2025_6`;
CREATE TABLE `packet_info_2025_6`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1117810587829809153 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for packet_info_2025_7
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_2025_7`;
CREATE TABLE `packet_info_2025_7`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1120708054573395969 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for packet_info_2025_8
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_2025_8`;
CREATE TABLE `packet_info_2025_8`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1123209348676595713 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for packet_info_2025_9
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_2025_9`;
CREATE TABLE `packet_info_2025_9`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `tmp1` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段1',
  `tmp2` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段2',
  `tmp3` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预留字段3',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1117198136855769089 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for packet_info_temp
-- ----------------------------
DROP TABLE IF EXISTS `packet_info_temp`;
CREATE TABLE `packet_info_temp`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `protocol` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '协议版本',
  `protocol_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电池电量',
  `temperature` decimal(20, 2) NULL DEFAULT NULL COMMENT '温度',
  `info_length` int(10) NULL DEFAULT NULL COMMENT '字节的长度',
  `drop_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '跌落报警',
  `lean_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '倾斜报警',
  `slope_move_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '斜率运动报警',
  `wake_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '唤醒中断',
  `swing_alarm` tinyint(1) NULL DEFAULT NULL COMMENT '摇摆报警',
  `charging` tinyint(1) NULL DEFAULT NULL COMMENT '设备是否充电',
  `stock_button` tinyint(1) NULL DEFAULT NULL COMMENT '库存按键按下',
  `operate_status` tinyint(1) NULL DEFAULT NULL COMMENT '运营状态',
  `hex_base_rep_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '16进制上报类型',
  `base_rep_type_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上报类型描述',
  `dec_base_rep_type` int(10) NULL DEFAULT NULL COMMENT '10进制上报类型',
  `cpreshs_tilt` decimal(5, 2) NULL DEFAULT NULL COMMENT '综合倾角',
  `retain_str` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '保留字段',
  `signal_value` int(10) NULL DEFAULT NULL COMMENT '通讯信息强度',
  `antenna_elevation` int(10) NULL DEFAULT NULL COMMENT '定位稳定信号字段',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `roll` decimal(5, 2) NULL DEFAULT NULL COMMENT '滚动角/倾斜角',
  `pitch` decimal(5, 2) NULL DEFAULT NULL COMMENT '俯仰角',
  `yaw` decimal(5, 2) NULL DEFAULT NULL COMMENT '偏航角',
  `ax` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ax',
  `ay` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据ay',
  `az` int(20) NULL DEFAULT NULL COMMENT '重力加速度数据az',
  `gx` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gx',
  `gy` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gy',
  `gz` int(20) NULL DEFAULT NULL COMMENT '陀螺仪数据gz',
  `mx` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mx',
  `my` int(20) NULL DEFAULT NULL COMMENT '磁力计数据my',
  `mz` int(20) NULL DEFAULT NULL COMMENT '磁力计数据mz',
  `sx` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sx',
  `sy` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sy',
  `sz` int(20) NULL DEFAULT NULL COMMENT '摇摆数据sz',
  `srx` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度x轴',
  `sry` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度y轴',
  `srz` int(20) NULL DEFAULT NULL COMMENT '摇摆幅度z轴',
  `dx` int(20) NULL DEFAULT NULL COMMENT '位移数据dx',
  `dy` int(20) NULL DEFAULT NULL COMMENT '位移数据dy',
  `dz` int(20) NULL DEFAULT NULL COMMENT '位移数据dz',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `heading_degrees` decimal(5, 2) NULL DEFAULT NULL COMMENT '磁偏角',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `lean_degrees` decimal(7, 4) NULL DEFAULT NULL COMMENT '倾斜角',
  `degree` decimal(5, 2) NULL DEFAULT NULL COMMENT '方向(单位为度数)',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `slp_wkp_times` int(20) NULL DEFAULT NULL COMMENT '休眠唤醒次数',
  `gap_length` int(10) NULL DEFAULT NULL COMMENT '裂缝长度',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei`(`imei`) USING BTREE,
  INDEX `idx_imei_time_lat_log`(`imei`, `latitude`, `longitude`, `create_time`) USING BTREE,
  INDEX `idx_imei_dst_time_ld`(`imei`, `data_status`, `create_time`, `lean_degrees`) USING BTREE,
  INDEX `idx_imei_time`(`imei`, `create_time`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21327866 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for page_customization
-- ----------------------------
DROP TABLE IF EXISTS `page_customization`;
CREATE TABLE `page_customization`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `group_id` int(11) NULL DEFAULT NULL COMMENT '所属组织',
  `type` tinyint(2) NULL DEFAULT NULL COMMENT '类型',
  `field_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'json文件的属性名称',
  `field_value` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'json文件的属性值',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1640 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '页面定制化表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for people_testing_info
-- ----------------------------
DROP TABLE IF EXISTS `people_testing_info`;
CREATE TABLE `people_testing_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '数据id',
  `group_id` int(11) NOT NULL COMMENT '组织id',
  `remark` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `delete_flag` tinyint(1) NULL DEFAULT 1 COMMENT '是否删除 -1：删除  1：未删除',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '手机号码',
  `charge_user` int(11) NULL DEFAULT NULL COMMENT '处理人',
  `charge_remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '处理意见',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_group_id`(`group_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 39 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '群测群防信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for permanent_staff_mp
-- ----------------------------
DROP TABLE IF EXISTS `permanent_staff_mp`;
CREATE TABLE `permanent_staff_mp`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `name` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '姓名',
  `type` tinyint(2) NULL DEFAULT NULL COMMENT '类型',
  `mp_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '公众号id',
  `open_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户在公众号的唯一标识',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '公众号固定人员' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for platform_version
-- ----------------------------
DROP TABLE IF EXISTS `platform_version`;
CREATE TABLE `platform_version`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `type` tinyint(1) NULL DEFAULT NULL COMMENT '类型（0-平台 1-小程序）',
  `major` int(10) NULL DEFAULT NULL COMMENT '主版本号',
  `minor` int(10) NULL DEFAULT NULL COMMENT '次版本号',
  `patch` int(10) NULL DEFAULT NULL COMMENT '修订号',
  `version` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '版本号x.x.x',
  `detail` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '版本详情',
  `attachment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '附件存放路径（url）',
  `publish_time` datetime NULL DEFAULT NULL COMMENT '发布时间',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '平台版本表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for production_test_info
-- ----------------------------
DROP TABLE IF EXISTS `production_test_info`;
CREATE TABLE `production_test_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `battery_voltage` decimal(10, 2) NULL DEFAULT NULL COMMENT '电池电压',
  `battery_percentage` decimal(5, 2) NULL DEFAULT NULL COMMENT '电量百分比',
  `sensor_address` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '传感器地址',
  `battery_value` decimal(10, 2) NULL DEFAULT NULL COMMENT '传感器数值',
  `accelerometer_test` tinyint(1) NULL DEFAULT NULL COMMENT '加速度传感器读写测试',
  `beidou_power_on_test` tinyint(1) NULL DEFAULT NULL COMMENT '北斗定位模组上电测试',
  `beidou_location_test` tinyint(1) NULL DEFAULT NULL COMMENT '北斗定位获取测试',
  `cat1_power_on_test` tinyint(1) NULL DEFAULT NULL COMMENT 'CAT1模组上电测试',
  `cat1_network_test` tinyint(1) NULL DEFAULT NULL COMMENT 'CAT1联网测试',
  `switch_detection` tinyint(1) NULL DEFAULT NULL COMMENT '开关量检测',
  `communication_interface_485_test` tinyint(1) NULL DEFAULT NULL COMMENT '通信接口485测试',
  `sensor_interrupt_pin_test` tinyint(1) NULL DEFAULT NULL COMMENT '传感器中断管脚测试',
  `lora_power_on_test` tinyint(1) NULL DEFAULT NULL COMMENT 'LORA模组上电测试',
  `lora_communication_test` tinyint(1) NULL DEFAULT NULL COMMENT 'LORA模组通讯测试',
  `all_test` tinyint(1) NULL DEFAULT 0 COMMENT '是否全部测试通过 1是 0否',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time`(`imei`, `create_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '生产监测信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for push_data_full
-- ----------------------------
DROP TABLE IF EXISTS `push_data_full`;
CREATE TABLE `push_data_full`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `attribute_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '属性中文名称',
  `attribute_value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '属性英文名称',
  `attribute_type` tinyint(2) NULL DEFAULT NULL COMMENT '属性类型',
  `attribute_type_value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '属性类型名称',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '推送数据全量表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for push_data_option
-- ----------------------------
DROP TABLE IF EXISTS `push_data_option`;
CREATE TABLE `push_data_option`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `access_system_id` int(11) NULL DEFAULT NULL COMMENT '接入系统id',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备号',
  `attribute_values` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '选择的属性名称',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `agd`(`access_system_id`, `imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2321 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '推送数据选项表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for push_record
-- ----------------------------
DROP TABLE IF EXISTS `push_record`;
CREATE TABLE `push_record`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `access_system_id` int(11) NULL DEFAULT NULL COMMENT '接入系统id',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备号',
  `push_method` tinyint(2) NULL DEFAULT NULL COMMENT '推送方式',
  `push_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '推送内容',
  `push_result` tinyint(2) NULL DEFAULT NULL COMMENT '推送结果; -1失败 ; 1 成功',
  `push_time` datetime NULL DEFAULT NULL COMMENT '推送时间',
  `response_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '响应内容',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1639 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '推送记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for quartz_cron_info
-- ----------------------------
DROP TABLE IF EXISTS `quartz_cron_info`;
CREATE TABLE `quartz_cron_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '数据id',
  `group_id` int(11) NULL DEFAULT NULL COMMENT '组织id',
  `user_id` int(11) NOT NULL COMMENT '巡检人员',
  `task_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务名称',
  `bean_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'bean名称',
  `method_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方法名称',
  `method_params` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方法参数',
  `cron_expression` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'cron表达式',
  `cron_expression_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'cron表达式周期',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `job_status` tinyint(4) NULL DEFAULT 1 COMMENT '状态  0：禁用  1：启用',
  `crt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人ID',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人',
  `upt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `quartz_cron_info_groupId_index`(`group_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 317 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '定时任务表达式' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for quartz_cron_info_param
-- ----------------------------
DROP TABLE IF EXISTS `quartz_cron_info_param`;
CREATE TABLE `quartz_cron_info_param`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '数据id',
  `quartz_corn_id` int(11) NOT NULL COMMENT '配置任务cron数据id',
  `quartz_corn_param` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '配置巡检任务生成json参数',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `quartz_cron_info_param_cron_id`(`quartz_corn_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 642 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '巡检任务配置参数' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for rainfall_day_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `rainfall_day_packet_info`;
CREATE TABLE `rainfall_day_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `rainfall` decimal(20, 2) NULL DEFAULT NULL COMMENT '雨量',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_status`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 84 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '雨量计每天记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for rainfall_hour_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `rainfall_hour_packet_info`;
CREATE TABLE `rainfall_hour_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `rainfall` decimal(20, 2) NULL DEFAULT NULL COMMENT '雨量',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_status`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1006 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '雨量计每小时记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for rainfall_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `rainfall_packet_info`;
CREATE TABLE `rainfall_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `temperature` decimal(5, 2) NULL DEFAULT NULL COMMENT '温度',
  `battery_level` bigint(10) NULL DEFAULT NULL COMMENT '电池电量',
  `rainfall` decimal(20, 2) NULL DEFAULT NULL COMMENT '雨量（计算后的数据）',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `raw_data` decimal(20, 2) NULL DEFAULT NULL COMMENT '设备上报数据',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_status`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1117887178920439809 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '雨量计上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for rebar_strain_gauge_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `rebar_strain_gauge_packet_info`;
CREATE TABLE `rebar_strain_gauge_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `strain_range_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '应变变换量',
  `strain_current_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '应变当前值',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `strain_init_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '应变初始值',
  `strain_frequency_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '上报的频率',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_status`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 786 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '钢筋应变计上报记录' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for rebar_stress_meter_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `rebar_stress_meter_packet_info`;
CREATE TABLE `rebar_stress_meter_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `stress_range_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '应力变化量',
  `stress_current_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '应力当前值',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `stress_init_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '应力初始值',
  `stress_frequency_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '上报的频率',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_status`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 692 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '钢筋应力上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for record_detail
-- ----------------------------
DROP TABLE IF EXISTS `record_detail`;
CREATE TABLE `record_detail`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `record_id` bigint(50) NULL DEFAULT NULL COMMENT '升级记录Id',
  `current_packet_no` int(10) NULL DEFAULT NULL COMMENT '当前包号',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 110879 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '升级记录详情表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for report_push_config
-- ----------------------------
DROP TABLE IF EXISTS `report_push_config`;
CREATE TABLE `report_push_config`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '组织',
  `period_type` tinyint(2) NULL DEFAULT NULL COMMENT '周期类型',
  `time_content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '具体推送时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报告公众号推送配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for report_push_person_config
-- ----------------------------
DROP TABLE IF EXISTS `report_push_person_config`;
CREATE TABLE `report_push_person_config`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '组织',
  `mounts_id` int(11) NOT NULL COMMENT '需要生成报告的安装物',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1626 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报告公众号推送组织配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for result_record
-- ----------------------------
DROP TABLE IF EXISTS `result_record`;
CREATE TABLE `result_record`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `result` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '计算结果',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备IMEI',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `machine_id` bigint(50) NULL DEFAULT NULL COMMENT 'machine_device表唯一标识id',
  `result_type` int(50) NULL DEFAULT NULL COMMENT '结果类型',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_machine_id_time_status`(`machine_id`, `crt_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `crt_time`, `data_status`) USING BTREE,
  INDEX `idx_did_mid_time_ds`(`data_id`, `machine_id`, `crt_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4825104 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '结果记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for result_record_copy1
-- ----------------------------
DROP TABLE IF EXISTS `result_record_copy1`;
CREATE TABLE `result_record_copy1`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `result` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '计算结果',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备IMEI',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `machine_id` bigint(50) NULL DEFAULT NULL COMMENT 'machine_device表唯一标识id',
  `result_type` int(50) NULL DEFAULT NULL COMMENT '结果类型',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_machine_id_dst_crt_time`(`machine_id`, `data_status`, `crt_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 149673 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '结果记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for result_record_rollback
-- ----------------------------
DROP TABLE IF EXISTS `result_record_rollback`;
CREATE TABLE `result_record_rollback`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `result` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '计算结果',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备IMEI',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `machine_id` bigint(50) NULL DEFAULT NULL COMMENT 'machine_device表唯一标识id',
  `result_type` int(50) NULL DEFAULT NULL COMMENT '结果类型 1定时打卡 2非定时打',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `azimuth` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '方位角',
  `start_time` datetime NULL DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime NULL DEFAULT NULL COMMENT '结束时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei__start_end`(`imei`, `start_time`, `end_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3509182 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '位移等结果记录表(数据回退用)' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for rtk_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `rtk_packet_info`;
CREATE TABLE `rtk_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `gx` decimal(20, 2) NULL DEFAULT NULL,
  `gy` decimal(20, 2) NULL DEFAULT NULL,
  `gz` decimal(20, 2) NULL DEFAULT NULL,
  `displacement` decimal(20, 2) NULL DEFAULT NULL COMMENT '位移',
  `subside` decimal(20, 2) NULL DEFAULT NULL COMMENT '沉降',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1123291383780880385 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'rtk上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sim_device_info
-- ----------------------------
DROP TABLE IF EXISTS `sim_device_info`;
CREATE TABLE `sim_device_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `iccid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '物联网卡',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'imei',
  `use_amount` decimal(10, 2) NULL DEFAULT NULL COMMENT '使用量',
  `remark` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_imei`(`imei`) USING BTREE,
  UNIQUE INDEX `udx_iccid_imei`(`iccid`, `imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2124 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'sim卡信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for single_day_variation
-- ----------------------------
DROP TABLE IF EXISTS `single_day_variation`;
CREATE TABLE `single_day_variation`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `report_date` date NOT NULL COMMENT '上报日期',
  `variation` decimal(9, 3) NOT NULL COMMENT '变换量',
  `type` tinyint(2) NOT NULL COMMENT '类型',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 347100 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备单日变化量表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for slope_meter_average_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `slope_meter_average_packet_info`;
CREATE TABLE `slope_meter_average_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `type` int(2) NULL DEFAULT 1 COMMENT '平均类型 1-日平均值',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `slope_meter_x_original` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪x原始值',
  `slope_meter_y_original` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪y原始值',
  `slope_meter_com_angle_original` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪综合原始值',
  `slope_meter_x` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪x值',
  `slope_meter_y` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪y值',
  `slope_meter_com_angle` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪综合值',
  `slope_meter_x_total` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪总x值',
  `slope_meter_y_total` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪总y值',
  `slope_meter_com_angle_total` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪总综合值',
  `temperature` decimal(5, 2) NULL DEFAULT NULL COMMENT '温度',
  `battery_level` bigint(10) NULL DEFAULT NULL COMMENT '电池电量',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_status`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 180 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '深部测斜仪平均值记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for slope_meter_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `slope_meter_packet_info`;
CREATE TABLE `slope_meter_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `temperature` decimal(5, 2) NULL DEFAULT NULL COMMENT '温度',
  `battery_level` bigint(10) NULL DEFAULT NULL COMMENT '电池电量',
  `slope_meter_x_original` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪x原始值',
  `slope_meter_y_original` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪y原始值',
  `slope_meter_x` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪x值',
  `slope_meter_y` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪y值',
  `slope_meter_com_angle` decimal(10, 4) NULL DEFAULT 0.0000 COMMENT '深部测斜仪综合倾角',
  `slope_meter_x_total` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪总x值',
  `slope_meter_y_total` decimal(10, 4) NULL DEFAULT NULL COMMENT '深部测斜仪总y值',
  `slope_meter_com_angle_total` decimal(10, 4) NULL DEFAULT 0.0000 COMMENT '深部测斜仪总综合倾角',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_status`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1122945296855478274 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '深部测斜仪上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sms_info
-- ----------------------------
DROP TABLE IF EXISTS `sms_info`;
CREATE TABLE `sms_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sms_type` tinyint(2) NOT NULL COMMENT '短信平台类型',
  `sign_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '签名',
  `secret_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `secret_key` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `sdk_appId` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `owner_group_id` int(11) NOT NULL COMMENT '所有权组织Id',
  `function_type` tinyint(2) NULL DEFAULT 1 COMMENT '功能类型 1-短信 2-语音',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '短信服务信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sms_push_info
-- ----------------------------
DROP TABLE IF EXISTS `sms_push_info`;
CREATE TABLE `sms_push_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '数据id',
  `group_id` int(11) NULL DEFAULT NULL COMMENT '组织id',
  `sms_platform_id` int(11) NOT NULL COMMENT '短信平台id',
  `alarm_type` tinyint(4) NOT NULL COMMENT '短信类型 0：气象预警 1：地质灾害 2：边坡预警',
  `alarm_level` tinyint(4) NOT NULL COMMENT '预警等级 1：一级 2：二级 3：三级 4：四级',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `delete_flag` tinyint(4) NULL DEFAULT 0 COMMENT '删除 -1：已删除 1：未删除',
  `crt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人',
  `upt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sms_push_info_groupId_index`(`group_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '短信接收配置' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sms_push_user_relation
-- ----------------------------
DROP TABLE IF EXISTS `sms_push_user_relation`;
CREATE TABLE `sms_push_user_relation`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '数据id',
  `business_id` int(11) NULL DEFAULT NULL COMMENT '关联数据id',
  `business_type` int(11) NULL DEFAULT 1 COMMENT '业务类型 1：短信发送配置 ',
  `user_id` int(11) NOT NULL COMMENT '接收人员id',
  `delete_flag` tinyint(4) NULL DEFAULT 1 COMMENT '删除 -1：已删除 1：未删除',
  `crt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人',
  `upt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sms_user_relation_index_business_all`(`business_id`, `business_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '短信接收人' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sms_template
-- ----------------------------
DROP TABLE IF EXISTS `sms_template`;
CREATE TABLE `sms_template`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `template_type` tinyint(2) NOT NULL COMMENT '模板类型',
  `template_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '模板id',
  `sms_info_id` int(11) NOT NULL COMMENT '短信服务id',
  `voice_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '语音号码',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_sms_type`(`sms_info_id`, `template_type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '短信模板' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sms_user
-- ----------------------------
DROP TABLE IF EXISTS `sms_user`;
CREATE TABLE `sms_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL COMMENT '组织Id',
  `name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '手机号',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 439 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '短信用户' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for soil_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `soil_packet_info`;
CREATE TABLE `soil_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `temperature` decimal(5, 2) NULL DEFAULT NULL COMMENT '温度',
  `battery_level` bigint(10) NULL DEFAULT NULL COMMENT '电池电量',
  `soil_water_rate` decimal(10, 1) NULL DEFAULT NULL COMMENT '土壤含水率',
  `soil_temperature` decimal(10, 1) NULL DEFAULT NULL COMMENT '土壤温度',
  `soil_electric_rate` decimal(10, 1) NULL DEFAULT NULL COMMENT '土壤导电率',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_status`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5221 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '土壤计上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for split_table_info
-- ----------------------------
DROP TABLE IF EXISTS `split_table_info`;
CREATE TABLE `split_table_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `table_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '表名',
  `start_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `end_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `type` int(2) NULL DEFAULT 0 COMMENT '类型 0-倾角拆表(用设备的类型)',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_start_time_end_time`(`start_time`, `end_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '拆表信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for statistics_user
-- ----------------------------
DROP TABLE IF EXISTS `statistics_user`;
CREATE TABLE `statistics_user`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `group_id` int(50) NULL DEFAULT NULL COMMENT '组织id',
  `statistics_user_id` int(50) NULL DEFAULT NULL COMMENT '报表接受人员',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '报表人员处理表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for surface_strain_gauge_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `surface_strain_gauge_packet_info`;
CREATE TABLE `surface_strain_gauge_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `temperature` decimal(5, 2) NULL DEFAULT NULL COMMENT '温度',
  `battery_level` bigint(10) NULL DEFAULT NULL COMMENT '电池电量',
  `strain_range_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '应变变化量',
  `strain_current_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '应变当前值',
  `strain_init_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '应变初始值',
  `strain_frequency_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '上报的频率',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_status`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9311 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '表面应变计上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sys_file_info
-- ----------------------------
DROP TABLE IF EXISTS `sys_file_info`;
CREATE TABLE `sys_file_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT 'Id',
  `business_id` bigint(50) NULL DEFAULT NULL COMMENT '业务数据id',
  `file_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文件名称',
  `type` tinyint(4) NULL DEFAULT NULL COMMENT '类型',
  `external_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '外网地址',
  `intranet_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '内网地址',
  `file_suffix` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件后缀',
  `bucket_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '腾讯云文件key',
  `delete_flag` tinyint(4) NULL DEFAULT 1 COMMENT '是否删除 -1:已删除 1：未删除',
  `crt_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人ID',
  `upt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upt_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sys_file_info_index_business_id`(`business_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1122982137268809729 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for system_config
-- ----------------------------
DROP TABLE IF EXISTS `system_config`;
CREATE TABLE `system_config`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `group_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '组织Id',
  `schedule_time` int(10) NULL DEFAULT NULL COMMENT '定时执行周期时间',
  `low_power` int(20) NULL DEFAULT NULL COMMENT '低电量报警阈值',
  `long_time_charge` int(20) NULL DEFAULT NULL COMMENT '长时间未充电报警阈值',
  `low_recovery_power_report_gap` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '低电量打卡间隔恢复电量设置（示例：50,1440,90）',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 164 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '系统配置表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for temperature_humidity_in_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `temperature_humidity_in_packet_info`;
CREATE TABLE `temperature_humidity_in_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `temperature` decimal(5, 1) NULL DEFAULT NULL COMMENT '温度',
  `humidity` decimal(5, 1) NULL DEFAULT NULL COMMENT '湿度',
  `battery_level` bigint(10) NULL DEFAULT NULL COMMENT '电池电量',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `temperature_self` decimal(5, 2) NULL DEFAULT NULL COMMENT '温度(g02)',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1123291065445789697 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '温湿度(内置)仪上报信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for temperature_humidity_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `temperature_humidity_packet_info`;
CREATE TABLE `temperature_humidity_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `temperature` decimal(5, 1) NULL DEFAULT NULL COMMENT '温度',
  `humidity` decimal(5, 1) NULL DEFAULT NULL COMMENT '湿度',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `be_supplementary` tinyint(1) NULL DEFAULT -1 COMMENT '是否补传数据',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14809 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '温湿度仪器上报信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for template_mp
-- ----------------------------
DROP TABLE IF EXISTS `template_mp`;
CREATE TABLE `template_mp`  (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `template_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '模板id(对应微信平台模板库)',
  `mp_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '微信Id(对应mp中id)',
  `type` int(10) NOT NULL COMMENT '模板类型',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '模板名称',
  `mini_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '小程序Id',
  `mini_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '小程序调整路径',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_mp_type`(`mp_id`, `type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '公众号模板表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for trouble_record
-- ----------------------------
DROP TABLE IF EXISTS `trouble_record`;
CREATE TABLE `trouble_record`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `trouble_desc` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '问题描述',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备IMEI',
  `status` tinyint(2) NULL DEFAULT NULL COMMENT '问题状态 0未处理 1处理中 2已处理',
  `charge_man` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '负责人',
  `charge_phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电话号码',
  `handle_content` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '处理详情',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `type` tinyint(2) NULL DEFAULT NULL COMMENT '故障类型',
  `trouble_type_number` bigint(50) NULL DEFAULT NULL COMMENT '故障类型10进制表示',
  `exception_message_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备故障异常信息枚举类下标，多个用英文逗号隔开',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time`(`imei`, `crt_time`) USING BTREE,
  INDEX `idx_did_time`(`data_id`, `crt_time`) USING BTREE,
  INDEX `idx_did_imei_time`(`data_id`, `imei`, `crt_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14324 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '故障记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for trouble_record_relation
-- ----------------------------
DROP TABLE IF EXISTS `trouble_record_relation`;
CREATE TABLE `trouble_record_relation`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `relate_id` int(11) NOT NULL COMMENT '故障记录Id',
  `type` tinyint(2) NOT NULL COMMENT '故障类型 1低电量 2打卡超时',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_relate_id_type`(`relate_id`, `type`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13435 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '故障记录关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for trouble_threshold
-- ----------------------------
DROP TABLE IF EXISTS `trouble_threshold`;
CREATE TABLE `trouble_threshold`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `enabled_config` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '启用的配置项',
  `low_power_threshold` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '低电量故障阈值',
  `frequency_threshold` int(5) NULL DEFAULT NULL COMMENT '频繁上报报警阈值',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_imei`(`imei`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12243 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '设备故障阈值配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for unofficial_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `unofficial_packet_info`;
CREATE TABLE `unofficial_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `latitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '纬度',
  `longitude` decimal(20, 10) NULL DEFAULT NULL COMMENT '经度',
  `battery_level` int(10) NULL DEFAULT NULL COMMENT '电量',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time`(`imei`, `create_time`) USING BTREE,
  INDEX `idx_did_time`(`data_id`, `create_time`) USING BTREE,
  INDEX `idx_did_imei_time`(`data_id`, `imei`, `create_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1123291404936949761 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '非官方简略上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for upgrade_record
-- ----------------------------
DROP TABLE IF EXISTS `upgrade_record`;
CREATE TABLE `upgrade_record`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `task_id` bigint(50) NULL DEFAULT NULL COMMENT '升级任务Id',
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备号',
  `previous_version` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '升级前版本',
  `current_version` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '升级后版本',
  `upgrade_status` tinyint(1) NULL DEFAULT NULL COMMENT '升级状态（0-待升级、1-升级中、2-下载完成、3-升级成功、4-未知、5-升级失败）',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1446 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '升级记录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for upgrade_task
-- ----------------------------
DROP TABLE IF EXISTS `upgrade_task`;
CREATE TABLE `upgrade_task`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `upgrader_id` bigint(50) NULL DEFAULT NULL COMMENT '升级包Id',
  `imeis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '设备号（通过逗号隔开）',
  `upgrade_type` tinyint(1) NULL DEFAULT NULL COMMENT '升级状态',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 909 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '升级任务表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for upgrader
-- ----------------------------
DROP TABLE IF EXISTS `upgrader`;
CREATE TABLE `upgrader`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `publish_date` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '发布日期',
  `soft_version` int(10) NULL DEFAULT NULL COMMENT '软件版本',
  `hard_version` int(10) NULL DEFAULT NULL COMMENT '硬件版本',
  `product_modal` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '产品型号',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '存放地址',
  `filename` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件名称',
  `file_type` tinyint(1) NULL DEFAULT NULL COMMENT '文件类型（0 - 通用类型 1-专属类型）',
  `group_id` int(10) NULL DEFAULT NULL COMMENT '所属层级（默认当前登录用户所在层级；也可以选择其下子层级）',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '升级包描述',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 857 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '软件版本管理表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user_mp
-- ----------------------------
DROP TABLE IF EXISTS `user_mp`;
CREATE TABLE `user_mp`  (
  `id` int(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int(50) NOT NULL COMMENT '用户id',
  `mp_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '该公众号的微信号',
  `open_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户在微信号的唯一标识',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '微信公众号表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user_theme_relation
-- ----------------------------
DROP TABLE IF EXISTS `user_theme_relation`;
CREATE TABLE `user_theme_relation`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '序号',
  `user_id` int(11) NOT NULL COMMENT '用户id',
  `theme` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '系统样式',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '操作时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人ID',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人',
  `upt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upt_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for version_announcement
-- ----------------------------
DROP TABLE IF EXISTS `version_announcement`;
CREATE TABLE `version_announcement`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `version_no` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '版本号',
  `version_content` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '版本内容',
  `publish_time` datetime NULL DEFAULT NULL COMMENT '版本发布时间',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作人ID',
  `upt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upt_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `type` tinyint(2) NULL DEFAULT NULL COMMENT '客户端类型  0：web 1：app',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_version_no`(`version_no`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '版本公告' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for vibration_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `vibration_packet_info`;
CREATE TABLE `vibration_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `battery_level` bigint(10) NULL DEFAULT NULL COMMENT '电池电量',
  `fqx` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '频率x轴',
  `fqy` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '频率y轴',
  `fqz` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '频率z轴',
  `sspx` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '速度(peak)x轴',
  `sspy` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '速度(peak)y轴',
  `sspz` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '速度(peak)z轴',
  `sppx` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '速度(p-p)x轴',
  `sppy` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '速度(p-p)y轴',
  `sppz` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '速度(p-p)z轴',
  `srmsx` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '速度(rms)x轴',
  `srmsy` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '速度(rms)y轴',
  `srmsz` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '速度(rms)z轴',
  `dspx` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '振幅值(peak)x轴',
  `dspy` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '振幅值(peak)y轴',
  `dspz` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '振幅值(peak)z轴',
  `dppx` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '振幅值(p-p)x轴',
  `dppy` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '振幅值(p-p)y轴',
  `dppz` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '振幅值(p-p)z轴',
  `drmsx` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '振幅值(rms)x轴',
  `drmsy` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '振幅值(rms)y轴',
  `drmsz` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '振幅值(rms)z轴',
  `aspx` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '加速度(peak)x轴',
  `aspy` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '加速度(peak)y轴',
  `aspz` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '加速度(peak)z轴',
  `appx` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '加速度(p-p)x轴',
  `appy` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '加速度(p-p)y轴',
  `appz` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '加速度(p-p)z轴',
  `armsx` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '加速度(rms)x轴',
  `armsy` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '加速度(rms)y轴',
  `armsz` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '加速度(rms)z轴',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `fq_result` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '频率结果',
  `ssp_result` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '速度(peak)结果',
  `dsp_result` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '振幅值(peak)结果',
  `asp_result` decimal(20, 6) NULL DEFAULT 0.000000 COMMENT '加速度(peak)结果',
  `be_supplementary` tinyint(1) NULL DEFAULT -1 COMMENT '是否补传数据',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1123291065437401089 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '振动报文记录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for water_level_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `water_level_packet_info`;
CREATE TABLE `water_level_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `temperature` decimal(5, 1) NULL DEFAULT NULL COMMENT '温度',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `water_range_value` decimal(20, 2) NULL DEFAULT NULL,
  `water_current_value` decimal(20, 2) NULL DEFAULT NULL,
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `be_supplementary` tinyint(1) NULL DEFAULT -1 COMMENT '是否补传数据',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_dst_time_value`(`imei`, `data_status`, `create_time`, `water_range_value`) USING BTREE,
  INDEX `idx_wat_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_imei_time_ds`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10918 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '水位上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for water_pressure_meter_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `water_pressure_meter_packet_info`;
CREATE TABLE `water_pressure_meter_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `range_value` decimal(20, 7) NULL DEFAULT NULL COMMENT '变化量',
  `current_value` decimal(20, 7) NULL DEFAULT NULL COMMENT '当前值',
  `init_value` decimal(20, 7) NULL DEFAULT NULL COMMENT '初始值',
  `frequency_value` decimal(20, 2) NULL DEFAULT NULL COMMENT '上报的频率',
  `temperature` decimal(5, 2) NULL DEFAULT NULL COMMENT '温度',
  `battery_level` bigint(10) NULL DEFAULT NULL COMMENT '电池电量',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_status`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1123283943681175553 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '水压力计上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for weixin_mp
-- ----------------------------
DROP TABLE IF EXISTS `weixin_mp`;
CREATE TABLE `weixin_mp`  (
  `id` int(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `mp_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '公众号名称',
  `mp_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '该公众号的微信号',
  `app_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '开发者Id',
  `app_secret` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '开发者密码',
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '令牌',
  `aes_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '加密秘钥',
  `remark` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `owner_group_id` int(11) NOT NULL COMMENT '所有权组织Id',
  `crt_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新主机',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_mp_id`(`mp_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '微信公众号表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for wind_speed_direction_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `wind_speed_direction_packet_info`;
CREATE TABLE `wind_speed_direction_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `location` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '设备地址,16进制',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `data_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '数据状态',
  `be_supplementary` tinyint(1) NOT NULL DEFAULT -1 COMMENT '是否补传数据',
  `temperature` decimal(5, 2) NULL DEFAULT NULL COMMENT '温度',
  `battery_level` bigint(10) NULL DEFAULT NULL COMMENT '电池电量',
  `wind_speed` decimal(20, 1) NULL DEFAULT NULL COMMENT '风速',
  `wind_direction` int(3) NULL DEFAULT NULL COMMENT '风向',
  `data_id` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time_status`(`imei`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_time_imei_status`(`create_time`, `imei`, `data_status`) USING BTREE,
  INDEX `idx_did_time_ds`(`data_id`, `create_time`, `data_status`) USING BTREE,
  INDEX `idx_did_imei_time_ds`(`data_id`, `imei`, `create_time`, `data_status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1123144475703783425 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '风速风向仪上报记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for wrong_packet_info
-- ----------------------------
DROP TABLE IF EXISTS `wrong_packet_info`;
CREATE TABLE `wrong_packet_info`  (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'imei',
  `original_packet` varchar(3072) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '原始报文',
  `report_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上报时间',
  `crt_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_imei_time`(`imei`, `report_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 126 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '异常报文记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- View structure for cmd_view
-- ----------------------------
DROP VIEW IF EXISTS `cmd_view`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `cmd_view` AS select `device_command`.`id` AS `id`,`device_command`.`command_name` AS `command_name`,`device_command`.`command_code` AS `command_code`,`device_command`.`resp_code` AS `resp_code` from `device_command`;

-- ----------------------------
-- View structure for latest_device_alarm
-- ----------------------------
DROP VIEW IF EXISTS `latest_device_alarm`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `latest_device_alarm` AS select `arm`.`id` AS `id`,`arm`.`imei` AS `imei`,`arm`.`alarm_status` AS `alarm_status`,`arm`.`alarm_result` AS `alarm_result`,`arm`.`charge_man` AS `charge_man`,`arm`.`charge_phone` AS `charge_phone`,`arm`.`predict_complete_time` AS `predict_complete_time`,`arm`.`real_complete_time` AS `real_complete_time`,`arm`.`danger_score` AS `danger_score`,`arm`.`duration` AS `duration`,`arm`.`fall_index` AS `fall_index`,`arm`.`swing_index` AS `swing_index`,`arm`.`lean_index` AS `lean_index`,`arm`.`spin_index` AS `spin_index`,`arm`.`alarm_desc` AS `alarm_desc`,`arm`.`remark` AS `remark`,`arm`.`crt_time` AS `crt_time`,`arm`.`crt_user` AS `crt_user`,`arm`.`crt_name` AS `crt_name`,`arm`.`crt_host` AS `crt_host`,`arm`.`upd_time` AS `upd_time`,`arm`.`upd_user` AS `upd_user`,`arm`.`upd_name` AS `upd_name`,`arm`.`upd_host` AS `upd_host`,`arm`.`year` AS `year`,`arm`.`month` AS `month`,`arm`.`day` AS `day`,`arm`.`time` AS `time`,`arm`.`danger_level` AS `danger_level` from `alarm` `arm` where (`arm`.`imei`,`arm`.`crt_time`) in (select `alarm`.`imei`,max(`alarm`.`crt_time`) from `alarm` group by `alarm`.`imei`);

-- ----------------------------
-- View structure for latest_device_status
-- ----------------------------
DROP VIEW IF EXISTS `latest_device_status`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `latest_device_status` AS select distinct `pi`.`id` AS `id`,`pi`.`imei` AS `imei`,`pi`.`protocol` AS `protocol`,`pi`.`protocol_version` AS `protocol_version`,`pi`.`battery_level` AS `battery_level`,`pi`.`temperature` AS `temperature`,`pi`.`heading_degrees` AS `heading_degrees`,`pi`.`create_time` AS `create_time`,`pi`.`lean_degrees` AS `lean_degrees` from (`bms`.`packet_info` `pi` join (select `bms`.`packet_info`.`imei` AS `imei`,max(`bms`.`packet_info`.`create_time`) AS `max_create_time` from `bms`.`packet_info` group by `bms`.`packet_info`.`imei`) `pm` on(((`pi`.`imei` = `pm`.`imei`) and (`pi`.`create_time` = `pm`.`max_create_time`))));

-- ----------------------------
-- View structure for max_soft_version
-- ----------------------------
DROP VIEW IF EXISTS `max_soft_version`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `max_soft_version` AS select `upgrader`.`id` AS `id`,`upgrader`.`publish_date` AS `publish_date`,`upgrader`.`soft_version` AS `soft_version`,`upgrader`.`hard_version` AS `hard_version`,`upgrader`.`product_modal` AS `product_modal`,`upgrader`.`url` AS `url`,`upgrader`.`filename` AS `filename`,`upgrader`.`file_type` AS `file_type`,`upgrader`.`group_id` AS `group_id`,`upgrader`.`remark` AS `remark`,`upgrader`.`crt_time` AS `crt_time`,`upgrader`.`crt_user` AS `crt_user`,`upgrader`.`crt_name` AS `crt_name`,`upgrader`.`crt_host` AS `crt_host`,`upgrader`.`upd_time` AS `upd_time`,`upgrader`.`upd_user` AS `upd_user`,`upgrader`.`upd_name` AS `upd_name`,`upgrader`.`upd_host` AS `upd_host` from `upgrader` where (`upgrader`.`hard_version`,`upgrader`.`group_id`,`upgrader`.`soft_version`) in (select `upgrader`.`hard_version`,`upgrader`.`group_id`,max(`upgrader`.`soft_version`) from `upgrader` group by `upgrader`.`hard_version`,`upgrader`.`group_id`);

-- ----------------------------
-- Procedure structure for UpdateAlarmTimes
-- ----------------------------
DROP PROCEDURE IF EXISTS `UpdateAlarmTimes`;
delimiter ;;
CREATE PROCEDURE `UpdateAlarmTimes`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE alarm_id BIGINT;
    DECLARE alarm_level TINYINT;
    DECLARE crt_time DATETIME;
    DECLARE cur CURSOR FOR 
        SELECT id, device_alarm_level, crt_time FROM alarm WHERE device_alarm_level IN (2) AND id = 26967;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO alarm_id, alarm_level, crt_time;
        IF done THEN
            LEAVE read_loop;
        END IF;

        IF crt_time IS NOT NULL THEN
            CASE alarm_level
                WHEN 1 THEN
                    -- 1级预警30分钟以内（分钟：10，15，20,25,30；秒：00,42,58,53,15,18,56,48,39,15）
                    SET @random_minute = ELT(FLOOR(RAND() * 5) + 1, 10, 15, 20, 25, 30);
                    SET @random_second = ELT(FLOOR(RAND() * 10) + 1, 00, 42, 58, 53, 15, 18, 56, 48, 39, 15);
                    -- 调试信息
                    SELECT @random_minute, @random_second;
                    UPDATE alarm
                    SET upd_time = DATE_ADD(crt_time, INTERVAL (@random_minute * 60 + @random_second) SECOND)
                    WHERE id = alarm_id;
                WHEN 2 THEN
                    -- 2级预警1小时以内（分钟：15,25,30,40,45,50,60；秒：00,42,58,53,15,18,56,48,39,15）
                    SET @random_minute = ELT(FLOOR(RAND() * 7) + 1, 15, 25, 30, 40, 45, 50, 60);
                    SET @random_second = ELT(FLOOR(RAND() * 10) + 1, 00, 42, 58, 53, 15, 18, 56, 48, 39, 15);
                    -- 调试信息
                    SELECT @random_minute, @random_second;
                    UPDATE alarm
                    SET upd_time = DATE_ADD(crt_time, INTERVAL (@random_minute * 60 + @random_second) SECOND)
                    WHERE id = alarm_id;
                WHEN 3 THEN
                    -- 3级预警1个半小时以内（分钟：35,45,60,65,70,75,86,89 秒：00,42,58,53,15,18,56,48,39,15）
                    SET @random_minute = ELT(FLOOR(RAND() * 8) + 1, 35, 45, 60, 65, 70, 75, 86, 89);
                    SET @random_second = ELT(FLOOR(RAND() * 10) + 1, 00, 42, 58, 53, 15, 18, 56, 48, 39, 15);
                    -- 调试信息
                    SELECT @random_minute, @random_second;
                    UPDATE alarm
                    SET upd_time = DATE_ADD(crt_time, INTERVAL (@random_minute * 60 + @random_second) SECOND)
                    WHERE id = alarm_id;
            END CASE;
        END IF;
    END LOOP;

    CLOSE cur;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for update_alarm_processing_time
-- ----------------------------
DROP PROCEDURE IF EXISTS `update_alarm_processing_time`;
delimiter ;;
CREATE PROCEDURE `update_alarm_processing_time`(in group_id int(11), in start_time nvarchar(20), in end_time nvarchar(20))
BEGIN
    -- 声明变量
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_id BIGINT;
    DECLARE v_crt_time DATETIME;
    DECLARE v_device_alarm_level TINYINT;
    DECLARE v_random_minutes INT;
    DECLARE v_random_seconds INT;
    DECLARE v_random_time DATETIME;
    
    -- 声明游标
    DECLARE cur CURSOR FOR 
         SELECT id, crt_time, device_alarm_level 
        FROM alarm 
        WHERE alarm_status IN (2) AND crt_time>=start_time AND crt_time<=end_time AND imei in (
				select imei FROM device_info info
        INNER JOIN base_group bg ON info.group_id = bg.id
        INNER JOIN group_relation gr ON info.group_id = gr.descendant         
                and gr.ancestor = group_id );
        
    -- 声明继续处理程序
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- 打开游标
    OPEN cur;
    
    -- 开始循环处理数据
    read_loop: LOOP
        -- 获取当前记录
        FETCH cur INTO v_id, v_crt_time, v_device_alarm_level;
        
        -- 如果没有更多记录，退出循环
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- 根据预警等级设置不同的随机分钟数和秒数
        IF v_device_alarm_level = 1 THEN
            -- 1级预警：30分钟以内
            SET v_random_minutes = ELT(FLOOR(1 + RAND() * 5), 10, 15, 20, 25, 30);
            
        ELSEIF v_device_alarm_level = 2 THEN
            -- 2级预警：1小时以内
            SET v_random_minutes = ELT(FLOOR(1 + RAND() * 7), 15, 25, 30, 40, 45, 50, 60);
            
        ELSE
            -- 3级预警：1.5小时以内
            SET v_random_minutes = ELT(FLOOR(1 + RAND() * 8), 35, 45, 60, 65, 70, 75, 86, 89);
            
        END IF;
        
        -- 随机选择秒数
        SET v_random_seconds = ELT(FLOOR(1 + RAND() * 10), 0, 42, 58, 53, 15, 18, 56, 48, 39, 15);
        
        -- 生成随机时间
        SET v_random_time = v_crt_time + INTERVAL (v_random_minutes * 60 + v_random_seconds) SECOND;
        
        -- 更新处理时间
        UPDATE alarm 
        SET upd_time = v_random_time
        WHERE id = v_id;
        
    END LOOP;
    
    -- 关闭游标
    CLOSE cur;
    
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
