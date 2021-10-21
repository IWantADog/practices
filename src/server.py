from concurrent import futures
import logging
import grpc

logging.basicConfig()
logger = logging.getLogger(__name__)
main_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))


def serve():
    logger.info("server start")
    main_server.add_insecure_port('[::]:50051')
    main_server.start()
    main_server.wait_for_termination()


if __name__ == '__main__':
    serve()
