import logging
import os
import time
from dotenv import load_dotenv

from flask import Flask, jsonify, request
from flask_cors import CORS
from bibtexParser import BibtexParser

from databaseManager import DataBaseManager
from HttpMessage import CANNOT_CONNECT_TO_DATABASE, FILE_NOT_UPLOADED, NO_FILE_SELECTED, NO_FILE_PART, SUCCESS_UPLOAD

DEBUG = True
logLevel = logging.DEBUG if DEBUG else logging.ERROR
logger = None

load_dotenv()
app = Flask("BibFileAPI")
CORS(app)


@app.route("/api/bibtex", methods=["POST"])
def upload_file():
    method = 'upload_file'
    if 'file' not in request.files:
        return return_error(NO_FILE_PART, 400, method)
    file = request.files['file']
    if file.filename == '':
        return return_error(NO_FILE_SELECTED, 400, method)
    database_manager = DataBaseManager()
    if not database_manager.connect_to_postgres():
        return return_error(CANNOT_CONNECT_TO_DATABASE, 500, method)
    success, data = database_manager.upload_file(file)
    if not success:
        return return_error(FILE_NOT_UPLOADED, 500, method)

    return convert_process(data)

@app.route("/api/bibtex/<id>", methods=["GET"])
def restore_file(id):
    method = 'restore_file'
    database_manager = DataBaseManager()
    if not database_manager.connect_to_postgres():
        return return_error(CANNOT_CONNECT_TO_DATABASE, 500, method)
    data = database_manager.get_data_by_id(id)
    return convert_process(data)


@app.route("/api/bibtex", methods=["GET"])
def get_all_files():
    method = 'get_all_files'
    database_manager = DataBaseManager()
    if not database_manager.connect_to_postgres():
        return return_error(CANNOT_CONNECT_TO_DATABASE, 500, method)
    return jsonify(database_manager.select_all_file())

def convert_process(data: bytes):
    method = 'convert_process'
    parser = BibtexParser()
    success, msg = parser.parse_file(file = data)
    if not success:
        return return_error(msg, 500, method)
    success, msg, errors = parser.convert_file()
    if not success:
        return return_error(msg, 500, method)
    success, msg = parser.save_rdf()
    if not success:
        return return_error(msg, 500, method)
    return jsonify({'message': SUCCESS_UPLOAD, 'warnings': errors}), 200

def return_error(msg, code, method=None):
    logger.error(f'{msg} {method}')
    return jsonify({'message': msg}), code

if __name__ == "__main__":
    # Flask logger configuration
    logging.getLogger("werkzeug").setLevel(logLevel)
    # API logger configuration
    logger = logging.getLogger("bibtexToRDF")
    filehandler = logging.FileHandler('logs/log-'+ str(int(time.time())) + '.log')
    streamhandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(module)s:%(message)s')
    streamhandler.setFormatter(formatter)
    filehandler.setFormatter(formatter)
    logger.setLevel(logLevel)
    logger.addHandler(filehandler)
    logger.addHandler(streamhandler)
    logger.info('Starting API')
    app.run(host=os.environ.get('FLASK_HOST'), port=os.environ.get('FLASK_PORT'), debug=DEBUG)
