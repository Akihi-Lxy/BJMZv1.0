# 北京梦织家居有限公司官网

## 项目简介

北京梦织家居有限公司官方网站系统，包含前端展示页面和管理后台，支持产品动态管理。

## 功能特点

### 前台功能
- 响应式网站设计，支持PC端和移动端
- 公司简介展示
- 产品动态展示（从服务器获取）
- 服务优势介绍
- 在线留言功能
- Banner轮播

### 后台管理功能
- 管理员登录认证
- 产品添加/编辑/删除
- 产品图片上传
- 数据统计面板

## 技术栈

- **前端**: HTML5, CSS3, JavaScript
- **后端**: Python Flask
- **依赖**: Flask, Flask-CORS, Werkzeug

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务器

```bash
python main.py
```

### 3. 访问网站

- **官网首页**: http://localhost:3000
- **管理后台**: http://localhost:3000/admin/login

---

## 管理员账号

- 用户名: `zhangmengke`
- 密码: `123456`

---

## 目录结构

```
ai/
├── css/                  # 样式文件
│   └── style.css
├── js/                   # 前端脚本
│   └── main.js
├── images/               # 静态图片
│   ├── logo.png
│   ├── cf03.jpg
│   ├── cf03 (1).jpg
│   └── cf2.jpg
├── uploads/              # 上传的产品图片
├── data/                 # 数据存储
│   └── products.json
├── index.html            # 官网首页
├── admin.html            # 管理后台
├── admin-login.html      # 登录页面
├── main.py               # Python后端服务器
├── requirements.txt      # Python依赖
└── README.md             # 说明文档
```

---

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/login | 管理员登录 |
| POST | /api/logout | 退出登录 |
| GET | /api/check-auth | 检查登录状态 |
| GET | /api/products | 获取产品列表 |
| POST | /api/products | 添加产品（需登录） |
| PUT | /api/products/:id | 更新产品（需登录） |
| DELETE | /api/products/:id | 删除产品（需登录） |

---

## 外网访问配置

如果需要让其他人通过外网访问，可以：

### 方法1: 使用内网穿透工具（推荐）
- 使用 ngrok、frp 等工具将本地服务映射到公网
- 例如使用 ngrok:
  ```bash
  ngrok http 3000
  ```

### 方法2: 部署到云服务器
- 将项目上传到阿里云、腾讯云等服务器
- 安装 Python 环境
- 运行 `pip install -r requirements.txt && python main.py`
- 使用 nginx 做反向代理

### 方法3: 局域网访问
- 确保服务器和访问者在同一局域网
- 服务器已配置监听 `0.0.0.0`
- 访问地址: `http://服务器IP:3000`
- 查看本机IP: Windows CMD输入 `ipconfig`

---

## 公司信息

- **公司名称**: 北京梦织家居有限公司
- **英文名称**: Beijing Mengzhi Home Co.,Ltd.
- **统一社会信用代码**: 91110112MADN22Q97H
- **法定代表人**: 张孟强
- **联系电话**: 17601607071
- **电子邮箱**: 17601607071@163.com
- **公司地址**: 北京市通州区玉桥北里47号1层A650号

---

## 版权所有

© 2024 北京梦织家居有限公司
