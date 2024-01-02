import grpc
import logging
from concurrent import futures
import sys
import os
from argon2 import PasswordHasher
from google.protobuf.json_format import MessageToDict
from user_handler import User
from jwt_handler import JWT
from redis_handler import RedisHandler
sys.path.append(".")
import protos.user_service_pb2 as user_service_pb2
import protos.user_service_pb2_grpc as user_service_pb2_grpc


class UserService(user_service_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.user = User()
        self.jwt = JWT()
        self.redis = RedisHandler()

    def CreateUser(self, request, context):
        try:
            username, password, email = request.username, request.password, request.email
            if not username or not password or not email:
                raise ValueError("Missing necessary fields")
            if not self.user.is_validate_password(password):
                raise ValueError("Invalid password format")
            salt = os.urandom(16).hex()
            e_password = PasswordHasher().hash(password + salt)
            if self.user.is_user_exists(username):
                raise ValueError("Username already exists")
            res = self.user.create_user(username, e_password, salt, email)
            return user_service_pb2.CreateUserResponse(user_id=str(res))
        except ValueError as e:
            logging.error(e)
            grpc_status_code = grpc.StatusCode.INVALID_ARGUMENT
            context.set_code(grpc_status_code)
            context.set_details(str(e))
            return user_service_pb2.CreateUserResponse(user_id="")
        except Exception as e:
            logging.error(e)
            grpc_status_code = grpc.StatusCode.INTERNAL
            context.set_code(grpc_status_code)
            context.set_details(str(e))
            return user_service_pb2.CreateUserResponse(user_id="")

    def UpdateUser(self, request, context):
        try:
            token, user, update_mask = request.token, request.user, request.update_mask
            if not token or not user:
                raise ValueError("Missing necessary fields")
            if update_mask.ByteSize() > 0:
                print("Update mask is not None")
                temp_dict = {}
                message_dict = MessageToDict(user)
                key_mapping = {
                    "firstName": "first_name",
                    "lastName": "last_name",
                    "age": "age",
                    "address": "address",
                }
                user_info = {key_mapping[k]: v for k,
                             v in message_dict.items()}
                for path in update_mask.paths:
                    keys = path.split('.')
                    for key in keys:
                        if key in user_info:
                            temp_dict[key] = user_info[key]
                print(temp_dict)
                res = self.user.update_user(token, temp_dict)
                print(res)
            else:
                res = self.user.update_user(token, MessageToDict(user))
                print(res)

            return user_service_pb2.UpdateUserResponse(message="OK")
        except Exception as e:
            logging.error(e)
            grpc_status_code = grpc.StatusCode.INTERNAL
            context.set_code(grpc_status_code)
            context.set_details(str(e))
            return user_service_pb2.UpdateUserResponse(message="")

    def Login(self, request, context):
        try:
            username, password = request.username, request.password
            if not username or not password:
                raise ValueError("Missing necessary fields")
            user_id = self.user.authenticate_user(username, password)
            print(user_id)
            if user_id != "":
                s_token = self.jwt.generate_token(user_id, 1)
                l_token = self.jwt.generate_token(user_id, 86400)
                self.redis.set(f"u:{user_id}:lt", l_token, 86400)
                return user_service_pb2.LoginResponse(token=s_token)
            raise ValueError("Incorrect password")
        except ValueError as e:
            logging.error(e)
            grpc_status_code = grpc.StatusCode.INVALID_ARGUMENT
            context.set_code(grpc_status_code)
            context.set_details(str(e))
            return user_service_pb2.LoginResponse(token="")
        except Exception as e:
            logging.error(e)
            grpc_status_code = grpc.StatusCode.INTERNAL
            context.set_code(grpc_status_code)
            context.set_details(str(e))
            return user_service_pb2.LoginResponse(token="")


def run():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserService(), server)
    server.add_insecure_port("[::]:%s" % port)
    server.start()
    print("Server started on port %s" % port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
