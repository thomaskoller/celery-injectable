from contextlib import contextmanager, ExitStack
from typing import (
    Annotated,
    Callable,
    get_args,
    get_type_hints,
    get_origin,
    Any,
    Generator,
    TypeAlias,
)
from inspect import isgeneratorfunction

Function: TypeAlias = Callable[..., Any]
Dependant: TypeAlias = Any


@contextmanager
def get_dependencies(func: Callable) -> Generator[dict[str, Dependant], Any, None]:
    with ExitStack() as stack:
        dependencies: dict[Function, Dependant] = {}
        yield _get_dependencies(func=func, stack=stack, dependency_cache=dependencies)


def _get_dependencies(
    func: Callable, stack: ExitStack, dependency_cache: dict[Function, Dependant]
) -> Any:
    dependencies = {}
    for name, annotation in get_type_hints(func, include_extras=True).items():
        if get_origin(annotation) is Annotated:
            _, depends = get_args(annotation)
            if depends.dependency in dependency_cache:
                dependencies[name] = dependency_cache[depends.dependency]
            else:
                if isgeneratorfunction(depends.dependency):
                    dependency = contextmanager(depends.dependency)
                    dependencies[name] = stack.enter_context(
                        dependency(
                            **_get_dependencies(
                                func=dependency,
                                stack=stack,
                                dependency_cache=dependency_cache,
                            )
                        )
                    )
                else:
                    dependency = depends.dependency
                    dependencies[name] = dependency(
                        **_get_dependencies(
                            func=dependency,
                            stack=stack,
                            dependency_cache=dependency_cache,
                        )
                    )
                dependency_cache[depends.dependency] = dependencies[name]
    return dependencies
