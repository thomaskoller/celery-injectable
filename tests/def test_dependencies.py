from typing import Annotated, Callable
from injectable import Depends
from injectable.dependencies import get_dependencies


def test_can_extract_dependencies():
    def get_calculator():
        return lambda a, b: a + b

    def fn(
        a: int,
        b: int,
        calculator: Annotated[Callable[[int, int], int], Depends(get_calculator)],
    ):
        return calculator(a, b)

    dependencies = get_dependencies(func=fn)
    assert "calculator" in dependencies
    assert dependencies["calculator"](1, 2) == 3
