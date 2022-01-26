from src.service.greeter import Greeter, add_GreeterServicer_to_server


def register_service(server):
    """
    register service to server
    :param server:
    :return:
    """

    service_map = {
        "greeter": {
            "class": Greeter(),
            "register": add_GreeterServicer_to_server
        }
    }

    for name, dt_info in service_map.items():
        dt_info["register"](dt_info["class"], server)
