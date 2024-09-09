from flask import Flask
from flask_cors import CORS
from database import db
from models.schemas import ma
from limiter import limiter
from caching import cache
from flask_swagger_ui import get_swaggerui_blueprint

# from models.customer import Customer
# from models.product import Product
# from models.order import Order

from routes.customerBP import customer_blueprint
from routes.productBP import product_blueprint
from routes.orderBP import order_blueprint
from routes.accountBP import account_blueprint

#SWAGGER
SWAGGER_URL = '/api/docs' # URL endpoint for Swagger API documentation
API_URL = '/static/swagger.yaml'

swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name':"E-commerce API"})

def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    CORS(app)

    print('Running')
    blueprint_config(app)
    rate_limit_config()

    return app

def blueprint_config(app):
    app.register_blueprint(customer_blueprint, url_prefix='/customers')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(account_blueprint, url_prefix='/account')
    
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

def rate_limit_config():
    limiter.init_app(app)  # Add this line to import the limiter module
    limiter.limit("100 per day")(customer_blueprint, product_blueprint, order_blueprint, account_blueprint)
    


app = create_app('ProductionConfig')
db.init_app(app)
ma.init_app(app)
limiter.init_app(app)
cache.init_app(app)


with app.app_context():
        db.drop_all()
        db.create_all()
        
        
        
        
        
