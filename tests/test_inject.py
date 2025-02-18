from typing import Annotated, Callable
from injectable import inject, Depends


def test_can_call_function_without_dependencies():
    @inject
    def fn(a: int, b: int):
        return a + b

    assert fn(1, 2) == 3


def test_can_call_function_with_single_dependency():
    def get_calculator():
        return lambda a, b: a + b

    @inject
    def fn(
        a: int,
        b: int,
        calculator: Annotated[Callable[[int, int], int], Depends(get_calculator)],
    ):
        return calculator(a, b)

    assert fn(1, 2) == 3
