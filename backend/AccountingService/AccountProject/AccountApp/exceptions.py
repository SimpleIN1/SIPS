from rest_framework import status
from rest_framework.views import exception_handler

from rest_framework.exceptions import APIException, NotAuthenticated, ErrorDetail


class BadRequestError(NotAuthenticated):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad request."
    default_code = "bad_request_error"


def user_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc.detail, ErrorDetail):
            response.data["detail"] = str(exc.detail)
        elif isinstance(exc.detail, dict):
            for key, value in exc.detail.items():
                if isinstance(value, list):
                    response.data[key] = [str(item) for item in value]
                else:
                    response.data[key] = str(value)

    return response
