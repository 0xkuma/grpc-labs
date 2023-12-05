#!/bin/bash

# Get the proto file
PROTO_FILE=$1

# Lowercase the language argument to avoid case sensitive issues
LANGUAGE=$(echo $2 | tr '[:upper:]' '[:lower:]')

# Directory containing the .proto files
PROTO_DIRECTORY="./protos"

# Check if both arguments are present
if [[ -z "$PROTO_FILE" || -z "$LANGUAGE" ]]; then
    echo "Usage: compile_proto.sh protofile destination_language"
    exit 1
fi

# Compile the proto file to the selected language
case "$LANGUAGE" in 
  "python")
    python -m grpc_tools.protoc  -I. --python_out=./server --pyi_out=./server --grpc_python_out=. ${PROTO_DIRECTORY}/${PROTO_FILE}
    python -m grpc_tools.protoc  -I. --python_out=./client --pyi_out=./client ${PROTO_DIRECTORY}/${PROTO_FILE}
    ;;
  *)
    echo "Unsupported language. The script currently supports python only"
    ;;
esac