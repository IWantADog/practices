from gevent import monkey
monkey.patch_all()

import time
import grpc
from grpc_app import app_pb2
from grpc_app import app_pb2_grpc

from flask import Flask, request

app = Flask(__name__)

grpc_host = "127.0.0.1:50051"
channel = grpc.insecure_channel(grpc_host)
stub = app_pb2_grpc.GreeterStub(channel)

@app.route('/greet/')
def greet():
    ident = request.args.get("ident", 0)
    print(f"flask_receive {time.time()}: {ident}")
    req = app_pb2.HelloRequest(name=str(ident))
    _ = stub.SayHello(req)
    # print(f"{time.time()} Greeter client received: " + resp.message)
    return "ok"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)

