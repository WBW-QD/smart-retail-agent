import requests
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT, SYSTEM_PROMPT

def chat(messages, stream=False):
    """调用 Ollama 对话接口"""
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": stream
    }
    try:
        resp = requests.post(url, json=payload, timeout=OLLAMA_TIMEOUT)
        resp.raise_for_status()
        if stream:
            return resp
        data = resp.json()
        return data.get("message", {}).get("content", "")
    except requests.exceptions.ConnectionError:
        return "【错误】无法连接 Ollama 服务，请确认 Ollama 已启动且地址配置正确。"
    except requests.exceptions.Timeout:
        return "【错误】Ollama 响应超时，请稍后重试或更换更轻量模型。"
    except Exception as e:
        return f"【错误】Ollama 调用失败：{str(e)}"

def build_messages(user_prompt, context=""):
    """构建带系统提示和上下文的消息列表"""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if context:
        messages.append({"role": "system", "content": f"参考数据：\n{context}"})
    messages.append({"role": "user", "content": user_prompt})
    return messages

def generate_recommendation(customer_info, products_info):
    """生成商品推荐"""
    context = f"顾客信息：{customer_info}\n\n可选商品：{products_info}"
    prompt = "基于以上顾客信息，从可选商品中挑选5个最适合的推荐商品，每个商品说明推荐理由。格式：商品名 - 推荐理由"
    return chat(build_messages(prompt, context))

def generate_marketing(customer_info, activity_type):
    """生成营销文案"""
    context = f"顾客信息：{customer_info}"
    prompt = f"为该顾客生成一条{activity_type}营销文案，要求亲切有吸引力，不超过100字，可直接用于短信推送。"
    return chat(build_messages(prompt, context))

def generate_restock_suggestion(product_info, sales_history):
    """生成补货建议"""
    context = f"商品信息：{product_info}\n销售历史：{sales_history}"
    prompt = "基于该商品当前库存和历史销量，给出补货建议，包括建议补货数量和理由。"
    return chat(build_messages(prompt, context))

def analyze_sales_query(question, sales_data):
    """自然语言销售数据分析"""
    context = f"销售数据：{sales_data}"
    prompt = f"基于以上销售数据回答问题：{question}\n请给出具体数字和分析结论。"
    return chat(build_messages(prompt, context))
