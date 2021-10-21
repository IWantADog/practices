from concurrent import futures
import logging
import grpc

main_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))


def serve():
    main_server.add_insecure_port('[::]:50051')
    main_server.start()
    main_server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
