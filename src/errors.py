import typing

OriginalFunction = typing.Callable[..., typing.Any]
CallbackFunction = typing.Callable[[Exception], typing.Any]
Wrapper = typing.Callable[..., typing.Any]
Decorator = typing.Callable[[Wrapper], Wrapper]


class EoprError(Exception):
    """Exception raised when an error occurs in the eopr library."""

    def __init__(self, e: Exception):
        self.e = e

    def __str__(self):
        return str(self.e)


def default_error_callback(e: Exception):
    raise EoprError(e) from e


def error_handler(callback: CallbackFunction) -> Decorator:
    def decorator(func: OriginalFunction) -> Wrapper:
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                callback(e)

        return wrapper

    return decorator
