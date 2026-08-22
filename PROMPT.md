# Vibe Coding 提示词（原始版）

> 本文件保留了最初用于喂给 Claude 的完整 vibe coding 提示词。项目已基于此提示词搭建完成，保留供参考。

```
你是一名全栈开发工程师，请帮我从零搭建一个「智慧零售营运 Agent」Web 应用，技术栈如下：

【前端】Vue 3 + Vite + Element Plus + ECharts + Axios
【后端】Python FastAPI（作为 Vue 与 Ollama 之间的 API 网关）
【大模型】本地 Ollama，默认模型 qwen2.5:7b（可在配置文件切换）
【数据库】SQLite（轻量，零配置，存商品、顾客、订单、对话记录）

一、项目核心功能（必须全部实现）
1. 商品推荐模块：输入顾客ID，Agent 基于购买历史生成个性化商品推荐 + 推荐理由
2. 顾客经营模块：顾客画像展示 + Agent 自动生成会员营销文案，可一键复制
3. 库存管理模块：商品库存列表 + 低库存预警 + Agent 生成补货建议
4. 营运决策支持：销售数据看板（ECharts）+ 自然语言问答分析
5. 智能对话侧边栏：全局常驻对话面板，对话历史持久化

二、前端页面结构（Vue 路由）
/            → 仪表盘 Dashboard
/products    → 商品推荐
/customers   → 顾客经营
/inventory   → 库存管理
/chat        → 智能对话

三、后端 API（FastAPI）
POST /api/chat
POST /api/recommend
GET  /api/customer/profile
GET  /api/customers
POST /api/customer/marketing
GET  /api/inventory
POST /api/inventory/restock
GET  /api/dashboard/sales
POST /api/dashboard/query
GET  /api/history
DELETE /api/history
GET  /api/products

四、数据库表（SQLite + SQLAlchemy）
products, customers, orders, chat_history
启动时自动建表并插入 mock 数据（20商品、10顾客、80订单）

五、Ollama 调用
- 调用 http://localhost:11434/api/chat
- system prompt：资深零售营运分析师，基于数据回答，不编造数字
- 相关数据作为 context 注入 prompt

六、工程规范
- 前后端分离，frontend/ + backend/
- 一键启动脚本 start.sh
- 代码有必要注释
- README.md 写明环境要求、安装步骤、启动命令
```
