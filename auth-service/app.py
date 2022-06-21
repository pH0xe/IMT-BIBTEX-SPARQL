from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

from flask_cors import CORS

from authModel import change_password, login, register
from databaseManager import init_db
from jwtHandler import verify_jwt_token

DEBUG = True

load_dotenv()
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
            return jsonify({"error": "Wrong password or username"}), 400      
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

@app.route("/api/auth/password", methods=["POST"])
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

if __name__ == "__main__":
    app.run(host=os.environ.get('FLASK_HOST'), port=os.environ.get('FLASK_PORT'), debug=DEBUG)