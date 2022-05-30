import string
import time
import jwt
import os




def generateJwtToken(username, isAdmin) -> string:
    payload_data = {
        "username": username,
        "isAdmin": isAdmin,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "nbf": int(time.time()) - 10,
    }
    return jwt.encode(payload_data, os.environ.get('AUTHSECRET'), algorithm="HS256")