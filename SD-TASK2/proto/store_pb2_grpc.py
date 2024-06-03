# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import store_pb2 as store__pb2


class KeyValueStoreStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.put = channel.unary_unary(
                '/distributedstore.KeyValueStore/put',
                request_serializer=store__pb2.PutRequest.SerializeToString,
                response_deserializer=store__pb2.PutResponse.FromString,
                )
        self.get = channel.unary_unary(
                '/distributedstore.KeyValueStore/get',
                request_serializer=store__pb2.GetRequest.SerializeToString,
                response_deserializer=store__pb2.GetResponse.FromString,
                )
        self.slowDown = channel.unary_unary(
                '/distributedstore.KeyValueStore/slowDown',
                request_serializer=store__pb2.SlowDownRequest.SerializeToString,
                response_deserializer=store__pb2.SlowDownResponse.FromString,
                )
        self.restore = channel.unary_unary(
                '/distributedstore.KeyValueStore/restore',
                request_serializer=store__pb2.RestoreRequest.SerializeToString,
                response_deserializer=store__pb2.RestoreResponse.FromString,
                )
        self.Store = channel.unary_unary(
                '/distributedstore.KeyValueStore/Store',
                request_serializer=store__pb2.StoreRequest.SerializeToString,
                response_deserializer=store__pb2.Empty.FromString,
                )
        self.GetValue = channel.unary_unary(
                '/distributedstore.KeyValueStore/GetValue',
                request_serializer=store__pb2.GetRequest.SerializeToString,
                response_deserializer=store__pb2.StoreRequest.FromString,
                )
        self.GetValues = channel.unary_unary(
                '/distributedstore.KeyValueStore/GetValues',
                request_serializer=store__pb2.Empty.SerializeToString,
                response_deserializer=store__pb2.List.FromString,
                )
        self.registerNode = channel.unary_unary(
                '/distributedstore.KeyValueStore/registerNode',
                request_serializer=store__pb2.RegisterNodeRequest.SerializeToString,
                response_deserializer=store__pb2.RegisterNodeResponse.FromString,
                )
        self.canCommit = channel.unary_unary(
                '/distributedstore.KeyValueStore/canCommit',
                request_serializer=store__pb2.Empty.SerializeToString,
                response_deserializer=store__pb2.CanCommitResponse.FromString,
                )
        self.doCommit = channel.unary_unary(
                '/distributedstore.KeyValueStore/doCommit',
                request_serializer=store__pb2.DoCommitRequest.SerializeToString,
                response_deserializer=store__pb2.Empty.FromString,
                )
        self.askVote = channel.unary_unary(
                '/distributedstore.KeyValueStore/askVote',
                request_serializer=store__pb2.AskRequest.SerializeToString,
                response_deserializer=store__pb2.AskResponse.FromString,
                )
        self.discover = channel.unary_unary(
                '/distributedstore.KeyValueStore/discover',
                request_serializer=store__pb2.DiscRequest.SerializeToString,
                response_deserializer=store__pb2.DiscResponse.FromString,
                )
        self.addPorts = channel.unary_unary(
                '/distributedstore.KeyValueStore/addPorts',
                request_serializer=store__pb2.portRequest.SerializeToString,
                response_deserializer=store__pb2.Empty.FromString,
                )


class KeyValueStoreServicer(object):
    """Missing associated documentation comment in .proto file."""

    def put(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def slowDown(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def restore(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Store(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetValues(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerNode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def canCommit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def doCommit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def askVote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def discover(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addPorts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KeyValueStoreServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'put': grpc.unary_unary_rpc_method_handler(
                    servicer.put,
                    request_deserializer=store__pb2.PutRequest.FromString,
                    response_serializer=store__pb2.PutResponse.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=store__pb2.GetRequest.FromString,
                    response_serializer=store__pb2.GetResponse.SerializeToString,
            ),
            'slowDown': grpc.unary_unary_rpc_method_handler(
                    servicer.slowDown,
                    request_deserializer=store__pb2.SlowDownRequest.FromString,
                    response_serializer=store__pb2.SlowDownResponse.SerializeToString,
            ),
            'restore': grpc.unary_unary_rpc_method_handler(
                    servicer.restore,
                    request_deserializer=store__pb2.RestoreRequest.FromString,
                    response_serializer=store__pb2.RestoreResponse.SerializeToString,
            ),
            'Store': grpc.unary_unary_rpc_method_handler(
                    servicer.Store,
                    request_deserializer=store__pb2.StoreRequest.FromString,
                    response_serializer=store__pb2.Empty.SerializeToString,
            ),
            'GetValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetValue,
                    request_deserializer=store__pb2.GetRequest.FromString,
                    response_serializer=store__pb2.StoreRequest.SerializeToString,
            ),
            'GetValues': grpc.unary_unary_rpc_method_handler(
                    servicer.GetValues,
                    request_deserializer=store__pb2.Empty.FromString,
                    response_serializer=store__pb2.List.SerializeToString,
            ),
            'registerNode': grpc.unary_unary_rpc_method_handler(
                    servicer.registerNode,
                    request_deserializer=store__pb2.RegisterNodeRequest.FromString,
                    response_serializer=store__pb2.RegisterNodeResponse.SerializeToString,
            ),
            'canCommit': grpc.unary_unary_rpc_method_handler(
                    servicer.canCommit,
                    request_deserializer=store__pb2.Empty.FromString,
                    response_serializer=store__pb2.CanCommitResponse.SerializeToString,
            ),
            'doCommit': grpc.unary_unary_rpc_method_handler(
                    servicer.doCommit,
                    request_deserializer=store__pb2.DoCommitRequest.FromString,
                    response_serializer=store__pb2.Empty.SerializeToString,
            ),
            'askVote': grpc.unary_unary_rpc_method_handler(
                    servicer.askVote,
                    request_deserializer=store__pb2.AskRequest.FromString,
                    response_serializer=store__pb2.AskResponse.SerializeToString,
            ),
            'discover': grpc.unary_unary_rpc_method_handler(
                    servicer.discover,
                    request_deserializer=store__pb2.DiscRequest.FromString,
                    response_serializer=store__pb2.DiscResponse.SerializeToString,
            ),
            'addPorts': grpc.unary_unary_rpc_method_handler(
                    servicer.addPorts,
                    request_deserializer=store__pb2.portRequest.FromString,
                    response_serializer=store__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'distributedstore.KeyValueStore', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class KeyValueStore(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def put(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/put',
            store__pb2.PutRequest.SerializeToString,
            store__pb2.PutResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/get',
            store__pb2.GetRequest.SerializeToString,
            store__pb2.GetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def slowDown(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/slowDown',
            store__pb2.SlowDownRequest.SerializeToString,
            store__pb2.SlowDownResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def restore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/restore',
            store__pb2.RestoreRequest.SerializeToString,
            store__pb2.RestoreResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Store(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/Store',
            store__pb2.StoreRequest.SerializeToString,
            store__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/GetValue',
            store__pb2.GetRequest.SerializeToString,
            store__pb2.StoreRequest.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetValues(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/GetValues',
            store__pb2.Empty.SerializeToString,
            store__pb2.List.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def registerNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/registerNode',
            store__pb2.RegisterNodeRequest.SerializeToString,
            store__pb2.RegisterNodeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def canCommit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/canCommit',
            store__pb2.Empty.SerializeToString,
            store__pb2.CanCommitResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def doCommit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/doCommit',
            store__pb2.DoCommitRequest.SerializeToString,
            store__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def askVote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/askVote',
            store__pb2.AskRequest.SerializeToString,
            store__pb2.AskResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def discover(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/discover',
            store__pb2.DiscRequest.SerializeToString,
            store__pb2.DiscResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def addPorts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/distributedstore.KeyValueStore/addPorts',
            store__pb2.portRequest.SerializeToString,
            store__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
