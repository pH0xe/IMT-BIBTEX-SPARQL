from unittest.mock import patch

import pytest
from authModel import register

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
        assert token == expected_token
        assert msg == expected_msg
