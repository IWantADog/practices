import logging
import grpc
from concurrent import futures

from src import register_service

logger = logging.getLogger(__name__)
main_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))


def serve():
    logger.info("register all service")
    register_service(main_server)

    logger.info("server start")
    main_server.add_insecure_port('127.0.0.1:5000')
    main_server.start()
    main_server.wait_for_termination()


if __name__ == '__main__':
    serve()
