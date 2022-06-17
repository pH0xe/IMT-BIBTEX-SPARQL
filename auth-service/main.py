from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

from authModel import login, register

DEBUG = True

load_dotenv()
app = Flask("auth-api")

@app.route("/api/login", methods=["POST"])
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

@app.route("/api/register", methods=["POST"])
def register_endpoint():
    # TODO: check if current user is logged in
    password = request.form.get("password")
    login_user = request.form.get("login")
    if login_user is not None and password is not None:
        token, message = register(login_user, password)
        if token is not None:
            return jsonify({"success": "User registered", "token": token}), 200
        return jsonify({"error": f"Unable to register user : {message}"}), 400
    return jsonify({"error": "Missing parameters"}), 400

if __name__ == "__main__":
    app.run(host=os.environ.get('FLASK_HOST'), port=os.environ.get('FLASK_PORT'), debug=DEBUG)