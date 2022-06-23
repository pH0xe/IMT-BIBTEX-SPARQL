from authModel import change_password, get_users, login, register, remove_user
from databaseManager import init_db
from jwtHandler import verify_jwt_token
from utils import check_environnement
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from psycopg2 import OperationalError
from flask_cors import CORS
import logging
import time
import sys

DEBUG = True

load_dotenv()
check_environnement()

app = Flask("auth-api")
CORS(app)

init_db()

@app.route("/api/auth/login", methods=["POST"])
def login_endpoint():
    password = request.form.get("password")
    login_user = request.form.get("login")
    if login_user is not None and password is not None:
        token = login(login_user, password)
        if token is not None:
            return jsonify({"success": "User logged in", "token": token}), 200
        else:
            return jsonify({"error": "Wrong password or username"}), 401      
    return jsonify({"error": "Missing parameters"}), 400

@app.route("/api/auth/register", methods=["POST"])
def register_endpoint():
    auth_token = request.headers.get("Authorization")
    if auth_token is not None:
        error, payload = verify_jwt_token(auth_token)
        if error :
            return jsonify(payload), 401
    else:
        return jsonify({"error": "Missing authentification token"}), 401

    password = request.form.get("password")
    login_user = request.form.get("login")
    if login_user is not None and password is not None:
        token, message = register(login_user, password)
        if token is not None:
            return jsonify({"success": "User registered", "token": token}), 200
        return jsonify({"error": f"Unable to register user : {message}"}), 400
    return jsonify({"error": "Missing parameters"}), 400

@app.route("/api/auth/password", methods=["PUT"])
def change_password_endpoint():
    auth_token = request.headers.get("Authorization")
    if auth_token is not None:
        error, payload = verify_jwt_token(auth_token)
        if error :
            return jsonify(payload), 401
    else:
        return jsonify({"error": "Missing authentification token"}), 401
    
    current_password = request.form.get("currentPassword")
    new_password = request.form.get("newPassword")
    username = payload["username"]
    token, message = change_password(username, current_password, new_password)
    if token is not None:
        return jsonify({"success": "Password changed", "token": token}), 200
    return jsonify({"error": f"Unable to change password : {message}"}), 400

@app.route("/api/auth/delete/<id>", methods=["DELETE"])
def delete_user_endpoint(id):
    auth_token = request.headers.get("Authorization")
    if auth_token is not None:
        error, payload = verify_jwt_token(auth_token)
        if error :
            return jsonify(payload), 401
    else:
        return jsonify({"error": "Missing authentification token"}), 401
    try:
        success, code = remove_user(id)
        if success:
            return jsonify({"success": "User deleted"}), 200
        if code == 404:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"error": f"Unable to remove user"}), 400
    except Exception as e:
        return jsonify({"error": f"Unable to remove user : {str(e)}"}), 400

@app.route("/api/auth/users", methods=["GET"])
def get_users_endpoint():
    auth_token = request.headers.get("Authorization")
    if auth_token is not None:
        error, payload = verify_jwt_token(auth_token)
        if error :
            return jsonify(payload), 401
    else:
        return jsonify({"error": "Missing authentification token"}), 401
    try:
        users = get_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": f"Unable to query users : {str(e)}"}), 400    

def create_app():
    db_is_initialized = False
    tries = 0
    max_tries = 3
    wait_time = 5
    while not db_is_initialized and tries < max_tries:
        tries += 1

        try:
            init_db()
        except OperationalError:
            logging.error("Unable to connect to the database")
            if tries < max_tries:
                logging.error(f"Retrying in {wait_time}s")
                time.sleep(wait_time)
            else:
                logging.error("Too many tries, shutting down.")
                sys.exit(1)
        else:
            db_is_initialized = True

    return app
