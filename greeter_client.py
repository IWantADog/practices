import grpc
from grpc_python.greeter_pb2_grpc import GreeterStub
from grpc_python.greeter_pb2 import HelloRequest


def run():
    channel = grpc.insecure_channel('localhost:5000')
    stub = GreeterStub(channel=channel)
    response = stub.SayHello(HelloRequest(name='you'))
    print(f"this is first response {response.message}")

    response = stub.SayHelloAgain(HelloRequest(name='you'))
    print(f"this is the second response {response.message}")


if __name__ == '__main__':
    run()
