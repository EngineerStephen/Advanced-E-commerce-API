from flask import Flask, request, jsonify
from models.schemas.productSchema import product_schema, products_schema
from services import productService  # don't import the individual function, import the module as a whole
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
          token = productService.login(credentials['username'], credentials['password'])
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
def save():  # name the controller will always be the same as the service function

     try:
          # try to validate the incoming data, and deserialize
          product_data = product_schema.load(request.json)

     except ValidationError as e:
          return jsonify(e.messages), 400
     
     product_saved = productService.save(product_data)
     return product_schema.jsonify(product_data), 201

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def find_all():
     all_products = productService.find_all()
     return products_schema.jsonify(all_products), 200

# ======================================================================================================
@cache.cached(timeout=60)
@admin_required
def find_all_paginate():
     page = int(request.args.get('page'))
     per_page = int(request.args.get('per_page'))
     products = productService.find_all_paginate(page, per_page)
     return products_schema.jsonify(products), 200

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def add_product():
     try: 
          product_data = product_schema.load(request.json)
          print(request.json, "JSON DATA FROM REQUEST")
          print(product_data, "PRODUCT DATA")
     except ValidationError as e:
          print(f"Error: {e}")
          return jsonify(e.messages), 400
     
     try:
          conn = connect_db()
          if conn is None:
               return jsonify({"error": "Database connection failed."}), 500
          
          cursor = conn.cursor()
          name = product_data['name']
          print(name)
          price = product_data['price']
          print(price)
          stock = product_data['stock']
          print(stock)

          new_product = (name, price, stock)

          query = "INSERT INTO Products(name, price, stock) VALUES(%s, %s, %s)"

          cursor.execute(query, new_product)
          conn.commit()

          return jsonify({"message": "New product added successfully"}), 201 
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
def List_products():

     conn = connect_db()
     cursor = conn.cursor(dictionary=True) 
     query = "SELECT * FROM Products"

     cursor.execute(query)

     products = cursor.fetchall()
     print(products)

     cursor.close()    
     conn.close()

     return products_schema.jsonify(products) 

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def update_product(id):
     try: 
          product_data = product_schema.load(request.json)
          print(product_data)
     except ValidationError as e:
          print(f"Error: {e}")
          return jsonify(e.messages), 400
     
     try:
          conn = connect_db()
          if conn is None:
               return jsonify({"error": "Database Connection Failed"}), 500
          
          cursor = conn.cursor()

          name = product_data['name']
          price = product_data['price']
          stock = product_data['stock']
                                             
          updated_product = (name, price, stock, id)

          query = "UPDATE Products SET name = %s, price = %s, stock = %s WHERE product_id = %s"

          cursor.execute(query, updated_product)
          conn.commit()

          return jsonify({"message": "Product details updated successfully"}), 200
     
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
def delete_product(id):
     try:
          conn = connect_db()
          if conn is None:
               return jsonify({"message": "Database connection failed"}), 500
          
          cursor = conn.cursor()
          product_to_remove = (id,)

          query = "SELECT * FROM Products WHERE product_id = %s"
          cursor.execute(query, product_to_remove)
          product = cursor.fetchone()
          print(product)
          if not product:
               return jsonify({"message": "Product not found"}), 404
          
          query = "SELECT * FROM Orders WHERE product_id = %s"
          cursor.execute(query, product_to_remove)
          product_orders = cursor.fetchall()

          if product_orders:
               return jsonify({"message": "Cannot delete product with associated orders."}), 403  # FORBID the user from deleting a product with orders
          
          query = "DELETE FROM Products WHERE product_id = %s"
          cursor.execute(query, product_to_remove)
          conn.commit()

          return jsonify({"message": "Product removed successfully"}), 200

     except Error as e:
          print(f"Error: {e}")
          return jsonify({"error": "Internal Server Error"}), 500
     
     finally:
          if conn and conn.is_connected():
               cursor.close()
               conn.close()
