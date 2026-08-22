import os

# Ollama 配置
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./retail.db")

# 系统提示词
SYSTEM_PROMPT = """你是一名资深零售营运分析师，服务于智慧零售营运Agent系统。
回答要求：
1. 所有建议必须基于提供的数据，严禁编造数字。
2. 回答简洁专业，分点清晰。
3. 涉及金额、数量时保留两位小数。
4. 给出可执行的营运建议，不要空泛。
5. 用中文回答。"""
