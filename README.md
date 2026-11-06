# 颐邻通 V1.0 · 社区养老便民服务平台

项目英文名称：ElderLink Community Elderly Service Platform
学号：2405030417　姓名：郑翕

## 技术栈

| 层 | 技术 | 版本 |
|----|------|------|
| 前端 | 原生 HTML + CSS + JavaScript | - |
| 后端 | FastAPI | 0.111+ |
| 数据库 | MySQL | 8.0 |
| ORM | SQLAlchemy | 2.0+ |
| 驱动 | pymysql | 1.1+ |

## V1.0 范围

| 类型 | 数量 | 清单 |
|------|------|------|
| 页面 | 3 | login.html, consult.html, workorder.html |
| 接口 | 6 | POST /api/login, POST /api/orders, GET /api/orders, PUT /api/orders/{id}/cancel, PUT /api/orders/{id}/assign, PUT /api/orders/{id}/review |
| 数据表 | 2 | user, work_order |

**⚠️ V1.0 不包含**：预约工单、公告、档案绑定、用户管理等后续模块。

## 项目结构

```
ElderLink_V1.0/
├── frontend/                   # 前端（由 FastAPI 静态托管）
│   ├── login.html              # 登录页
│   ├── consult.html            # 家属咨询工单页
│   ├── workorder.html          # 后台工单处理台
│   ├── css/
│   │   └── style.css           # 全局样式
│   └── js/
│       └── api.js              # fetch 封装 + 工具函数
├── backend/
│   ├── main.py                 # FastAPI 入口 + CORS + 静态托管
│   ├── database.py             # SQLAlchemy 引擎 + 连接配置
│   ├── models.py               # ORM 模型（User, WorkOrder）
│   ├── schemas.py              # Pydantic 请求/响应模型
│   ├── requirements.txt        # Python 依赖
│   ├── sql/
│   │   └── init.sql            # 建库建表 + 测试数据（MySQL 8.0）
│   └── routers/
│       ├── __init__.py
│       ├── auth.py             # POST /api/login
│       └── orders.py           # 其余 5 个工单接口
└── README.md
```

## 快速启动

### 1. 准备环境

```bash
# 确保已安装 Python 3.10+ 和 MySQL 8.0
# 安装 Python 依赖
cd ElderLink_V1.0/backend
pip install -r requirements.txt
```

### 2. 建库建表

打开 Navicat 或 MySQL 命令行，执行 `backend/sql/init.sql` 即可：

```sql
source init.sql;
```

（数据库连接信息已写死在 `database.py`：root/root@localhost:3306/elderlink_v10）

### 3. 启动服务

```bash
cd ElderLink_V1.0/backend
python main.py
```

启动后控制台会打印：
```
后端 API：  http://localhost:8000/docs
前端首页：  http://localhost:8000/login.html
```

### 4. 浏览器访问

| 地址 | 用途 |
|------|------|
| http://localhost:8000/login.html | 登录页 |
| http://localhost:8000/docs | FastAPI Swagger 接口文档 |

## 测试账号

| 账号 | 密码 | 角色 | 登录后跳转 |
|------|------|------|-----------|
| fam01 | 123456 | 家属 | consult.html |
| help01 | 123456 | 助老员 | workorder.html |
| admin | 123456 | 管理员 | workorder.html |

## 核心业务闭环（V1.0 跑通流程）

```
家属 fam01 登录 → consult.html 提交咨询工单
      ↓
管理员 admin / 助老员 help01 登录 → workorder.html 看到"待分派"的工单
      ↓
点击"分派给我" → 工单状态变为"处理协同中"
      ↓
点击"通过"并填入答复 → 工单状态变为"复核通过"
      ↓
家属刷新 consult.html → 看到答复内容 ✅
```

## 6 个接口一览

| 方法 | 路径 | 功能 | 操作角色 |
|------|------|------|---------|
| POST | `/api/login` | 用户登录校验 | 所有人 |
| POST | `/api/orders` | 提交咨询工单 | 家属 |
| GET | `/api/orders` | 查询工单列表 | 所有人 |
| PUT | `/api/orders/{id}/cancel` | 取消工单 | 家属 |
| PUT | `/api/orders/{id}/assign` | 分派工单 | 管理员/助老员 |
| PUT | `/api/orders/{id}/review` | 复核审批（通过/驳回） | 管理员/助老员 |
