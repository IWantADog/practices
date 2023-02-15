import grpc
from grpc_app import app_pb2_grpc
from grpc_app import app_pb2

def run(host):
    with grpc.insecure_channel(host) as channel:
        stub = app_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(app_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)

if __name__ == '__main__':
    host = "127.0.0.1:55100"
    run(host=host)