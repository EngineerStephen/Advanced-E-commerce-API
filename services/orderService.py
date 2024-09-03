from database import db 
from models.order import Order
from models.customer import Customer
from models.product import Product
from sqlalchemy import select
from datetime import date

def save(order_data):
    
    new_order = Order(date=date.today(), customer_id = order_data["customer_id"])

    for item_id in order_data['products_ids']:
        query = select(Product).filter(Product.id == item_id)
        item = db.session.execute(query).scalar()
        print(item)
        new_order.products.append(item)

    db.session.add(new_order)
    db.session.commit()

    db.session.refresh(new_order)
    return new_order

def find_all():
    query = select(Order)
    all_orders = db.session.execute(query).scalars().all()
    return all_orders

def find_by_id(id):
    query = select(Order).where(Order.id == id)
    order = db.session.execute(query).scalars().all()
    return order

def find_by_customer_id(id):
    query = select(Order).where(Order.customer_id == id)
    orders = db.session.execute(query).scalars().all()
    return orders

def find_by_customer_email(email):
    query = select(Order).join(Customer).where(Customer.id == Order.customer_id).filter(Customer.email == email)
    orders = db.session.execute(query).scalars().all()
    return orders


def place_order(order_data):
    
    new_order = Order(date=date.today(), customer_id = order_data["customer_id"])

    for item_id in order_data['products_ids']:
        query = select(Product).filter(Product.id == item_id)
        item = db.session.execute(query).scalar()
        print(item)
        new_order.products.append(item)

def retrieve_order(id):
    query = select(Order).where(Order.id == id)
    order = db.session.execute(query).scalars().all()
    return order
