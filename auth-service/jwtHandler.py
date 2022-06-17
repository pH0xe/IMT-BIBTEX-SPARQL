import time
import jwt
import os




def generate_jwt_token(username, is_admin) -> str:
    payload_data = {
        "username": username,
        "isAdmin": is_admin,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600, # 1 hour
        "nbf": int(time.time()) - 10,
    }
    return jwt.encode(payload_data, os.environ.get('AUTHSECRET'), algorithm="HS256")