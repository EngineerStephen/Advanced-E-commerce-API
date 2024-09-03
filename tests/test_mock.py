import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
from werkzeug.security import generate_password_hash
from services import customerService

class TestLoginCustomer(unittest.TestCase):

    @patch('services.customerService.db.session.execute')
    def test_login_customer(self, mock_customer):
        #set up the return value for our mock object
        faker           = Faker()
        mock_user       = MagicMock() #simulate a user retrieved from the database
        mock_user.id    = 1
        mock_user.roles = [MagicMock(role_name='admin'), MagicMock(role_name='user')]
        password = faker.password()
        mock_user.username = faker.user_name()
        mock_user.password = generate_password_hash(password)
        mock_customer.return_value.scalar_one_or_none.return_value = mock_user

        response = customerService.login(mock_user.username, password)

        self.assertEqual(response['status'], 'fail')

if __name__ == '__main__':
    unittest.main()