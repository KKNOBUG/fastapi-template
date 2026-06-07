from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `krun_example_category` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    `state` SMALLINT NOT NULL  COMMENT '状态(0:启用, 1:禁用)' DEFAULT 0,
    `created_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `created_user` VARCHAR(16)   COMMENT '创建人员',
    `updated_user` VARCHAR(16)   COMMENT '更新人员',
    `name` VARCHAR(64) NOT NULL  COMMENT '分类名称',
    `code` VARCHAR(32) NOT NULL UNIQUE COMMENT '分类编码',
    `description` LONGTEXT   COMMENT '分类描述',
    `sort_order` INT NOT NULL  COMMENT '排序序号' DEFAULT 0,
    `parent_id` BIGINT   COMMENT '父分类ID',
    KEY `idx_krun_exampl_state_7db76a` (`state`)
) CHARACTER SET utf8mb4 COMMENT='商品分类模型';
CREATE TABLE IF NOT EXISTS `krun_example_product` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    `state` SMALLINT NOT NULL  COMMENT '状态(0:启用, 1:禁用)' DEFAULT 0,
    `created_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `created_user` VARCHAR(16)   COMMENT '创建人员',
    `updated_user` VARCHAR(16)   COMMENT '更新人员',
    `uid` CHAR(36)  UNIQUE COMMENT '唯一标识符',
    `name` VARCHAR(128) NOT NULL  COMMENT '商品名称',
    `code` VARCHAR(32) NOT NULL UNIQUE COMMENT '商品编码',
    `description` LONGTEXT   COMMENT '商品描述',
    `price` DECIMAL(10,2) NOT NULL  COMMENT '商品价格',
    `stock` INT NOT NULL  COMMENT '库存数量' DEFAULT 0,
    `category_id` BIGINT NOT NULL  COMMENT '分类ID',
    `is_featured` BOOL NOT NULL  COMMENT '是否推荐' DEFAULT 0,
    `tags` JSON NOT NULL  COMMENT '商品标签',
    KEY `idx_krun_exampl_state_925e91` (`state`),
    KEY `idx_krun_exampl_categor_07d841` (`category_id`)
) CHARACTER SET utf8mb4 COMMENT='商品模型';
CREATE TABLE IF NOT EXISTS `krun_user` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    `state` SMALLINT NOT NULL  COMMENT '状态(0:启用, 1:禁用)' DEFAULT 0,
    `created_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `created_user` VARCHAR(16)   COMMENT '创建人员',
    `updated_user` VARCHAR(16)   COMMENT '更新人员',
    `username` VARCHAR(32) NOT NULL UNIQUE COMMENT '用户账号',
    `password` VARCHAR(255) NOT NULL  COMMENT '用户密码',
    `alias` VARCHAR(64) NOT NULL  COMMENT '用户姓名',
    `email` VARCHAR(64) NOT NULL  COMMENT '用户邮箱',
    `phone` VARCHAR(20)   COMMENT '用户电话',
    `motto` VARCHAR(255)   COMMENT '用户签名',
    `avatar` VARCHAR(255)   COMMENT '用户头像',
    `is_active` BOOL NOT NULL  COMMENT '是否激活' DEFAULT 1,
    `is_superuser` BOOL NOT NULL  COMMENT '是否为超级管理员' DEFAULT 0,
    `last_login` DATETIME(6)   COMMENT '最后一次登陆时间',
    `address` VARCHAR(255)   COMMENT '用户住址',
    `gender` SMALLINT NOT NULL  COMMENT '用户性别: 0未知 1男 2女' DEFAULT 0,
    `user_type` SMALLINT NOT NULL  COMMENT '用户类型：0xx 1xx 2xx' DEFAULT 0,
    `emergency_name` VARCHAR(32)   COMMENT '紧急联系人',
    `emergency_phone` VARCHAR(20)   COMMENT '紧急联系电话',
    UNIQUE KEY `uid_krun_user_alias_6dc3a1` (`alias`, `email`),
    KEY `idx_krun_user_state_80291a` (`state`),
    KEY `idx_krun_user_is_acti_e29ecb` (`is_active`),
    KEY `idx_krun_user_is_supe_31d692` (`is_superuser`),
    KEY `idx_krun_user_last_lo_a0ca1d` (`last_login`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `krun_audit` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    `created_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `user_id` BIGINT NOT NULL  COMMENT '用户ID',
    `username` VARCHAR(32) NOT NULL  COMMENT '用户名称',
    `request_time` DATETIME(6) NOT NULL  COMMENT '请求时间',
    `request_tags` VARCHAR(255)   COMMENT '请求模块' DEFAULT '',
    `request_summary` VARCHAR(255)   COMMENT '请求接口' DEFAULT '',
    `request_method` VARCHAR(7) NOT NULL  COMMENT '请求方式',
    `request_router` VARCHAR(255) NOT NULL  COMMENT '请求路由',
    `request_client` VARCHAR(16)   COMMENT '请求来源' DEFAULT '',
    `request_header` JSON   COMMENT '请求头部',
    `request_params` LONGTEXT   COMMENT '请求参数',
    `response_time` DATETIME(6) NOT NULL  COMMENT '响应时间',
    `response_header` JSON   COMMENT '响应头部',
    `response_code` VARCHAR(16)   COMMENT '响应代码' DEFAULT '',
    `response_message` VARCHAR(512)   COMMENT '响应消息' DEFAULT '',
    `response_params` LONGTEXT   COMMENT '响应参数',
    `response_elapsed` VARCHAR(16) NOT NULL  COMMENT '响应耗时',
    KEY `idx_krun_audit_user_id_e9d5e0` (`user_id`),
    KEY `idx_krun_audit_usernam_846619` (`username`),
    KEY `idx_krun_audit_request_a40ba0` (`request_time`),
    KEY `idx_krun_audit_request_5a7d0a` (`request_tags`),
    KEY `idx_krun_audit_request_d86ea0` (`request_summary`),
    KEY `idx_krun_audit_request_33c11b` (`request_method`),
    KEY `idx_krun_audit_request_b7752f` (`request_router`),
    KEY `idx_krun_audit_respons_6a54ed` (`response_time`),
    KEY `idx_krun_audit_respons_7f45f5` (`response_code`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
