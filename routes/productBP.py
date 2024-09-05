from flask import Blueprint
from controllers.productController import find_all, save, List_products, add_product, update_product, delete_product

product_blueprint = Blueprint('product_bp', __name__)
product_blueprint.route('/', methods=['POST'])(save)
product_blueprint.route('/', methods=['GET'])(find_all)

product_blueprint.route('/', methods=['POST'])(add_product)
product_blueprint.route('/update', methods=['GET'])(update_product)
product_blueprint.route('/', methods=['GET'])(List_products)
product_blueprint.route('/search', methods=['DELETE'])(delete_product)
