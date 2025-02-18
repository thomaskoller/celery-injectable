from typing import (
    Annotated,
    Callable,
    get_args,
    get_type_hints,
    get_origin,
    Any,
)


def get_dependencies(func: Callable) -> dict[str, Any]:
    dependencies = {}
    for name, annotation in get_type_hints(func, include_extras=True).items():
        if get_origin(annotation) is Annotated:
            _, depends = get_args(annotation)
            dependencies[name] = depends.dependency()
    return dependencies
