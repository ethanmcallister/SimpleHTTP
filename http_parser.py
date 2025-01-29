from Request import Request
from Response import Response

# create a Request object using Request.py
# send the Request object to the server
def decode_request(bytes):

    # convert bytes into string
    request_str = str(bytes, "utf-8")

    # convert the string into list of lines
    request_list = request_str.split("\n")

    # request object variables
    method = ""
    uri = ""
    version = ""
    headers = {}
    body = ""

    is_body = False
    first_line = True
    line_count = 0

    # parse through the request string lines
    for line in request_list:
        if line_count == 0:
            first_line = False
            first_line_list = line.split(" ")

            method = first_line_list[0]
            uri = first_line_list[1]
            version = first_line_list[2]
        elif line == "":
            is_body = True
            continue
        if is_body:
            body += line + "\n"
        elif ':' in line:
            header = line.split(":")
            headers[header[0].strip()] = header[1].strip()  
        line_count += 1
        
    # create the Request object
    req = Request(method, uri, version, body, headers)

    # return the Request object
    return req

def encode_response(Response):
    # encode Response object into bytes
    # send the bytes to the server

    # convert Response object into string
    # status line
    text = Response.version + " " + str(Response.code) + " " + Response.reason + "\n"
    # headers
    for header in Response.headers:
        text += header + ": " + str(Response.headers[header]) + "\n"
    # body
    text += '\n' + Response.body

    # return the string
    return text
