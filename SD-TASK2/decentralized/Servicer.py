import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'proto'))

import store_pb2, store_pb2_grpc
from data_destore import data_destore
import time, grpc

class KeyValueStoreServicer(store_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, port, port1, weight):
        self.delay = 0
        self.nodes_ports = [port, port1]
        self.weight = weight
        self.READ_QUORUM = 2
        self.WRITE_QUORUM = 3

        self._initialize_db_channel()
        self._load_initial_values()
        print(f"Port: {port} port1: {port1}")

    def _initialize_db_channel(self):
        self.db_channel = grpc.insecure_channel('localhost:50051')
        self.db_stub = store_pb2_grpc.KeyValueStoreStub(self.db_channel)

    def _load_initial_values(self):
        values = self.db_stub.GetValues(store_pb2.Empty())
        for value in values.values:
            print (f"Recieved: {value.key} --> {value.value}")
            data_destore.doCommit(value.key, value.value)

    def put(self, request, context):
        time.sleep(self.delay)
        success = self._perform_write_quorum(requst)

        if success:
            put_response = data_store.pu(request.key, request.value)
            if put_response:
                self._propagate_commit(request)

            self._propagate_to_db(request)

        return store_pb2.PutResponse(success=success)


    def _perform_write_quorum(self, request):
        quorum = self.weight

        for port in self.nodes_ports:
            with grpc.insecure_channel(f'localhost:{port}') as channel:
                stub = store_pb2_grpc.KeyValueStoreStub(channel)
                response_quorum = stub.askVote(store_pb2.AskRequest(key=request.key))
                quorum = quorum + response_quorum.weight

        if quorum >= self.WRITE_QUORUM:
            return True
        else:
            return False

    def _propagate_commit(self, request):

        for port in self.nodes_ports:
            with grpc.insecure_channel(f'localhost:{port}') as channel:
                stub = store_pb2_grpc.KeyValueStoreStub(channel)
                stub.doCommit(store_pb2.DoCommitRequest(key=request.key, value=request.value))

    def _propagate_to_db(self, request):
        value = store_pb2.StoreRequest(key=request.key, value=request.value)
        with grpc.insecure_channel(f'localhost:50051') as channel:
            stub = store_pb2_grpc.KeyValueStoreStub(channel)
            stub.Store(value)

    def get(self, request, context):
        value, found = data_destore.get(request.key)
        response = store_pb2.GetResponse()
        response.value = value
        response.found = found

        quorum = 0
        for port in self.nodes_ports:
            with grpc.insecure_channel(f'localhost:{port}') as channel:
                stub = store_pb2_grpc.KeyValueStoreStub(channel)
                response_quorum = stub.askVote(store_pb2.AskRequest(key=request.key))
            if response_quorum.value == value:
                quorum = quorum + response_quorum.weight

            if quorum >= self.READ_QUORUM:
                response.found = True
            else:
                response.found = False

        time.sleep(self.time)
        return response


    def slowDown(self, request, context):
        try:
            self.time = request.seconds
        except (AttributeError, TypeError) as e:
            self.time = 0
            return store_pb2.SlowDownResponse(success=False)

        return store_pb2.SlowDownResponse(success=True)

    def restore(self, empty, context):
        self.time=0
        return store_pb2.RestoreResponse(success=True)

    def askVote(self, request, context):
        value = data_destore.askVote(request.key)
        response = store_pb2.AskResponse(weight=self.weight, value=value)
        return response

    def doCommit(self, request, context):
        data_destore.doCommit(request.key, request.value)
        return store_pb2.Empty()

    def discover(self, request, context):
        ports = self.nodes_ports
        return store_pb2.DiscResponse(ports=ports)

    def addPorts(self, request, context):
        node_ports = request.ports.split(",")
        for item in node_ports:
            if item != "":
                try:
                    port = int(item)
                    if port not in self.ports:
                        self.node_ports.append(port)
                except ValueError:
                    print(f"Skip: {item}")

        return store_pb2.Empty()


