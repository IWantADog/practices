import time
import grpc
from concurrent import futures

from grpc_app import app_pb2_grpc
from grpc_app import app_pb2

class GreeterService(app_pb2_grpc.GreeterServicer):

  def SayHello(self, request, context):
    print(f"{time.time()} receive: {request.name}")
    time.sleep(5)
    return app_pb2.HelloReply(message='Hello, %s!' % request.name)

  def SayHelloAgain(self, request, context):
    return app_pb2.HelloReply(message='Hello again, %s!' % request.name)
  

def serve():
  print("running!")
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
  app_pb2_grpc.add_GreeterServicer_to_server(
      GreeterService(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()
