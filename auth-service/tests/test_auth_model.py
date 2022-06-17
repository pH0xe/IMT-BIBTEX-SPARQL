from unittest.mock import patch

import pytest
from authModel import login, register

class TestAuthModel():

    @pytest.mark.parametrize('register_success, register_msg, expected_token, expected_msg', 
        [
            (True, None, 'token', None),                                # User successfully register
            (False, 'User already exist', None, 'User already exist'),  # User can't register (already exist)
            (False, 'Error', None, 'Error')                             # User can't register (Unknown error)
        ],
        ids=['register_success', 'register_failed_user_already_exist', 'register_failed_unknown_error']
    )
    @patch('authModel.DatabaseManager')
    @patch('authModel.generate_jwt_token')
    def test_register(self, mock_token, mock_db, register_success, register_msg, expected_token, expected_msg):
        mock_db.return_value.hash_and_register_user.return_value = register_success, register_msg
        mock_token.return_value = "token"
        token, msg = register("test", "test")

        # DB should be called only once
        assert mock_db.return_value.hash_and_register_user.called == True
        assert mock_db.return_value.hash_and_register_user.call_count == 1

        # Token should be generated only once and only if user successfully register
        assert mock_token.called == register_success
        if register_success:
            assert mock_token.call_count == 1
        
        # Check if token is correct and if message is correct
        assert token == expected_token
        assert msg == expected_msg

    @pytest.mark.parametrize('expected_token, login_name, login_password, check_password_success, check_password_admin', 
        [
            (None, None, 'pass', False, None),                          # Password or username is empty
            (None, 'wrongName', 'pass', False, False),                  # Password or username is incorrect
            ('token', 'log', 'pass', True, False),                     # Everything is correct (non admin)
            ('token', 'admin', 'pass', True, True)                     # Everything is correct (admin)
        ],
        ids=['empty_field', 'wrong_credential', 'login_success', 'login_success_admin']
    )
    @patch('authModel.DatabaseManager')
    @patch('authModel.generate_jwt_token')
    def test_login(self, mock_token, mock_db, expected_token, login_name, login_password, check_password_success, check_password_admin):
        mock_db.return_value.check_password_in_database.return_value = check_password_success, check_password_admin
        mock_token.return_value = "token"
        token = login(login_name, login_password)

        # DB should be called only once
        assert mock_db.return_value.check_password_in_database.called == True
        assert mock_db.return_value.check_password_in_database.call_count == 1

        # Token should be generated only once and only if user successfully register
        assert mock_token.called == check_password_success
        if check_password_success:  
            assert mock_token.call_count == 1
        
        # Check if token is correct 
        assert token == expected_token
