from flask import Flask, request
import time
from schema import Schema, SchemaError

from flask.json import jsonify

app = Flask(__name__)

user_info_map = {
    "Tom": {
        "name": "Tom",
        "gender": "man",
        "ago": 12,
        "telephone": "12345678"
    }
}

user_access_map = {
    "Tom": {
        "/get": ['get'],
        "/view": ['get']
    }
}


@app.route("/get_info", methods=["GET"])
def get_info():
    req_schema = Schema({"username": str})

    try:
        req_data = req_schema.validate(request.args.to_dict())
    except SchemaError:
        raise

    user_info = user_info_map.get(
        req_data["username"], {"name": "unknow"}
    )
    return jsonify({
        "info": user_info,
        "timestamp": int(time.time()), 
    })

@app.route("/check")
def check():
    req_schema = Schema({
        "username": str,
        "method": str,
        "path": str
    })

    try:
        req_data = req_schema.validate(request.args.to_dict())
    except SchemaError:
        raise
    
    can_access = check_accsee(**req_data)
    return ({"msg": "ok"}, 200) if can_access else ({"msg": "auth error"}, 500)


def check_accsee(username, path, method):
    path_method_mapping = user_access_map.get(username, {})
    return method in path_method_mapping.get(path, [])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5011, debug=True)