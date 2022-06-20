import os
from typing import Tuple
import jwt

def verify_jwt_token(token: str) -> Tuple[bool, dict]:
    """
    It takes a JWT token as a string, and returns a tuple of a boolean and a dictionary. The boolean is
    True if the token is valid, and False if it is not. The dictionary contains the decoded token if the
    token is valid, and an error message if it is not
    
    :param token: The token to be verified
    :type token: str
    :return: A tuple of a boolean and a dictionary.
    """
    try:
        return True, jwt.decode(token, os.environ.get('AUTHSECRET'), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False, {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return False, {"error": "Invalid token"}
    except Exception as e:
        return False, {"error": f"Unable to decode token : {e}"}