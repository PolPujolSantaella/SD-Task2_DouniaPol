import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'proto'))

import grpc, time
import store_pb2
import store_pb2_grpc
from data_store import data_store
from concurrent import futures

class KeyValueStoreServicer(store_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, port):
        self.delay = 0
        self.nodes_ports = []

        self.NodeMaster = (port == 32770)
        if not self.NodeMaster:
            with grpc.insecure_channel(f'localhost:32770') as channel:
                stub = store_pb2_grpc.KeyValueStoreStub(channel)
                success = stub.registerNode(store_pb2.RegisterNodeRequest(port=port))

        with grpc.insecure_channel(f'localhost:50051') as channel:
            stub = store_pb2_grpc.KeyValueStoreStub(channel)
            values = stub.GetValues(store_pb2.Empty())

            for value in values.values:
                print(f'Received: {value.key} --> {value.value}')
                data_store.doCommit(value.key, value.value)

    def registerNode(self, request, context):
        if self.NodeMaster:
            self.nodes_ports.append(request.port)
            print(f"Node {request.port} registered")
            return store_pb2.RegisterNodeResponse(success=True)
        else:
            return store_pb2.RegisterNodeResponse(success=False)


    def put(self, request, context):
        time.sleep(self.delay)
        if not self.NodeMaster:
            return store_pb2.PutResponse(success=False)

        success = data_store.put(request.key, request.value)
        response = store_pb2.PutResponse(success=success)

        for port in self.nodes_ports:
            with grpc.insecure_channel(f'localhost:{port}') as channel:
                stub = store_pb2_grpc.KeyValueStoreStub(channel)
                stub.canCommit(store_pb2.Empty())

        for port in self.nodes_ports:
            with grpc.insecure_channel(f'localhost:{port}') as channel:
                stub = store_pb2_grpc.KeyValueStoreStub(channel)
                stub.doCommit(store_pb2.DoCommitRequest(key=request.key, value=request.value))

        with grpc.insecure_channel(f'localhost:50051') as channel:
            stub = store_pb2_grpc.KeyValueStoreStub(channel)
            stub.Store(store_pb2.StoreRequest(key=request.key, value=request.value))

        return response


    def doCommit(self, request, context):
        data_store.doCommit(request.key, request.value)
        return store_pb2.Empty()

    def canCommit(self, empty, context):
        return store_pb2.CanCommitResponse(success=True)

    def get (self, request, context):
        value, found = data_store.get(request.key)
        response = store_pb2.GetResponse(value=value, found=found)
        print (f'Get received: {request.key} --> {response.found}, value: {response.value}')
        time.sleep(self.delay)
        return response

    def restore (self, empty, context):
        time.sleep(self.delay)
        self.delay = 0
        return store_pb2.RestoreResponse(success=True)


    def slowDown(self, request, context):
        try:
            self.delay = request.seconds
            print("SlowDown seconds: " + str(self.delay))
        except (AttributeError, TypeError) as e:
            self.delay = 0
            return store_pb2.SlowDownResponse(success=False)

        time.sleep(self.delay)
        return store_pb2.SlowDownResponse(success=True)


