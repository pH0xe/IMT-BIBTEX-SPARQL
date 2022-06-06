import logging
import os
import time
from dotenv import load_dotenv

from flask import Flask, jsonify, request
from bibtexParser import BibtexParser

from databaseManager import DataBaseManager
from pybtex.database.input.bibtex import UndefinedMacro, DuplicateField

DEBUG = True

load_dotenv()
app = Flask("BibFileAPI")

@app.route("/api/bibtex", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        logging.warning('no file part')
        return jsonify({'message': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        logging.warning('No file selected for uploading')
        return jsonify({'message': 'No file selected for uploading'}), 400
    database_manager = DataBaseManager()
    if not database_manager.connect_to_postgres():
        return jsonify({'message': 'Could not connect to database'}), 500
    success, data = database_manager.upload_file(file)
    if not success:
        return jsonify({'message': 'Could not upload file'}), 500

    return convert_process(data)

@app.route("/api/bibtex/<id>", methods=["GET"])
def restore_file(id):
    database_manager = DataBaseManager()
    if not database_manager.connect_to_postgres():
        return jsonify({'message': 'Could not connect to database'}), 500
    data = database_manager.get_data_by_id(id)
    return convert_process(data)


@app.route("/api/bibtex", methods=["GET"])
def get_all_files():
    database_manager = DataBaseManager()
    if not database_manager.connect_to_postgres():
        return jsonify({'message': 'Could not connect to database'}), 500
    return jsonify(database_manager.select_all_file())

def convert_process(data: bytes):
    parser = BibtexParser()
    success, msg = parser.parse_file(file = data)
    if not success:
        return jsonify({'message': msg}), 500
    success, msg = parser.convert_file()
    if not success:
        return jsonify({'message': msg}), 500
    success, msg = parser.save_rdf()
    if not success:
        return jsonify({'message': msg}), 500
    return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, handlers=[ 
        logging.StreamHandler(), 
        logging.FileHandler('logs/log-'+ str(int(time.time())) + '.log') 
    ])
    app.run(host=os.environ.get('FLASK_HOST'), port=os.environ.get('FLASK_PORT'), debug=DEBUG)
