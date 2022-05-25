from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

from authModel import checkPasswordInDatabase, connectToPostgres, hashAndRegisterUser, registerUser

DEBUG = True

load_dotenv()
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Julien!"

@app.route("/api/login", methods=["POST"])
def login():
    password = request.form.get("password")
    loginUser = request.form.get("login")
    if loginUser is not None and password is not None:
        token = loginUser(loginUser, password)
        if token is not None:
            return jsonify({"success": "User logged in", "token": token}), 200
        else:
            return jsonify({"error": "Wrong password or username"}), 400
            
    return jsonify({"error": "Missing parameters"}), 400

@app.route("/api/register", methods=["POST"])
def register():
    password = request.form.get("password")
    loginUser = request.form.get("login")
    if loginUser is not None and password is not None:
        token = registerUser(loginUser, password)
        if token is not None:
            return jsonify({"success": "User registered", "token": token}), 200
        return jsonify({"error": "Unable to loging user"}), 400
    return jsonify({"error": "Missing parameters"}), 400

if __name__ == "__main__":
    app.run(host=os.environ.get('FLASK_HOST'), port=os.environ.get('FLASK_PORT'), debug=DEBUG)