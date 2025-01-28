# contains endpoint functions that will be called by the router
# create Response objects based on requests and send them to the router

from Response import Response

def home(req):
    version = "HTTP/1.1"
    code = 200
    reason = "OK"
    headers = {}
    body = get_body(req)

    return Response(version=version, code=code, reason=reason, headers=headers, body=body)

def about(req):
    version = "HTTP/1.1"
    code = 200
    reason = "OK"
    headers = {}
    body = get_body(req)

    return Response(version=version, code=code, reason=reason, headers=headers, body=body)

def experience(req):
    version = "HTTP/1.1"
    code = 200
    reason = "OK"
    headers = {}
    body = get_body(req)

    return Response(version=version, code=code, reason=reason, headers=headers, body=body)

def projects(req):
    version = "HTTP/1.1"
    code = 200
    reason = "OK"
    headers = {}
    body = get_body(req)

    return Response(version=version, code=code, reason=reason, headers=headers, body=body)

def get_body(req):
    path = ""
    if (req.uri == "/"):
        path = f"./templates/index.html"
    else:
        path = f"./templates{req.uri}.html"

    with open(path, "r") as file:
        return file.read()
