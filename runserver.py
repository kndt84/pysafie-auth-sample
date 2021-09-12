import yaml
from bottle import route, run, request, redirect, ServerAdapter
from gevent.pywsgi import WSGIServer
import pysafie

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
    return '<a href="https://openapi.safie.link/v1/auth/authorize?client_id=481a6e416310&response_type=code&scope=safie-api&redirect_uri=https://127.0.0.1">click here</a>'


@route('/')
def get_auth_code():
    code = request.query.code
    client_id = conf['client_id']
    client_secret = conf['client_secret']
    redirect_uri = conf['redirect_uri']

    safie = pysafie.Safie(client_id, client_secret, redirect_uri)
    safie.get_access_token(code)

    # You can get access token information as instance variables and need to store it
    print('access_token: ', self.access_token)
    print('refresh_token: ', self.refresh_token)
    print('expires_at: 'self.expires_at)
    
    res = safie.get_device_list()
    return res.json()


run(host='127.0.0.1', port=443, server=SSLWebServer)
