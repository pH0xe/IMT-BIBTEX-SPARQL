import logging
import os
import time

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

DEBUG = True

load_dotenv()
app = Flask(__name__)

# send bib file to server
@app.route("/api/bibtex", methods=["POST"])
def login():
    if 'file' not in request.files:
        logging.warning('no file part')
        return jsonify({'message': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        logging.warning('No file selected for uploading')
        return jsonify({'message': 'No file selected for uploading'}), 400
    filename = secure_filename(file.filename)
    print(file)
    print(type(file))
    print(file.read())

    password = request.form.get("password")
    loginUser = request.form.get("login")
    if loginUser is not None and password is not None:
        token = loginUser(loginUser, password)
        if token is not None:
            return jsonify({"success": "User logged in", "token": token}), 200
        else:
            return jsonify({"error": "Wrong password or username"}), 400

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, handlers=[ 
        logging.StreamHandler(), 
        logging.FileHandler('logs/log-'+ str(int(time.time())) + '.log') 
    ])
    app.run(host=os.environ.get('FLASK_HOST'), port=os.environ.get('FLASK_PORT'), debug=DEBUG)
