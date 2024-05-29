import time
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
print("Starting Server")
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = str(socket.recv_string())
    print(f"Received request: {message}")
    message = json.loads(message)

    action = message["type"]

    path = message["path"]
    path = path.split("/")
    location = path[0]
    spec = path[1]
    key = path[2] if len(path) > 2 else ""

    incoming_data = message["data"]

    file = open("tasks.json")
    server_data = json.load(file)
    response = {"code": 200, "message": "", "data": None}
    match action:
        case "get":
            match location:
                case "tasks":
                    match spec:
                        case "all":
                            response["data"] = server_data["tasks"]
                        case spec if spec.isdigit():
                            response["data"] = server_data["tasks"][int(spec)-1]
                        case _:
                            response["code"] = 400
                case "attributes":
                    match spec:
                        case "all":
                            response["data"] = server_data["attributes"]
                        case spec if spec.isdigit():
                            response["data"] = server_data["attributes"][int(spec) - 1]
        case "post":
            print("Post")
            match location:
                case "tasks":
                    match spec:
                        case "all":
                            server_data["tasks"].append(incoming_data)
                        case spec if spec.isdigit():
                            match key:
                                case "attributes":
                                    server_data["tasks"][int(spec)-1]["attributes"].append(incoming_data)
                                case _:
                                    response["code"] = 400
                        case _:
                            response["code"] = 400

                case "attributes":
                    server_data["attributes"].append(incoming_data)
                case _:
                    response["code"] = 400
        case "put":
            print("Put")
            match location:
                case "tasks":
                    match spec:
                        case "all":
                            response["code"] = 404
                        case spec if spec.isdigit():
                            match key:
                                case "attributes":
                                    task_index = int(spec) - 1
                                    attribute_index = int(key) - 1
                                    server_data["tasks"][task_index]["attributes"][attribute_index].update(incoming_data)
                                    response = 200
                                case "":
                                    task_index = int(spec) - 1
                                    # Get the existing task
                                    server_data["tasks"][task_index].update(incoming_data)
                                    response = 200
                                case _:
                                    response["code"] = 400
                        case _:
                            response["code"] = 400
        case "delete":
            print("Delete")
            match location:
                case "tasks":
                    match spec:
                        case "all":
                            response["code"] = 405
                        case spec if spec.isdigit():
                            match key:
                                case "attributes":
                                    task_index = int(spec) - 1
                                    res = list(filter(lambda i: i['id'] != incoming_data["id"], server_data["tasks"][task_index]["attributes"]))
                                    server_data["tasks"][task_index]["attributes"] = res
                                case "":
                                    task_index = int(spec) - 1
                                    del server_data["tasks"][task_index]
                        case _:
                            response["code"] = 400
                case "attributes":
                    match spec:
                        case "all":
                            response["code"] = 405
                        case spec if spec.isdigit():
                            attribute_index = int(spec) - 1
                            del server_data["attributes"][attribute_index]
                        case _:
                            response["code"] = 400
        case _:
            response["code"] = 400

    match response["code"]:
        case 200:
            response["message"] = "OK"
        case 400:
            response["message"] = "Bad Request"
        case 404:
            response["message"] = "Not Found"
        case 405:
            response["message"] = "Method Not Allowed"
    file = open("tasks.json", "w")
    json.dump(server_data, file, indent=4)
    file.close()
    #  Send reply back to client
    socket.send_string(json.dumps(response))