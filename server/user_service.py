import grpc
import logging
from concurrent import futures
import sys
import os
from argon2 import PasswordHasher
from user_handler import User
from jwt_handler import generate_token
import validator
sys.path.append(".")
import protos.user_service_pb2 as user_service_pb2
import protos.user_service_pb2_grpc as user_service_pb2_grpc

class UserService(user_service_pb2_grpc.UserServiceServicer):
    def CreateUser(self, request, context):
        try:
            username, password, email = request.username, request.password, request.email
            if not username or not password or not email:
                raise ValueError("Missing necessary fields")
            if not validator.is_validate_password(password):
                raise ValueError("Invalid password format")
            salt = os.urandom(16).hex()
            e_password = PasswordHasher().hash(password + salt)
            user = User()
            if user.is_user_exist(username):
                raise ValueError("Username already exists")
            res = user.create_user(username, e_password, salt, email)
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
        finally:
            user.db.close_connection()

    def Login(self, request, context):
        try:
            username, password = request.username, request.password
            if not username or not password:
                raise ValueError("Missing necessary fields")
            user = User()
            if not user.is_user_exist(username):
                raise ValueError("Username does not exist")
            if not user.is_correct_password(username, password):
                raise ValueError("Incorrect password")
            return user_service_pb2.LoginResponse(token=generate_token(username))
        except ValueError as e:
            logging.error(e)
            grpc_status_code = grpc.StatusCode.INVALID_ARGUMENT
            context.set_code(grpc_status_code)
            context.set_details(str(e))
            return user_service_pb2.LoginResponse(token="Fail")
        except Exception as e:
            logging.error(e)
            grpc_status_code = grpc.StatusCode.INTERNAL
            context.set_code(grpc_status_code)
            context.set_details(str(e))
            return user_service_pb2.LoginResponse(token="Fail")
        finally:
            user.db.close_connection()


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
