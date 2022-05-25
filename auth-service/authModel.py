from jwtHandler import generateJwtToken
from userModel import checkPasswordInDatabase, hashAndRegisterUser


def registerUser(username, password):
    # User successfully register
    if hashAndRegisterUser(username, password):
        # Generate token for user
        token = generateJwtToken(username, False)
        return token
    # User can't register
    return None

def loginUser(username, password):
    valid, isAdmin = checkPasswordInDatabase(username, password)
    # User give valid credentials
    if valid:
        # Generate token for user
        token = generateJwtToken(username, isAdmin)
        return token
    # User can't login
    return None