from typing import Any, TypedDict


class AuthenticationError(Exception):
    """Raised when there is an authentication error."""

    pass


class MissingApiToken(Exception):
    """Raised when an API token is missing."""

    pass


class UnknownRpcMethod(Exception):
    """Raised when an unknown RPC method is called."""

    pass


class ZodErrorRaw(TypedDict):
    expected: str
    code: str
    path: list[str]
    message: str

    def __init__(self, zod_error: dict[str, Any]) -> None:
        self.zod_error = zod_error
        super().__init__("Zod Validation Error")


class RpcValidationError(ValueError):
    """Raised when there is a validation error in RPC parameters."""

    def __init__(self, errors: list[ZodErrorRaw]) -> None:
        self.errors = errors

        msg = "Invalid Parameters:\n"
        for err in errors:
            msg += f"- Path: {'.'.join(err['path'])}, Expected: {err['expected']}\n"

        super().__init__(msg)
