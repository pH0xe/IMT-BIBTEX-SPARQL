from typing import Tuple
from databaseManager import DatabaseManager
from jwtHandler import generate_jwt_token


def register(username, password) -> Tuple[str, str]:
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

def login(username, password) -> str:
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

def change_password(username, current_password, new_password) -> Tuple[str, str]:
    token = None
    database_manager = DatabaseManager()
    success, message = database_manager.change_password_in_db(username, current_password, new_password)
    # User successfully change password
    if success:
        # Generate token for user
        token = generate_jwt_token(username, False)
    database_manager.close_connection()
    # return none if User can't register
    return token, message

def remove_user(id) -> Tuple[bool, int]:
    database_manager = DatabaseManager()
    if database_manager.is_super_admin(id):
        return False, 404

    success = database_manager.remove_user(id)
    database_manager.close_connection()
    return success, None

def get_users() -> list:
    database_manager = DatabaseManager()
    users = database_manager.get_all_users()
    database_manager.close_connection()
    return users