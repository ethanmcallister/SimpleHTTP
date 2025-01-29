# contains endpoint functions that will be called by the router
# create Response objects based on requests and send them to the router

from Response import Response
import datetime

def home(req):
    version = "HTTP/1.1"
    code = 200
    reason = "OK"
    body = get_body(req)
    headers = generate_headers(req, body)

    return Response(version=version, code=code, reason=reason, headers=headers, body=body)

def about(req):
    version = "HTTP/1.1"
    code = 200
    reason = "OK"
    body = get_body(req)
    headers = generate_headers(req, body)

    return Response(version=version, code=code, reason=reason, headers=headers, body=body)

def experience(req):
    version = "HTTP/1.1"
    code = 200
    reason = "OK"
    body = get_body(req)
    headers = generate_headers(req, body)

    return Response(version=version, code=code, reason=reason, headers=headers, body=body)

def projects(req):
    version = "HTTP/1.1"
    code = 200
    reason = "OK"
    body = get_body(req)
    headers = generate_headers(req, body)

    return Response(version=version, code=code, reason=reason, headers=headers, body=body)

def get_body(req):
    path = ""
    if (req.uri == "/"):
        path = f"./templates/index.html"
    else:
        path = f"./templates{req.uri}.html"

    with open(path, "r") as file:
        return file.read()

def generate_headers(req, body):
    headers = {}
    headers["Server"] = "SimpleHTTPServer"
    headers["Date"] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers["Connection"] = "close"
    headers["Cache-Control"] = "max-age=3"
    headers["Content-Length"] = len(body.encode('utf-8'))
    if '.' in req.uri:
        if '.js' in req.uri:
            headers["Content-Type"] = "text/javascript"
        elif '.css' in req.uri:
            headers["Content-Type"] = "text/css"
    else:
        headers["Content-Type"] = "text/html"

    return headers
