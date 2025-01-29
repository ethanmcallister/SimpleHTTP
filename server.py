# listens for bytes, then sends data to the http parser (decoder/encoder)

from http_parser import decode_request, encode_response 
from router import route 

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 8004))
    s.listen()
    print("listening on port 8004")

    while True:
        connection, addr = s.accept()
        with connection:
            data = connection.recv(8192)
            if not data:
                connection.close()
                continue

            #TODO: parse the request, send through middleware and encode the response
            # parse the request
            req = decode_request(data)            

            # send the request to the router
            response = route(req)

            # encode the response
            encoded_response = encode_response(response)

            connection.send(bytes(encoded_response, "UTF-8"))
