from random import randint
from typing import Annotated, Callable

import pytest

from celery_injectable import Depends
from celery_injectable.dependencies import get_dependencies


def test_can_extract_dependencies():
    def get_calculator():
        return lambda a, b: a + b

    def fn(
        a: int,
        b: int,
        calculator: Annotated[Callable[[int, int], int], Depends(get_calculator)],
    ):
        return calculator(a, b)

    with get_dependencies(func=fn) as dependencies:
        assert "calculator" in dependencies
        assert dependencies["calculator"](1, 2) == 3


def test_will_close_context():
    def get_number():
        try:
            yield 1
        finally:
            raise ValueError

    def fn(
        number: Annotated[int, Depends(get_number)],
    ):
        return number

    context_manager = get_dependencies(func=fn)
    dependencies = context_manager.__enter__()
    assert "number" in dependencies
    with pytest.raises(ValueError):
        context_manager.__exit__(None, None, None)


def test_will_reuse_dependencies():
    def get_number():
        return randint(1, 100)

    def fn(
        first: Annotated[int, Depends(get_number)],
        second: Annotated[int, Depends(get_number)],
    ):
        return first == second

    with get_dependencies(func=fn) as dependencies:
        assert dependencies["first"] == dependencies["second"]
