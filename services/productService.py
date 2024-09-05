from models.product import Product
from database import db
from sqlalchemy import select

def save(product_data):
    new_product = Product(name=product_data['name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    db.session.refresh(new_product)

    return new_product

def find_all():
    query = select(Product)
    all_products = db.session.execute(query).scalars().all()
    return all_products

def search_product(search_term):
    query = select(Product).where(Product.name.like(f'%{search_term}%'))
    search_products = db.session.execute(query).scalars().all()
    return search_products


def add_product(product_data):
    new_product = Product(name=product_data['name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    db.session.refresh(new_product)

    return new_product

def read_product(product_data):
    query = select(Product).where(Product.id == product_data['id'])
    product = db.session.execute(query).scalar_one_or_none()
    return product

def update_product(product_data):
    query = select(Product).where(Product.id == product_data['id'])
    product = db.session.execute(query).scalar_one_or_none()
    product.name = product_data['name']
    product.price = product_data['price']
    db.session.commit()
    return product

def delete_product(product_data):
    query = select(Product).where(Product.id == product_data['id'])
    product = db.session.execute(query).scalar_one_or_none()
    db.session.delete(product)
    db.session.commit()
    return product

def List_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products