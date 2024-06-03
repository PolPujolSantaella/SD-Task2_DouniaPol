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
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreServicer(32771), server)
    server.add_insecure_port('[::]:32771')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
