from database import db 
from models.customer import Customer 
from utils.util import encode_token

from sqlalchemy import select

def login(username, password): 
    query = select(Customer).where(Customer.username == username)
    customer = db.session.execute(query).scalar_one_or_none() 
    if customer and customer.password == password:
        auth_token = encode_token(customer.id, customer.role.role_name)

        response = {
            "status":"success",
            "message":"Successfully Logged In",
            "auth_token": auth_token
        }
        return response
    else:
        response = {
            "status": "fail",
            "message": "Invalid username or password"
        }
        return response


def save(customer_data):
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], password=customer_data['password'], phone=customer_data['phone'], username=customer_data['username'])
    db.session.add(new_customer)
    db.session.commit()

    db.session.refresh(new_customer)
    return new_customer

def find_all():
    query = select(Customer)
    all_customers = db.session.execute(query).scalars().all()
    return all_customers

def find_all_paginate(page, per_page):
    customers = db.paginate(select(Customer), page = page, per_page = per_page)
    return customers


def add_customer(customer_data):
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], password=customer_data['password'], phone=customer_data['phone'], username=customer_data['username'])
    db.session.add(new_customer)
    db.session.commit()

    db.session.refresh(new_customer)
    return new_customer

def read_customer(customer_data):
    query = select(Customer).where(Customer.id == customer_data['id'])
    customer = db.session.execute(query).scalar_one_or_none()
    return customer

def update_customer(customer_data):
    query = select(Customer).where(Customer.id == customer_data['id'])
    customer = db.session.execute(query).scalar_one_or_none()
    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.password = customer_data['password']
    customer.phone = customer_data['phone']
    customer.username = customer_data['username']
    db.session.commit()
    return customer

def delete_customer(customer_data):
    query = select(Customer).where(Customer.id == customer_data['id'])
    customer = db.session.execute(query).scalar_one_or_none()
    db.session.delete(customer)
    db.session.commit()
    return customer


