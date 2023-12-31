# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import user_service_pb2 as protos_dot_user__service__pb2


class UserServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateUser = channel.unary_unary(
                '/user.UserService/CreateUser',
                request_serializer=protos_dot_user__service__pb2.CreateUserRequest.SerializeToString,
                response_deserializer=protos_dot_user__service__pb2.CreateUserResponse.FromString,
                )
        self.Login = channel.unary_unary(
                '/user.UserService/Login',
                request_serializer=protos_dot_user__service__pb2.LoginRequest.SerializeToString,
                response_deserializer=protos_dot_user__service__pb2.LoginResponse.FromString,
                )
        self.UpdateUser = channel.unary_unary(
                '/user.UserService/UpdateUser',
                request_serializer=protos_dot_user__service__pb2.UpdateUserRequest.SerializeToString,
                response_deserializer=protos_dot_user__service__pb2.User.FromString,
                )


class UserServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Login(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateUser': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateUser,
                    request_deserializer=protos_dot_user__service__pb2.CreateUserRequest.FromString,
                    response_serializer=protos_dot_user__service__pb2.CreateUserResponse.SerializeToString,
            ),
            'Login': grpc.unary_unary_rpc_method_handler(
                    servicer.Login,
                    request_deserializer=protos_dot_user__service__pb2.LoginRequest.FromString,
                    response_serializer=protos_dot_user__service__pb2.LoginResponse.SerializeToString,
            ),
            'UpdateUser': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateUser,
                    request_deserializer=protos_dot_user__service__pb2.UpdateUserRequest.FromString,
                    response_serializer=protos_dot_user__service__pb2.User.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'user.UserService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UserService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/user.UserService/CreateUser',
            protos_dot_user__service__pb2.CreateUserRequest.SerializeToString,
            protos_dot_user__service__pb2.CreateUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Login(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/user.UserService/Login',
            protos_dot_user__service__pb2.LoginRequest.SerializeToString,
            protos_dot_user__service__pb2.LoginResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/user.UserService/UpdateUser',
            protos_dot_user__service__pb2.UpdateUserRequest.SerializeToString,
            protos_dot_user__service__pb2.User.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
