from rest_framework.exceptions import ValidationError
from rest_framework import status


def raise_error(message, status_code=status.HTTP_400_BAD_REQUEST):
    err_obj = {
        'status': 'error',
        'message': message
    }
    error_message = ValidationError(err_obj)
    error_message.status_code = status_code
    raise error_message
