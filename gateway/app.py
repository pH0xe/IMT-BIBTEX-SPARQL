from email import message
import os
from flask import Flask, Response, jsonify, redirect, request
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import yaml

from jwtHandler import verify_jwt_token
from utils import check_environnement

DEBUG = True

load_dotenv()
check_environnement()
app = Flask("api-gateway")
CORS(app)


def load_configuration(path):
    with open(path) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config

config = load_configuration('routing.yaml')

@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def path_router(path):
    for entry in config['paths']:
        if path.startswith(entry['path']):
            if entry['auth']:
                token = request.headers.get('Authorization')
                if not token:
                    return jsonify({"error": "No authorization header"}), 403
                is_authentified, message = verify_jwt_token(token)
                if not is_authentified:
                    return jsonify({"error": message}), 403

            addr = f"{entry['server']}{path}"
            try:
                resp = requests.request(
                    method=request.method,
                    url=addr,
                    headers={key: value for (key, value) in request.headers if key != 'Host'},
                    data=request.get_data(),
                    cookies=request.cookies,
                    allow_redirects=False)
            except Exception as e:
                return Response(e, status=500)

            excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
            headers = [(name, value) for (name, value) in resp.raw.headers.items()
                    if name.lower() not in excluded_headers]
            return Response(resp.content, resp.status_code, headers)
    return jsonify({"error": "Not found: /" + path}), 404


if __name__ == '__main__':
    app.run(host=os.environ.get('FLASK_HOST'), port=os.environ.get('FLASK_PORT'), debug=DEBUG)
