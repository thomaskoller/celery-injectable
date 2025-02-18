from typing import (
    ParamSpec,
    TypeVar,
    Callable,
)

from .dependencies import get_dependencies

P = ParamSpec("P")
R = TypeVar("R")


def inject(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args, **kwargs) -> R:
        return func(*args, **kwargs, **get_dependencies(func=func))

    return wrapper
