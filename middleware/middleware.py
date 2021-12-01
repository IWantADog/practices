import requests
import json


class AuthorationApi:
    base_host = "http://127.0.0.1:5011"

    def send_request(self, path, method, data):
        _url = self.base_host + path
        if method == "get":
            resp = requests.get(_url, params=data)
        elif method == "post":
            resp = requests.post(_url, data=data)
        else:
            raise Exception("undefined method")

        if resp.status_code != 200:
            raise Exception(f"authorization error: {resp.content}")

        return resp.json()

    def get_user_info(self, username):
        _path = '/get_info'
        return self.send_request(_path, method='get', data={"username": username})

    def authorization(self, username, path, method):
        _path = "/check"
        data = dict(username=username, path=path, method=method)
        return self.send_request(_path, method="get", data=data)


class RequestMiddleware:
    def __init__(self, app):
        self.app = app
        self.auth_api = AuthorationApi()

    def get_user_info(self, username):
        return self.auth_api.get_user_info(username)

    def authorization(self, username, path, method):
        return self.auth_api.authorization(
            username=username, path=path, method=method
        )

    def __call__(self, environ, start_response):
        request = environ['werkzeug.request']
        username = request.cookies.get('x-user', None)
        path = request.path
        method = request.method.lower()

        if not username:
            raise Exception("please login")
        
        self.authorization(username=username, path=path, method=method)
        return self.app(environ, start_response)