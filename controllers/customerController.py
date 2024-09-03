from flask import Flask, request, jsonify
from models.schemas.customerSchema import customer_schema, customers_schema
from services import customerService #dont import the individual function, import the module as a whole
from flask_marshmallow import Marshmallow 
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, admin_required
from mysql.connector import Error
from connection import connect_db


# ======================================================================================================
def login():
    try:
        credentials = request.json
        token = customerService.login(credentials['username'], credentials['password'])
    except KeyError:
        return jsonify({'messages':'Invalid payload, expecting username and password'}), 401
    
    if token:
        return jsonify(token), 200
    else:
        return jsonify({'messages':'Invalid username or password'}), 401
# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def save(): #name the controller will always be the same as the service function

    try:
        #try to validate the incoming data, and deserialize
        customer_data = customer_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer_saved = customerService.save(customer_data)
    return customer_schema.jsonify(customer_data), 201


# ======================================================================================================

@token_required
@cache.cached(timeout=60)
@admin_required
def find_all():
    all_customers = customerService.find_all()
    return customers_schema.jsonify(all_customers),200

# ======================================================================================================
@cache.cached(timeout=60)
@admin_required
def find_all_paginate():
    page = int(request.args.get('page'))
    per_page = int(request.args.get('per_page'))
    customers = customerService.find_all_paginate(page, per_page)
    return customers_schema.jsonify(customers), 200


# ======================================================================================================

@token_required
@cache.cached(timeout=60)
@admin_required
def add_customer():
    try: 
        customer_data = customer_schema.load(request.json)
        print(request.json, "JSON DATA FROM REQUEST")
        print(customer_data, "CUSTOMER DATA")
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed."}), 500
        
        cursor = conn.cursor()
        name = customer_data['name']
        print(name)
        email = customer_data['email']
        print(email)
        phone = customer_data['phone']
        print(phone)

        new_customer = (name, email, phone)

        query = "INSERT INTO Customers(name, email, phone) VALUES(%s, %s, %s)"


        cursor.execute(query, new_customer)
        conn.commit()

        return jsonify({"message": "New customer added successfully"}), 201 
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
def read_customers():

    conn = connect_db()
    cursor = conn.cursor(dictionary=True) 
    query = "SELECT * FROM Customers"

    cursor.execute(query)

    customers = cursor.fetchall()
    print(customers)

    cursor.close()    
    conn.close()


    return customers_schema.jsonify(customers) 


# ======================================================================================================

@token_required
@cache.cached(timeout=60)
@admin_required
def update_customer(id):
    try: 
    
        customer_data = customer_schema.load(request.json)
        print(customer_data)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database Connection Failed"}), 500
        
        cursor = conn.cursor()

        name = customer_data['name']
        email = customer_data['email']
        phone = customer_data['phone']
        #                                    
        updated_customer = (name, email, phone, id)


        query = "UPDATE Customers SET name = %s, email = %s, phone = %s WHERE customer_id = %s"


        cursor.execute(query, updated_customer)
        conn.commit()


        return jsonify({"message": "Customer details updated successfully"}), 200
    
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
def delete_customer(id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"message": "Database connection failed"}), 500
        cursor = conn.cursor()
        customer_to_remove = (id,)


        query = "SELECT * FROM Customers WHERE customer_id = %s"
        cursor.execute(query, customer_to_remove)
        customer = cursor.fetchone()
        print(customer)
        if not customer:
            return jsonify({"message": "Customer not found"}), 404
        

        query = "SELECT * FROM Orders WHERE customer_id = %s"
        cursor.execute(query, customer_to_remove)

        customer_orders = cursor.fetchall()

        if customer_orders:
            return jsonify({"message": "Cannot delete customer with associated orders. "}), 403 #FORBID the user from deleting a customer with orders
        

        query = "DELETE FROM Customers WHERE customer_id = %s"
        cursor.execute(query, customer_to_remove)
        conn.commit()

        return jsonify({"message": "Customer removed successfully"}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()