from grpc_python.greeter_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server

from grpc_python.greeter_pb2 import HelloReply

import logging

class Greeter(GreeterServicer):
	def SayHello(self, request, context):
		logging.info(f'receive a request {request.name}')
		return HelloReply(message=f"Hello, {request.name}")

	def SayHelloAgain(self, request, context):
		logging.info(f'receive a request {request.name}')
		return HelloReply(message=f"Hello again, {request.name}")


customer_services = [Greeter]