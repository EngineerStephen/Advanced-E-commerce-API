from flask import jsonify, request
from models.schemas.orderSchema import order_schema, orders_schema
from marshmallow import ValidationError
from services import orderService
from utils.util import user_token_wrapper
# from connection import connect_db
from utils.util import token_required, admin_required
from caching import cache


@token_required
@cache.cached(timeout=60)
@admin_required
def save():
     try:
          order_data = order_schema.load(request.json)
     except ValidationError as err:
               return jsonify(err.message), 400
     
     new_order = orderService.save(order_data)
     return order_schema.jsonify(new_order), 201




@token_required
@cache.cached(timeout=60)
@admin_required
def find_all():
     all_orders = orderService.find_all()
     return orders_schema.jsonify(all_orders), 200




@token_required
@cache.cached(timeout=60)
@admin_required
def find_by_id(id):
     orders = orderService.find_by_id(id)
     return orders_schema.jsonify(orders), 200

@token_required
@cache.cached(timeout=60)
@admin_required
def find_by_customer_id(id, token_id):
     if id == token_id:
          orders = orderService.find_by_customer_id(id)
     else:
          return jsonify({"message": "You can't view other peoples orders..."})
     return orders_schema.jsonify(orders), 200




@token_required
@cache.cached(timeout=60)
@admin_required
def find_by_customer_email():
     email = request.json['email']
     orders = orderService.find_by_customer_email(email)
     return orders_schema.jsonify(orders), 200

@token_required
@cache.cached(timeout=60)
@admin_required
def place_order():
          try:
               order_data = order_schema.load(request.json)
          except ValidationError as err:
               return jsonify(err.message), 400
          try: 
               new_order = orderService.place_order(order_data)
               return order_schema.jsonify(new_order), 201
          
          
@token_required
@cache.cached(timeout=60)
@admin_required         
def retrieve_order():
     order_id = request.json['order_id']
     order = orderService.retrieve_order(order_id)
     return order_schema.jsonify(order), 200