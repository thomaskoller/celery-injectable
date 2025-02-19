from contextlib import contextmanager, ExitStack
from typing import (
    Annotated,
    Callable,
    get_args,
    get_type_hints,
    get_origin,
    Any,
    Generator,
)
from inspect import isgeneratorfunction


@contextmanager
def get_dependencies(func: Callable) -> Generator[dict[str, Any], Any, None]:
    with ExitStack() as stack:
        yield _get_dependencies(func=func, stack=stack)


def _get_dependencies(func: Callable, stack: ExitStack) -> Any:
    dependencies = {}
    for name, annotation in get_type_hints(func, include_extras=True).items():
        if get_origin(annotation) is Annotated:
            _, depends = get_args(annotation)
            if isgeneratorfunction(depends.dependency):
                dependency = contextmanager(depends.dependency)
                dependencies[name] = stack.enter_context(
                    dependency(**_get_dependencies(func=dependency, stack=stack))
                )
            else:
                dependency = depends.dependency
                dependencies[name] = dependency(
                    **_get_dependencies(func=dependency, stack=stack)
                )
    return dependencies
