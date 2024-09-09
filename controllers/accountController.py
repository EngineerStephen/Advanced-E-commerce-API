from flask import Flask, request, jsonify
from models.schemas.accountSchema import account_schema, accounts_schema
from services import accountService  # Don't import the individual function, import the module as a whole
from flask_marshmallow import Marshmallow 
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, admin_required
from mysql.connector import Error
# from connection import connect_db


# ======================================================================================================
def login():
    try:
        credentials = request.json
        token = accountService.login(credentials['username'], credentials['password'])
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting username and password'}), 401
    
    if token:
        return jsonify(token), 200
    else:
        return jsonify({'messages': 'Invalid username or password'}), 401
# ======================================================================================================
@token_required
@admin_required
def save():  # Name the controller the same as the service function

    try:
        # Try to validate the incoming data and deserialize
        account_data = account_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    account_saved = accountService.save(account_data)
    return account_schema.jsonify(account_data), 201


# ======================================================================================================

@token_required
@cache.cached(timeout=60)
@admin_required
def find_all():
    all_accounts = accountService.find_all()
    return accounts_schema.jsonify(all_accounts), 200

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def find_all_paginate():
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))
    accounts = accountService.find_all_paginate(page, per_page)
    return accounts_schema.jsonify(accounts), 200


# ======================================================================================================
@token_required
@admin_required
def add_account():
    try: 
        account_data = account_schema.load(request.json)
        print(request.json, "JSON DATA FROM REQUEST")
        print(account_data, "ACCOUNT DATA")
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed."}), 500
        
        cursor = conn.cursor()
        name = account_data['name']
        print(name)
        email = account_data['email']
        print(email)
        phone = account_data['phone']
        print(phone)

        new_account = (name, email, phone)

        query = "INSERT INTO Accounts(name, email, phone) VALUES(%s, %s, %s)"


        cursor.execute(query, new_account)
        conn.commit()

        return jsonify({"message": "New account added successfully"}), 201 
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def read_accounts():

    conn = connect_db()
    cursor = conn.cursor(dictionary=True) 
    query = "SELECT * FROM Accounts"

    cursor.execute(query)

    accounts = cursor.fetchall()
    print(accounts)

    cursor.close()    
    conn.close()


    return accounts_schema.jsonify(accounts) 


# ======================================================================================================
@token_required
@admin_required
def update_account(id):
    try: 
    
        account_data = account_schema.load(request.json)
        print(account_data)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database Connection Failed"}), 500
        
        cursor = conn.cursor()

        name = account_data['name']
        email = account_data['email']
        phone = account_data['phone']
        #                                    
        updated_account = (name, email, phone, id)


        query = "UPDATE Accounts SET name = %s, email = %s, phone = %s WHERE account_id = %s"


        cursor.execute(query, updated_account)
        conn.commit()


        return jsonify({"message": "Account details updated successfully"}), 200
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:

        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
            
# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def delete_account(id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"message": "Database connection failed"}), 500
        cursor = conn.cursor()
        account_to_remove = (id,)


        query = "SELECT * FROM Accounts WHERE account_id = %s"
        cursor.execute(query, account_to_remove)
        account = cursor.fetchone()
        print(account)
        if not account:
            return jsonify({"message": "Account not found"}), 404
        

        query = "SELECT * FROM Orders WHERE account_id = %s"
        cursor.execute(query, account_to_remove)

        account_orders = cursor.fetchall()

        if account_orders:
            return jsonify({"message": "Cannot delete account with associated orders."}), 403  # FORBID the user from deleting an account with orders
        

        query = "DELETE FROM Accounts WHERE account_id = %s"
        cursor.execute(query, account_to_remove)
        conn.commit()

        return jsonify({"message": "Account removed successfully"}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
