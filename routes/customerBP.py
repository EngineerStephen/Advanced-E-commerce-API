from flask import Blueprint
from controllers.customerController import save, find_all, find_all_paginate, login, add_customer, update_customer, delete_customer, read_customer, 

customer_blueprint = Blueprint('customer_bp', __name__)

customer_blueprint.route('/', methods=['POST'])(save)
customer_blueprint.route('/', methods=['GET'])(find_all)
customer_blueprint.route('/paginate', methods=['GET'])(find_all_paginate)
customer_blueprint.route('/login', methods=['POST'])(login)

customer_blueprint.route('/', methods=['POST'])(add_customer)
customer_blueprint.route('/', methods=['GET'])(read_customer)
customer_blueprint.route('/update', methods=['POST'])(update_customer)
customer_blueprint.route('/', methods=['DELETE'])(delete_customer)

