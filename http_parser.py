from Request import Request
from Response import Response

# create a Request object using Request.py
# send the Request object to the server
def decode_request(bytes):

    # convert bytes into string
    requestStr = str(bytes, "utf-8")

    # convert the string into list of lines
    requestList = requestStr.split("\n")

    # request object variables
    method = ""
    uri = ""
    version = ""
    headers = {}
    body = ""

    isBody = False
    firstLine = True
    lineCount = 0

    # parse through the request string lines
    for line in requestList:
        if lineCount == 0:
            firstLine = False
            firstLineList = line.split(" ")

            method = firstLineList[0]
            uri = firstLineList[1]
            version = firstLineList[2]
        elif line == "":
            isBody = True
            continue
        if isBody:
            body += line + "\n"
        elif ':' in line:
            header = line.split(":")
            headers[header[0].strip()] = header[1].strip()  
        lineCount += 1
        
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
        text += header + ": " + Response.headers[header] + "\n"
    # body
    text += '\n' + Response.body

    # return the string
    return text
