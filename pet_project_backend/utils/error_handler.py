def http_400_bad_request_handler(msg):
    response = {
        "errorMessage": "The server cannot process the request due to some client error.",
        "details": msg,
    }
    return response, 400


def http_401_unauthorized_request_handler(msg):
    response = {
        "errorMessage": "The server cannot process the request due to the client is not authorized.",
        "details": msg,
    }
    return response, 401


def http_403_forbidden_request_handler(msg):
    response = {
        "errorMessage": "The server cannot process the request due to the client does not have the proper access "
        "rights to the content.",
        "details": msg,
    }
    return response, 403


def http_404_resource_not_found_handler(msg):
    response = {
        "errorMessage": "The server cannot find the request resource.",
        "details": msg,
    }
    return response, 404
