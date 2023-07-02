from typing import Any, Callable


class EoprError(Exception):
    """Exception raised when an error occurs in the eopr library."""

    def __init__(self, e: Exception):
        self.e = e

    def __str__(self):
        return str(self.e)


def default_error_callback(e: Exception):
    raise EoprError(e) from e


def error_handler(
    callback: Callable[[Exception], Any]
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                callback(e)

        return wrapper

    return decorator
