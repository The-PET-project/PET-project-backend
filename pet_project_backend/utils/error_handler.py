def bad_request_handler(msg):
    response = {
        "errorMessage": "The server cannot process the request due to client error.",
        "details": msg
    }
    return response, 400


def unauthorized_request_handler(msg):
    response = {
        "errorMessage": "The server cannot process the request due to the client is not authorized.",
        "details": msg
    }
    return response, 401
