from grpc.greeter_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from grpc.greeter_pb2 import HelloReply

from concurrent import futures
import logging
import grpc

class Greeter(GreeterServicer):
	def SayHello(self, request, context):
		logging.info(f'receive a request {request.name}')
		return HelloReply(message=f"Hello, {request.name}")

	def SayHelloAgain(self, request, context):
		logging.info(f'receive a request {request.name}')
		return HelloReply(message=f"Hello again, {request.name}")


def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	add_GreeterServicer_to_server(Greeter(), server)
	server.add_insecure_port('[::]:50051')
	server.start()
	server.wait_for_termination()

if __name__ == '__main__':
	logging.basicConfig()
	serve()