import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'proto'))

import grpc, json
import store_pb2
import store_pb2_grpc
from concurrent import futures

FILE = 'data.json'

class dataStorageBase:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_store = self.load()
        self.keys_set = set(self.data_store.keys())

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as s:
                values = json.load(s)
                print("Loaded")
                return values
        else:
           print("No data loaded")
           return {}

    def save(self):
        with open(self.file_path, 'w') as s:
            json.dump(self.data_store, s)
            print ("Stored")

class dataStorage(store_pb2_grpc.KeyValueStoreServicer, dataStorageBase):
    def __init__(self, file_path):
        dataStorageBase.__init__(self, file_path)

    def Store(self, request, context):
        self.keys_set.add(request.key)
        self.data_store[request.key] = request.value
        self.save()
        return store_pb2.Empty()

    def GetValue(self, request, context):
        value = self.data_store.get(request.key, "")
        return store_pb2.StoreRequest(key=request.key, value=value)

    def GetValues(self, request, context):
        values = [store_pb2.StoreRequest(key=k, value=v) for k, v in self.data_store.items()]
        return store_pb2.List(values=values)


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(dataStorage(FILE), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    run()
