# handles requests recieved from server and calls endpoints
# after recieving responses from endpoints, send them to the http parser
# also executes middleware chain

from endpoints import home, about, experience, projects
from Response import Response

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
        # set the `Location` header to tell the browser where to go.
        response.headers["Location"] = "/about"

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
            try:
                # send the ./static/<uri> file as the response body with the required headers
                with open(f"./static/{req.uri}", "r") as static_file:
                    content = static_file.read()

                version = "HTTP/1.1"
                code = 200
                reason = "OK"
                headers = {}
                body = content

                response = Response(version=version, code=code, reason=reason, headers=headers, body=body)

                if req.uri.endswith(".css"):
                    response.headers["Content-Type"] = "text/css"
                elif req.uri.endswith(".js"):
                    response.headers["Content-Type"] = "text/javascript"
                else:
                    response.headers["Content-Type"] = "application/octet-stream"
                return response
            
            # send a 404 response if the file is not found
            except FileNotFoundError:
                version = "HTTP/1.1"
                code = 404
                reason = "Not Found"
                body = "404 Not Found"

                response = Response(version=version, code=code, reason=reason, headers=headers, body=body)

                return response

        return next(req)

    return middleware

def route(req):
    middleware_chain = logging_middleware_factory(route_to_endpoint)
    route = static_files_middleware_factory(middleware_chain)
    response = route(req)
    return response
