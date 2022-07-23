from rest_framework import status
from rest_framework.response import Response


def format_serializer_errors(errors):
    l_errors = dict(errors)
    key = (list(l_errors.keys())[0])
    return errors[key][0]


def error_response(error, status_code=status.HTTP_400_BAD_REQUEST):
    response_error = error
    if isinstance(error, list):
        response_error = format_serializer_errors(errors)
        print(response_error, 'response erro')
    return Response(data={'error': response_error}, status=status_code)


def success_response(data=None, message=None):
    response_obj = {}
    if data:
        response_obj['data'] = data
    if message:
        response_obj['message'] = message
    return Response(data=response_obj, status=status.HTTP_200_OK)
