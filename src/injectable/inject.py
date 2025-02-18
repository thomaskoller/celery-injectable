from typing import ParamSpec, TypeVar, Callable

P = ParamSpec("P")
R = TypeVar("R")


def inject(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
