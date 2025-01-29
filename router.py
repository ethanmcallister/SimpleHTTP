# handles requests recieved from server and calls endpoints
# after recieving responses from endpoints, send them to the http parser
# also executes middleware chain

from endpoints import home, about, experience, projects
from Response import Response
import datetime

def route_to_endpoint(req):
    # route to the correct endpoint based on the request

    if req.uri == "/":
        response = home(req)
    elif req.uri == "/about":
        response = about(req)
    elif req.uri == "/experience":
        response = experience(req)
    elif req.uri == "/projects":
        response = projects(req)
    elif req.uri == "/info":
        # http redirect to /about, code 301
        req.uri = "/about"
        response = about(req)
        response.code = 301
        response.reason = "Moved Permanently"

        # headers
        response.headers["Server"] = "SimpleHTTPServer"
        response.headers["Date"] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        response.headers["Connection"] = "close"
        response.headers["Cache-Control"] = "max-age=3"

        # set the `Location` header to tell the browser where to go.
        response.headers["Location"] = "/about"
    else:
        # 404 response
        version = "HTTP/1.1"
        code = 404
        reason = "Not Found"
        headers = {}

        # headers
        headers["Server"] = "SimpleHTTPServer"
        headers["Date"] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        headers["Connection"] = "close"
        headers["Cache-Control"] = "max-age=3"

        body = "404 Not Found"

        response = Response(version=version, code=code, reason=reason, headers=headers, body=body)

    return response

# middleware chain
def logging_middleware_factory(next):
    def middleware(req):
        # Log the request method and URI
        print(f"Request Recieved: {req.method} {req.uri}")

        res = next(req)

        # Log the response URI, code, and reason
        print(f"{req.uri} {res.code} {res.reason}")

        return res

    return middleware

def static_files_middleware_factory(next):
    def middleware(req):
        version = "HTTP/1.1"
        code = None 
        reason = ""
        headers = {}
        body = ""

        if '.' in req.uri:
            file_path = req.uri[1:]

            try:
                with open(file_path, "r") as file:
                    content = file.read()

                version = "HTTP/1.1"
                code = 200
                reason = "OK"
                if (file_path.endswith(".css")):
                    content_type = "text/css"
                elif (file_path.endswith(".js")):
                    content_type = "text/javascript"

                headers = {
                    "Server": "SimpleHTTPServer",
                    "Date": datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                    "Connection": "close",
                    "Cache-Control": "max-age=3",
                    "Content-Length": len(content.encode('utf-8')),
                    "Content-Type": content_type,
                }

                body = content

                res = Response(version=version, code=code, reason=reason, headers=headers, body=body)

                if req.uri.endswith(".css"):
                    res.headers["Content-Type"] = "text/css"
                elif req.uri.endswith(".js"):
                    res.headers["Content-Type"] = "text/javascript"
                else:
                    raise FileNotFoundError
                return res

            except FileNotFoundError:
                version = "HTTP/1.1"
                code = 404
                reason = "Not Found"
                body = "404 Not Found"

                res = Response(version=version, code=code, reason=reason, headers=headers, body=body)

                return res

        return next(req)

    return middleware

def route(req):
    middleware_chain = logging_middleware_factory(static_files_middleware_factory(route_to_endpoint))
    response = middleware_chain(req)

    return response
