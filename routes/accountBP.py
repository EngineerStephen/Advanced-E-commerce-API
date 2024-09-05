from flask import Blueprint
from controllers.accountController import save, find_all, find_all_paginate, login, add_account, update_account, delete_account, read_accounts

account_blueprint = Blueprint('account_bp', __name__)

account_blueprint.route('/', methods=['POST'])(save)
account_blueprint.route('/', methods=['GET'])(find_all)
account_blueprint.route('/paginate', methods=['GET'])(find_all_paginate)
account_blueprint.route('/login', methods=['POST'])(login)
account_blueprint.route('/', methods=['POST'])(add_account)
account_blueprint.route('/update', methods=['POST'])(update_account)
account_blueprint.route('/delete', methods=['DELETE'])(delete_account)
account_blueprint.route('/', methods=['GET'])(read_accounts)
