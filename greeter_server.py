import grpc
import logging
from concurrent import futures

from grpc_python.greeter_pb2_grpc import add_GreeterServicer_to_server
from src import customer_services


def add_service(service_list, server):
    for service in service_list:
        add_GreeterServicer_to_server(service(), server)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 注册自定义的services
    add_service(customer_services, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
