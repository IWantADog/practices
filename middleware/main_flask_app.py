import json

from flask import Flask, request
from flask.json import jsonify
from middleware import RequestMiddleware


app = Flask(__name__)
app.wsgi_app = RequestMiddleware(app.wsgi_app)

@app.route("/get", methods=["GET"])
def get():
    user_info = request.cookies.get("user_info", None)
    if user_info is None:
        user_info = json.dumps({"msg": "is empty"})

    return jsonify({"data": json.loads(user_info)})

@app.route("/view", methods=["GET"])
def view():
    return "it's work", 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
