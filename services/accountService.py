from database import db
from models.account import Account 
from utils.util import encode_token

from sqlalchemy import select

def login(username, password):
    query = select(Account).where(Account.username == username)
    account = db.session.execute(query).scalar_one_or_none()
    if account and account.password == password:
        auth_token = encode_token(account.id, account.role.role_name)

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


def save(account_data):
    
    new_account = Account(name=account_data['name'], email=account_data['email'], password=account_data['password'], phone=account_data['phone'], username=account_data['username'])
    db.session.add(new_account)
    db.session.commit()

    db.session.refresh(new_account)
    return new_account

def find_all():
    query = select(Account)
    all_accounts = db.session.execute(query).scalars().all()
    return all_accounts

def find_all_paginate(page, per_page):
    accounts = db.paginate(select(Account), page = page, per_page = per_page)
    return accounts

def add_account(account_data):
    new_account = Account(name=account_data['name'], email=account_data['email'], password=account_data['password'], phone=account_data['phone'], username=account_data['username'])
    db.session.add(new_account)
    db.session.commit()

    db.session.refresh(new_account)
    return new_account

def read_account(account_data):
    query = select(Account).where(Account.id == account_data['id'])
    account = db.session.execute(query).scalar_one_or_none()
    return account

def update_account(account_data):
    query = select(Account).where(Account.id == account_data['id'])
    account = db.session.execute(query).scalar_one_or_none()
    account.name = account_data['name']
    account.email = account_data['email']
    account.password = account_data['password']
    account.phone = account_data['phone']
    account.username = account_data['username']
    db.session.commit()
    return account


def delete_account(account_data):
    query = select(Account).where(Account.id == account_data['id'])
    account = db.session.execute(query).scalar_one_or_none()
    db.session.delete(account)
    db.session.commit()
    return account