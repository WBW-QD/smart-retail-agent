from database import SessionLocal, engine
from models import Product, Customer, Order, Base
import random
from datetime import datetime, timedelta

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Product).count() > 0:
        db.close()
        return
    seed_products(db)
    seed_customers(db)
    seed_orders(db)
    db.close()

def seed_products(db):
    products = [
        ("纯牛奶250ml*12盒", "乳品饮料", 49.9, 120, 85),
        ("酸奶风味发酵乳", "乳品饮料", 12.8, 200, 150),
        ("矿泉水550ml*24瓶", "乳品饮料", 29.9, 300, 220),
        ("可乐330ml*24罐", "乳品饮料", 59.9, 80, 130),
        ("薯片原味70g", "休闲零食", 8.5, 150, 95),
        ("巧克力威化饼", "休闲零食", 15.9, 60, 110),
        ("坚果混合装250g", "休闲零食", 39.9, 45, 70),
        ("方便面五连包", "休闲零食", 19.9, 180, 140),
        ("大米5kg", "粮油调味", 45.0, 90, 55),
        ("食用油5L", "粮油调味", 79.9, 30, 40),
        ("生抽酱油500ml", "粮油调味", 12.9, 110, 65),
        ("食盐加碘400g", "粮油调味", 3.5, 250, 80),
        ("卫生纸10卷装", "日用百货", 22.9, 70, 90),
        ("洗衣液2kg", "日用百货", 35.9, 50, 60),
        ("牙膏薄荷味", "日用百货", 14.9, 130, 85),
        ("洗发水500ml", "日用百货", 49.9, 40, 45),
        ("苹果红富士5斤", "生鲜水果", 29.9, 25, 120),
        ("香蕉1kg", "生鲜水果", 6.9, 80, 150),
        ("猪后腿肉500g", "生鲜水果", 28.0, 15, 90),
        ("鸡蛋30枚装", "生鲜水果", 25.9, 60, 130),
    ]
    for name, category, price, stock, sales in products:
        db.add(Product(name=name, category=category, price=price,
                        stock=stock, sales_30d=sales, image_url=""))
    db.commit()

def seed_customers(db):
    names = ["张伟", "李娜", "王芳", "刘洋", "陈静", "杨磊", "赵敏", "黄强", "周婷", "吴超"]
    categories = ["乳品饮料", "休闲零食", "粮油调味", "日用百货", "生鲜水果"]
    tags_pool = ["高频购买", "价格敏感", "品质追求", "新客", "沉睡客户", "会员活跃", "家庭用户", "单身白领"]
    for i, name in enumerate(names):
        pref = random.choice(categories)
        total = round(random.uniform(200, 5000), 2)
        count = random.randint(3, 50)
        cust_tags = random.sample(tags_pool, k=random.randint(1, 3))
        days_ago = random.randint(0, 30)
        last = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        db.add(Customer(
            name=name,
            phone=f"138{random.randint(10000000, 99999999)}",
            total_spent=total,
            order_count=count,
            preferred_category=pref,
            last_purchase=last,
            tags=",".join(cust_tags)
        ))
    db.commit()

def seed_orders(db):
    customers = db.query(Customer).all()
    products = db.query(Product).all()
    for _ in range(80):
        c = random.choice(customers)
        p = random.choice(products)
        qty = random.randint(1, 5)
        amount = round(p.price * qty, 2)
        days_ago = random.randint(0, 30)
        order_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        db.add(Order(customer_id=c.id, product_id=p.id, quantity=qty,
                      amount=amount, order_date=order_date))
    db.commit()
