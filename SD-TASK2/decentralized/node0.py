import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'proto'))

import grpc
import time
import store_pb2
import store_pb2_grpc
from concurrent import futures
from Servicer import KeyValueStoreServicer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    port = 32770
    port1 = 32771
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreServicer(32770, 32771, 1), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()

    time.sleep(5)

    with grpc.insecure_channel(f'localhost:{port1}') as channel:
        node_stub = store_pb2_grpc.KeyValueStoreStub(channel)
        ports = node_stub.discover(store_pb2.DiscRequest(port=port1))

        if ports:
            with grpc.insecure_channel(f'localhost:{port}') as my_channel:
                stub = store_pb2_grpc.KeyValueStoreStub(my_channel)
                stub.addPorts(store_pb2.portRequest(ports=ports))



    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
