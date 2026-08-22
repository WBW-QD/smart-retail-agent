from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import json

from database import get_db, engine
from models import Product, Customer, Order, ChatHistory, Base
from mock_data import init_db
import ollama_client

app = FastAPI(title="智慧零售营运Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    init_db()

# ============ 请求模型 ============
class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = ""

class RecommendRequest(BaseModel):
    customer_id: int

class MarketingRequest(BaseModel):
    customer_id: int
    activity_type: str = "会员促销"

class RestockRequest(BaseModel):
    product_id: int

class SalesQueryRequest(BaseModel):
    question: str

# ============ 通用对话 ============
@app.post("/api/chat")
def api_chat(req: ChatRequest, db: Session = Depends(get_db)):
    messages = ollama_client.build_messages(req.message, req.context)
    # 保存用户消息
    db.add(ChatHistory(role="user", content=req.message))
    db.commit()
    result = ollama_client.chat(messages)
    # 保存AI回复
    db.add(ChatHistory(role="assistant", content=result))
    db.commit()
    return {"reply": result}

# ============ 商品推荐 ============
@app.post("/api/recommend")
def api_recommend(req: RecommendRequest, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == req.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="顾客不存在")
    products = db.query(Product).all()
    cust_info = f"姓名:{customer.name}, 总消费:{customer.total_spent}元, 订单数:{customer.order_count}, 偏好品类:{customer.preferred_category}, 标签:{customer.tags}"
    prod_info = "\n".join([f"[{p.id}] {p.name} - {p.category} - ¥{p.price} (库存:{p.stock})" for p in products])
    result = ollama_client.generate_recommendation(cust_info, prod_info)
    return {"customer": cust_info, "recommendation": result}

# ============ 顾客画像 ============
@app.get("/api/customer/profile")
def api_customer_profile(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="顾客不存在")
    orders = db.query(Order).filter(Order.customer_id == customer_id).all()
    avg_order = round(customer.total_spent / customer.order_count, 2) if customer.order_count else 0
    return {
        "id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "total_spent": customer.total_spent,
        "order_count": customer.order_count,
        "avg_order": avg_order,
        "preferred_category": customer.preferred_category,
        "last_purchase": customer.last_purchase,
        "tags": customer.tags.split(",") if customer.tags else [],
        "order_history": [{"product_id": o.product_id, "quantity": o.quantity, "amount": o.amount, "date": o.order_date} for o in orders]
    }

@app.get("/api/customers")
def api_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return [{"id": c.id, "name": c.name, "total_spent": c.total_spent,
             "order_count": c.order_count, "preferred_category": c.preferred_category,
             "tags": c.tags} for c in customers]

# ============ 营销文案 ============
@app.post("/api/customer/marketing")
def api_marketing(req: MarketingRequest, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == req.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="顾客不存在")
    cust_info = f"姓名:{customer.name}, 总消费:{customer.total_spent}元, 偏好品类:{customer.preferred_category}, 标签:{customer.tags}"
    result = ollama_client.generate_marketing(cust_info, req.activity_type)
    return {"customer_name": customer.name, "marketing_text": result}

# ============ 库存管理 ============
@app.get("/api/inventory")
def api_inventory(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    result = []
    for p in products:
        warning = p.stock < 50
        result.append({
            "id": p.id, "name": p.name, "category": p.category,
            "price": p.price, "stock": p.stock, "sales_30d": p.sales_30d,
            "low_stock": warning
        })
    return result

@app.post("/api/inventory/restock")
def api_restock(req: RestockRequest, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == req.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    orders = db.query(Order).filter(Order.product_id == req.product_id).all()
    prod_info = f"商品:{product.name}, 品类:{product.category}, 价格:¥{product.price}, 当前库存:{product.stock}, 近30天销量:{product.sales_30d}"
    sales_info = "\n".join([f"{o.order_date}: 售出{o.quantity}件, 金额¥{o.amount}" for o in orders])
    result = ollama_client.generate_restock_suggestion(prod_info, sales_info)
    return {"product": prod_info, "suggestion": result}

# ============ 销售看板 ============
@app.get("/api/dashboard/sales")
def api_dashboard_sales(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    total_sales = round(sum(o.amount for o in orders), 2)
    total_orders = len(orders)
    avg_order = round(total_sales / total_orders, 2) if total_orders else 0
    # 按品类统计
    products = {p.id: p for p in db.query(Product).all()}
    category_sales = {}
    for o in orders:
        p = products.get(o.product_id)
        if p:
            category_sales[p.category] = category_sales.get(p.category, 0) + o.amount
    top_categories = sorted(category_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    # 按日期统计
    date_sales = {}
    for o in orders:
        date_sales[o.order_date] = date_sales.get(o.order_date, 0) + o.amount
    sorted_dates = sorted(date_sales.items())
    return {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "avg_order": avg_order,
        "top_categories": [{"name": k, "value": round(v, 2)} for k, v in top_categories],
        "date_trend": [{"date": d, "value": round(v, 2)} for d, v in sorted_dates]
    }

@app.post("/api/dashboard/query")
def api_dashboard_query(req: SalesQueryRequest, db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    products = {p.id: p for p in db.query(Product).all()}
    sales_data = []
    for o in orders:
        p = products.get(o.product_id)
        sales_data.append(f"日期:{o.order_date}, 商品:{p.name if p else '未知'}, 品类:{p.category if p else '未知'}, 数量:{o.quantity}, 金额:¥{o.amount}")
    data_str = "\n".join(sales_data)
    result = ollama_client.analyze_sales_query(req.question, data_str)
    return {"answer": result}

# ============ 对话历史 ============
@app.get("/api/history")
def api_history(db: Session = Depends(get_db)):
    history = db.query(ChatHistory).order_by(ChatHistory.id).all()
    return [{"role": h.role, "content": h.content, "created_at": h.created_at.isoformat() if h.created_at else ""} for h in history]

@app.delete("/api/history")
def api_clear_history(db: Session = Depends(get_db)):
    db.query(ChatHistory).delete()
    db.commit()
    return {"message": "对话历史已清空"}

# ============ 商品列表 ============
@app.get("/api/products")
def api_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [{"id": p.id, "name": p.name, "category": p.category,
             "price": p.price, "stock": p.stock, "sales_30d": p.sales_30d} for p in products]

@app.get("/api/health")
def health():
    return {"status": "ok", "model": ollama_client.OLLAMA_MODEL if hasattr(ollama_client, 'OLLAMA_MODEL') else "qwen2.5:7b"}
