from flask import Blueprint
from controllers.accountController import save, find_all, find_all_paginate, login

account_blueprint = Blueprint('account_bp', __name__)

account_blueprint.route('/', methods=['POST'])(save)
account_blueprint.route('/', methods=['GET'])(find_all)
account_blueprint.route('/paginate', methods=['GET'])(find_all_paginate)
account_blueprint.route('/login', methods=['POST'])(login)

