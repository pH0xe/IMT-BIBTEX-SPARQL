import time
from typing import Tuple
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

def verify_jwt_token(token: str) -> Tuple[bool, dict]:
    try:
        return False, jwt.decode(token, os.environ.get('AUTHSECRET'), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return True, {"error": "Token expired"}
    except Exception as e:
        return True, {"error": f"Unable to decode token : {e}"}
    