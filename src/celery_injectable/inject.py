from typing import (
    ParamSpec,
    TypeVar,
    Callable,
)

from .dependencies import get_dependencies

P = ParamSpec("P")
R = TypeVar("R")


def injectable(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args, **kwargs) -> R:
        with get_dependencies(func=func) as dependencies:
            return func(*args, **kwargs, **dependencies)

    return wrapper
