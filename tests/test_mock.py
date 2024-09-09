import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
from werkzeug.security import generate_password_hash
from services import customerService
from services import accountService
from services import productService
from services import orderService

class TestLoginCustomer(unittest.TestCase):

    @patch('services.customerService.db.session.execute')
    def test_login_customer(self, mock_customer):
        faker           = Faker()
        mock_user       = MagicMock() 
        mock_user.id    = 1
        mock_user.roles = [MagicMock(role_name='admin'), MagicMock(role_name='user')]
        password = faker.password()
        mock_user.username = faker.user_name()
        mock_user.password = generate_password_hash(password)
        mock_customer.return_value.scalar_one_or_none.return_value = mock_user

        response = customerService.login(mock_user.username, password)

        self.assertEqual(response['status'], 'fail')
 
 
        
        
    @patch('services.accountService.db.session.execute')
    def test_login_account(self, mock_account):
        faker           = Faker()
        mock_user       = MagicMock() 
        mock_user.id    = 1
        mock_user.roles = [MagicMock(role_name='admin'), MagicMock(role_name='user')]
        password = faker.password()
        mock_user.username = faker.user_name()
        mock_user.password = generate_password_hash(password)
        mock_account.return_value.scalar_one_or_none.return_value = mock_user

        response = accountService.login(mock_user.username, password)

        self.assertEqual(response['status'], 'fail')
    
 
 
    

    @patch('services.accountService.db.session.execute')
    def test_login_account(self, mock_account):
        faker = Faker()
        mock_account = MagicMock()
        mock_account.id = 1
        mock_account.roles = [MagicMock(role_name='admin'), MagicMock(role_name='user')]
        password = faker.password()
        mock_account.password = generate_password_hash(password)
        mock_account.return_value.scalar_one_or_none.return_value = mock_account

        response = accountService.login(mock_account.username, password)

        self.assertEqual(response['status'], 'fail')
        
        
        
    @patch('services.productService.db.session.execute')
    def test_login_product(self, mock_product):
        faker = Faker()
        mock_product = MagicMock()
        mock_product.id = 1
        mock_product.roles = [MagicMock(role_name='admin'), MagicMock(role_name='user')]
        password = faker.password()
        mock_product.password = generate_password_hash(password)
        mock_product.return_value.scalar_one_or_none.return_value = mock_product

        response = productService.login(mock_product.username, password)
        
        
    @patch('services.orderService.db.session.execute')
    def test_login_order(self, mock_order):
        faker = Faker() 
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.roles = [MagicMock(role_name='admin'), MagicMock(role_name='user')]
        password = faker.password()
        mock_order.password = generate_password_hash(password)
        mock_order.return_value.scalar_one_or_none.return_value = mock_order
        
        response = orderService.login(mock_order.username, password)

        self.assertEqual(response['status'], 'fail')

    

if __name__ == '__main__':
    unittest.main()