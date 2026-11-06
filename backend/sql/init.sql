-- ============================================================
-- 颐邻通 V1.0 社区养老便民服务平台
-- 建库建表 SQL（MySQL 8.0）
-- 仅 V1.0 范围：user 表 + work_order 表
-- ============================================================

-- 1. 建库
CREATE DATABASE IF NOT EXISTS elderlink_v10
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE elderlink_v10;

-- 2. 用户表（user）
DROP TABLE IF EXISTS work_order;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id          INT           NOT NULL AUTO_INCREMENT  COMMENT '用户编号（主键，自增）',
    account     VARCHAR(50)   NOT NULL                 COMMENT '登录账号',
    name        VARCHAR(50)   NOT NULL                 COMMENT '姓名',
    role        VARCHAR(20)   NOT NULL                 COMMENT '角色（家属/助老员/管理员）',
    community   VARCHAR(100)  NOT NULL DEFAULT ''      COMMENT '所属社区',
    password    VARCHAR(100)  NOT NULL                 COMMENT '登录密码',
    status      VARCHAR(20)   NOT NULL DEFAULT '启用'   COMMENT '账号状态（启用/停用）',
    PRIMARY KEY (id),
    UNIQUE KEY uk_account (account)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 3. 工单表（work_order）
CREATE TABLE work_order (
    id           INT           NOT NULL AUTO_INCREMENT  COMMENT '工单主键，自增',
    order_no     VARCHAR(30)   NOT NULL                 COMMENT '工单编号（业务唯一标识）',
    submitter_id INT           NOT NULL                 COMMENT '提交人（外键→user.id）',
    elder_name   VARCHAR(50)   NOT NULL                 COMMENT '老人姓名',
    content      TEXT          NOT NULL                 COMMENT '咨询内容',
    status       VARCHAR(20)   NOT NULL DEFAULT '待分派' COMMENT '工单状态',
    reply_content TEXT                                  COMMENT '答复内容（复核通过后写入）',
    submit_time  DATETIME      NOT NULL                 COMMENT '提交时间',
    assign_time  DATETIME                               COMMENT '分派时间',
    review_time  DATETIME                               COMMENT '复核时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_order_no (order_no),
    KEY idx_submitter_id (submitter_id),
    CONSTRAINT fk_order_submitter FOREIGN KEY (submitter_id) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='工单表';

-- ============================================================
-- 4. 插入测试数据
-- ============================================================

-- 测试账号（密码统一为 123456）
INSERT INTO user (account, name, role, community, password, status) VALUES
('fam01',   '张阿姨', '家属',   '阳光社区', '123456', '启用'),
('fam02',   '李叔叔', '家属',   '阳光社区', '123456', '启用'),
('help01',  '王助老', '助老员', '阳光社区', '123456', '启用'),
('help02',  '赵助老', '助老员', '阳光社区', '123456', '启用'),
('admin',   '孙管理', '管理员', '阳光社区', '123456', '启用');

-- 插入一条示例工单（家属 fam01 提交的咨询）
INSERT INTO work_order (order_no, submitter_id, elder_name, content, status, submit_time) VALUES
('WO20261104001', 1, '张大爷', '请问社区有没有免费体检活动？', '待分派', NOW());
