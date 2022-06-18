import time
from unittest.mock import patch
import jwt
import pytest

from jwtHandler import verify_jwt_token

class TestJwtHandler():

    @pytest.mark.parametrize('is_admin, expire_time, is_invalid, is_error', 
        [
            (False, 3600, False, False),                                 # Correct token (no admin)
            (True, 3600, False, False),                                  # Correct token (admin)
            (False, 2, False, True),                                     # Token expired
            (False, 3600, True, True)                                    # invalid token 
        ],
        ids=['correct_token_no_admin', 'correct_token_admin', 'token_expired', 'invalid_token']
    )
    @patch('jwtHandler.os.environ.get')
    def test_jwt_token(self, mock_env, is_admin, expire_time, is_invalid, is_error):
        mock_env.return_value = "SECRET"
        payload_data = None
        token = 'Invalid_token'
        if not is_invalid:
            payload_data = {
                "username": 'username',
                "isAdmin": is_admin,
                "iat": int(time.time()),
                "exp": int(time.time()) + expire_time,
                "nbf": int(time.time()) - 10,
            }
            token = jwt.encode(payload_data, 'SECRET', algorithm="HS256")
            time.sleep(5)

        error, payload = verify_jwt_token(token)
        assert error == is_error
        if not is_error:
            assert payload_data['username'] == payload['username']
            assert payload_data['isAdmin'] == payload['isAdmin']
            assert payload_data['iat'] == payload['iat']
            assert payload_data['exp'] == payload['exp']
            assert payload_data['nbf'] == payload['nbf']
        else:
            assert 'error' in payload