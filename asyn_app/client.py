from grpc_app import greeter_client

if __name__ == "__main__":
    host = "127.0.0.1:50051"
    greeter_client.run(host)
