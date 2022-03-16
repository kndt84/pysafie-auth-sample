import yaml
from bottle import route, run, request, redirect, ServerAdapter
from gevent.pywsgi import WSGIServer
import pysafie
import json
CERT = 'cert.pem'
KEY = 'key.pem'

with open('config.yml', 'r') as yml:
    conf = yaml.load(yml)


class SSLWebServer(ServerAdapter):
    def run(self, handler):
        srv = WSGIServer(('127.0.0.1', 443), handler,
                         certfile=CERT,
                         keyfile=KEY)
        srv.serve_forever()


@route('/authsample')
def authsample():
    return '<a href="https://openapi.safie.link/v1/auth/authorize?client_id=481a6e416310&response_type=code&scope=safie-api&redirect_uri=https://safie-auth.scorer.jp/auth_code"> click here </a>'


@route('/')
def get_auth_code():
    # Get authorization code as a GET parameter
    code = request.query.code
    status = {}
    status['status_code'] = '1000'
    status['message'] = 'success'
    status['auth_code'] = str(code)
    response = json.dumps(status)
    return response

run(host='127.0.0.1', port=443, server=SSLWebServer)
