from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    DEFAULT_MESSAGE = "Invalid authentication credentials"
    DEFAULT_REDIRECT_LOCATION = "/index"

    def __init__(self, message=None, redirect=False, redirect_location=None):
        status_code = status.HTTP_401_UNAUTHORIZED
        headers = {"WWW-Authenticate": "Bearer"}
        if redirect:
            status_code = status.HTTP_302_FOUND
            headers["Location"] = (
                redirect_location
                if redirect_location
                else self.DEFAULT_REDIRECT_LOCATION
            )

        super().__init__(
            detail=message if message else self.DEFAULT_MESSAGE,
            status_code=status_code,
            headers=headers,
        )


class SessionExpiredException(UnauthorizedException):
    def __init__(self):
        super().__init__(
            "Session expired", redirect=True, redirect_location="/auth/session_expired"
        )


class RegistrationException(HTTPException):
    default_message = "Registration error"

    def __init__(self, message=None):
        super().__init__(
            detail=message or self.default_message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
