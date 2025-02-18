
from injectable import inject


def test_can_call_function_without_dependencies():
    @inject
    def fn(a: int, b: int):
        return a + b

    assert fn(1, 2) == 3
