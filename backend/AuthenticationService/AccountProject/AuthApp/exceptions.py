from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail


def user_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc.detail, ErrorDetail):
            response.data["detail"] = str(exc.detail)
        elif isinstance(exc.detail, dict):
            for key, value in exc.detail.items():
                response.data[key] = [str(item) for item in value]

    return response
