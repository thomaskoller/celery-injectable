import math
from typing import Annotated, Callable
from celery_injectable import injectable, Depends


def test_can_call_function_without_dependencies():
    @injectable
    def fn(a: int, b: int):
        return a + b

    assert fn(1, 2) == 3


def test_can_call_function_with_single_dependency():
    def get_calculator():
        return lambda a, b: a + b

    @injectable
    def fn(
        a: int,
        b: int,
        calculator: Annotated[Callable[[int, int], int], Depends(get_calculator)],
    ):
        return calculator(a, b)

    assert fn(1, 2) == 3


def test_can_call_function_with_single_generator_dependency():
    def get_calculator():
        yield lambda a, b: a + b

    @injectable
    def fn(
        a: int,
        b: int,
        calculator: Annotated[Callable[[int, int], int], Depends(get_calculator)],
    ):
        return calculator(a, b)

    assert fn(1, 2) == 3


def test_can_call_function_with_dependencies():
    def get_pi():
        yield math.pi

    def get_rad_to_degree(
        pi: Annotated[float, Depends(get_pi)],
    ):
        yield lambda rad: rad * (180 / pi)

    @injectable
    def fn(
        rad: float,
        rad_to_degree: Annotated[Callable[[float], float], Depends(get_rad_to_degree)],
    ):
        return rad_to_degree(rad)

    assert fn(rad=math.pi) == 180
