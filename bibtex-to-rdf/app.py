import logging
import os
import time
from typing import Tuple
import requests
from dotenv import load_dotenv

from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from bibtexParser import BibtexParser

from databaseManager import DataBaseManager
from HttpMessage import CANNOT_CONNECT_TO_DATABASE, FILE_NOT_UPLOADED, NO_FILE_SELECTED, NO_FILE_PART, SUCCESS_UPLOAD
from utils import check_environnement

def init_logger():
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

    return logger

DEBUG = True
logLevel = logging.DEBUG if DEBUG else logging.ERROR
logger = init_logger()

load_dotenv()
check_environnement()
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

    message, code, graph_data = convert_process(data)
    if code == 200:
        update_code = update_fuseki(graph_data)
        if update_code == 200:
            database_manager.commit_upload()
        else:
            database_manager.rollback_upload()
            message = jsonify({'message': 'Unable to update fuseki'})
            code = 503
    else:
        database_manager.rollback_upload()

    return message, code

@app.route("/api/bibtex/<id>", methods=["GET"])
def restore_file(id):
    method = 'restore_file'
    database_manager = DataBaseManager()
    if not database_manager.connect_to_postgres():
        return return_error(CANNOT_CONNECT_TO_DATABASE, 500, method)
    data = database_manager.get_data_by_id(id)
    message, code, graph_data = convert_process(data)
    if code == 200:
        update_code = update_fuseki(graph_data)
        if update_code != 200:
            message = jsonify({'message': 'Unable to update fuseki'})
            code = 503

    return message, code


@app.route("/api/bibtex", methods=["GET"])
def get_all_files():
    method = 'get_all_files'
    database_manager = DataBaseManager()
    if not database_manager.connect_to_postgres():
        return return_error(CANNOT_CONNECT_TO_DATABASE, 500, method)
    return jsonify(database_manager.select_all_file())

@app.route('/api/bibtex/<id>', methods=['DELETE'])
def delete_file_endpoint(id):
    method = 'delete_file'
    database_manager = DataBaseManager()
    if not database_manager.connect_to_postgres():
        return return_error(CANNOT_CONNECT_TO_DATABASE, 500, method)
    return database_manager.delete_file(id)
    
def convert_process(data: bytes) -> Tuple[Response, int, str]:
    method = 'convert_process'
    parser = BibtexParser()
    success, msg = parser.parse_file(file = data)
    if not success:
        return return_error(msg, 418, method)
    success, msg, errors = parser.convert_file()
    if not success:
        return return_error(msg, 418, method)
    success, msg, graph_data = parser.save_rdf()
    if not success:
        return return_error(msg, 500, method)
    return jsonify({'message': SUCCESS_UPLOAD, 'warnings': errors}), 200, graph_data

def update_fuseki(graph_data: str):
    url = "http://sparql-endpoint:3030/library/data"
    file_data = { 'file': ('lib.rdf', graph_data, 'application/octet-stream')}
    rep = requests.request('PUT',url, files=file_data)
    return rep.status_code

def return_error(msg, code, method=None):
    logger.error(f'{msg} {method}')
    return jsonify({'message': msg}), code

def create_app():
	return app

if __name__ == "__main__":
    app.run(host=os.environ.get('FLASK_HOST'), port=os.environ.get('FLASK_PORT'), debug=DEBUG)
