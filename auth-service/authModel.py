from databaseManager import DatabaseManager
from jwtHandler import generate_jwt_token


def register(username, password):
    token = None
    database_manager = DatabaseManager()
    success, message = database_manager.hash_and_register_user(username, password)
    # User successfully register
    if success:
        # Generate token for user
        token = generate_jwt_token(username, False)
    database_manager.close_connection()
    # return none if User can't register
    return token, message

def login(username, password):
    token = None
    database_manager = DatabaseManager()
    valid, is_admin = database_manager.check_password_in_database(username, password)
    # User give valid credentials
    if valid:
        # Generate token for user
        token = generate_jwt_token(username, is_admin)
    database_manager.close_connection()
    # User can't login
    return token