# handles requests recieved from server and calls endpoints
# after recieving responses from endpoints, send them to the http parser
# also executes middleware chain

from endpoints import home, about, experience, projects

def route_to_endpoint(req):
    # route to the correct endpoint based on the request

    # execute middleware chain on request
    middleware(req)

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
        response = about(req)
        response.code = 301
        # set the `Location` header to tell the browser where to go.
        response.headers["Location"] = "/about"

    # execute the middleware chain on the response
    middleware(response)

    return response

# middleware chain
def middleware(req):
    # execute middleware functions

    # log 
    print(req.method, req.uri)
    pass

def middleware_factory(next):
    def middlware(my_input):
        # Do something with my_input (optional)
        res = next(my_input) # call the next middleware in the chain
        # do something with res (optional)
        return res # don't forget this step!
    
    return middlware # don't forget this step!
