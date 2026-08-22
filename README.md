# 智慧零售营运 Agent

基于 Vue 3 + FastAPI + Ollama 的智慧零售营运智能体系统，集成商品推荐、顾客经营、库存管理、营运决策分析和智能对话五大模块。

## 🔗 在线体验 & 仓库

- **GitHub 仓库**：https://github.com/WBW-QD/smart-retail-agent
- **在线演示（GitHub Pages）**：https://WBW-QD.github.io/smart-retail-agent/
- 线上版本为**纯前端静态演示**（无后端），AI 对话、数据看板等调用 `/api` 的功能需在本地运行后端 + Ollama 才能使用（详见下方「部署到 GitHub Pages」说明）。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + Element Plus + ECharts + Axios |
| 后端 | Python FastAPI + SQLAlchemy |
| 大模型 | 本地 Ollama（默认 qwen2.5:7b） |
| 数据库 | SQLite（零配置，自动初始化） |

## 功能模块

1. **营运看板** — 销售概览统计卡片、销售趋势折线图、热销品类饼图、自然语言数据分析问答
2. **商品推荐** — 选择顾客后，AI 基于消费偏好生成个性化商品推荐及理由
3. **顾客经营** — 顾客列表与画像详情、历史订单、AI 生成多场景营销文案（一键复制）
4. **库存管理** — 库存列表、低库存预警标记、AI 基于销量生成补货建议
5. **智能对话** — 全屏对话页 + 全局侧边栏对话面板，对话历史持久化，快捷提问

## 环境要求

- Python 3.10+
- Node.js 16+
- Ollama（本地服务，端口 11434）

## 快速开始

### 1. 启动 Ollama

```bash
# 安装 Ollama（如未安装）
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull qwen2.5:7b

# 启动服务（保持运行）
ollama serve
```

### 2. 一键启动项目

```bash
chmod +x start.sh
./start.sh
```

启动脚本会自动：
- 创建 Python 虚拟环境并安装后端依赖
- 安装前端 npm 依赖
- 后台启动后端（端口 8000）和前端（端口 5173）

### 3. 手动启动（分步）

**后端：**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**前端（新开终端）：**
```bash
cd frontend
npm install
npm run dev
```

### 4. 访问

- 前端界面：http://localhost:5173
- 后端 API 文档：http://localhost:8000/docs

## 部署到 GitHub Pages

前端已配置 GitHub Actions 自动部署（`.github/workflows/deploy.yml`），推送到 `main` 分支即自动构建并发布：

1. 在 GitHub 仓库 **Settings → Pages** 中确认 **Source** 为 **GitHub Actions**
2. 推送代码到 `main`，Actions 会自动执行 `build` + `deploy`
3. 访问 https://WBW-QD.github.io/smart-retail-agent/

> ⚠️ **限制说明**：GitHub Pages 是纯静态托管，没有后端服务。线上演示可正常浏览界面，但调用 `/api` 的 AI 对话、数据看板、商品推荐等动态功能会失败——完整功能请按「快速开始」在本地运行（后端 + Ollama）。

## 项目结构

```
smart-retail-agent/
├── frontend/                  # Vue 3 前端
│   ├── src/
│   │   ├── views/             # 5个页面视图
│   │   │   ├── Dashboard.vue
│   │   │   ├── Products.vue
│   │   │   ├── Customers.vue
│   │   │   ├── Inventory.vue
│   │   │   └── Chat.vue
│   │   ├── components/        # 布局 & 对话侧边栏
│   │   │   ├── Layout.vue
│   │   │   └── ChatSidebar.vue
│   │   ├── router/            # 路由配置
│   │   ├── api/               # Axios API 封装
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── backend/                   # FastAPI 后端
│   ├── main.py                # API 路由（12个接口）
│   ├── config.py              # 配置（Ollama地址、模型名、系统提示词）
│   ├── database.py            # 数据库连接
│   ├── models.py              # SQLAlchemy 数据模型
│   ├── ollama_client.py       # Ollama 调用封装
│   ├── mock_data.py           # 初始化模拟数据
│   └── requirements.txt
├── start.sh                   # 一键启动脚本
├── PROMPT.md                  # 原始 vibe coding 提示词
└── README.md
```

## 配置说明

在 `backend/config.py` 中可修改：

```python
OLLAMA_BASE_URL = "http://localhost:11434"   # Ollama 服务地址
OLLAMA_MODEL = "qwen2.5:7b"                   # 使用的模型
OLLAMA_TIMEOUT = 120                           # 超时时间（秒）
```

也可通过环境变量覆盖：
```bash
export OLLAMA_BASE_URL=http://192.168.1.100:11434
export OLLAMA_MODEL=llama3.1
```

## 模型切换建议

| 模型 | 参数量 | 适用场景 |
|------|--------|----------|
| qwen2.5:7b | 7B | 中文效果好，推荐默认 |
| llama3.1 | 8B | 通用能力强 |
| phi3:mini | 3.8B | 低配置电脑 |
| qwen2.5:3b | 3B | 极轻量，快速响应 |

切换模型：`ollama pull <模型名>`，然后修改 `config.py` 中的 `OLLAMA_MODEL`。

## API 接口列表

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/chat | 通用对话 |
| POST | /api/recommend | 商品推荐 |
| GET | /api/customer/profile | 顾客画像详情 |
| GET | /api/customers | 顾客列表 |
| POST | /api/customer/marketing | 生成营销文案 |
| GET | /api/inventory | 库存列表 |
| POST | /api/inventory/restock | 补货建议 |
| GET | /api/dashboard/sales | 销售看板数据 |
| POST | /api/dashboard/query | 自然语言数据分析 |
| GET | /api/history | 对话历史 |
| DELETE | /api/history | 清空对话历史 |
| GET | /api/products | 商品列表 |

## 注意事项

1. **必须先启动 Ollama**，否则所有 AI 功能会返回连接错误
2. 首次启动后端会自动创建数据库并插入模拟数据，无需手动初始化
3. 前端通过 Vite 代理将 `/api` 请求转发到后端 `localhost:8000`，无需额外配置跨域
4. 如 Ollama 运行在另一台机器上，修改 `OLLAMA_BASE_URL` 为对应地址
5. 前端路由使用 hash 模式（`/#/products`），以保证 GitHub Pages 等纯静态托管下刷新不 404
6. GitHub Pages 线上演示为静态前端，动态功能需本地运行（见「部署到 GitHub Pages」）
