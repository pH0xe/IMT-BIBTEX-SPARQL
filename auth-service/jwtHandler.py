import string
import jwt
import os




def generateJwtToken(username, isAdmin) -> string:
    payload_data = {
        "username": username,
        "isAdmin": isAdmin
    }
    return jwt.encode(payload_data, os.environ.get('AUTHSECRET'), algorithm="HS256")