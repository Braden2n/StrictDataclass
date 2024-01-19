"""This module contains various functions whose purpose is to return
type-casted values for both simple and complex typing structures.
"""
if __name__ == "__main__":
    exit()
__all__ = [
    "cast_to_any_type",
    "cast_to_possibles",
    "cast_to_simple_type",
    "cast_to_instance",
    "cast_to_bool",
    "ObjectTypeNotCastableError",
]
from datetime import date, datetime
from dateutil.parser import parse
from types import UnionType
from typing import Any, Callable, Union, get_args, get_origin


class ObjectTypeNotCastableError(TypeError):
    """Raised when an object is not castable to a preferred type."""
    def __init__(self, cast_value: object, cast_type: Any) -> None:
        error_message = f"`{cast_value}` of type `{type(cast_value)}` is not "\
            + f"castable to `{cast_type}`"
        super().__init__(error_message)


def cast_to_bool(cast_value: Any) -> bool:
    """Casts any value to a boolean. Checks known boolean values 
    prior to using bool() casting.
    """
    TRUE_BOOLS = ['1', 'TRUE', 'T']
    if isinstance(cast_value, int):
        cast_value = str(cast_value)
    if not isinstance(cast_value, str):
        return bool(cast_value)
    return cast_value.upper() in TRUE_BOOLS


def double_unpacked(cast_value: Any, callable_type: type) -> Any:
    """Attempts instantiation to a type with any value unpacked 
    twice.
    """
    return callable_type(**cast_value)


def single_unpacked(cast_value: Any, callable_type: type) -> Any:
    """Attempts instantiation to a type with any value unpacked 
    once.
    """
    return callable_type(*cast_value)


def cast_to_custom_type(cast_value: Any, callable_type: type) -> Any:
    """Attempts to cast any value to an instance of an object/function 
    by passing the value to the callable with successive levels of 
    unpacking.
    """
    try:
        return double_unpacked(cast_value, callable_type)
    except TypeError:
        try:
            return single_unpacked(cast_value, callable_type)
        except TypeError:
            try:
                return callable_type(cast_value)
            except TypeError:
                raise ObjectTypeNotCastableError(cast_value, callable_type)
    except ValueError:
        raise ObjectTypeNotCastableError(cast_value, callable_type)


def cast_to_simple_type(cast_value: Any, cast_type: type) -> Any:
    """Attempts to cast a value to the provided type if it isn't 
    already in the desired type.
    
    dateutil.parser.parse implemented for date and datetime values.
    cast_to_bool implemented for boolean values. If cast_type is not
    callable, ObjectTypeNotCastableError will throw. cast_to_instance
    implemented for all other types.
    """
    if cast_type == Any or isinstance(cast_value, cast_type):
        return cast_value
    if cast_type == date:
        return parse(cast_value).date()
    if cast_type == datetime:
        return parse(cast_value)
    if cast_type == bool:
        return cast_to_bool(cast_value)
    else:
        if not isinstance(cast_type, Callable):
            raise ObjectTypeNotCastableError(cast_value, cast_type)
        return cast_to_custom_type(cast_value, cast_type)


def cast_to_multiple_types(cast_value: Any, cast_types: tuple) -> Any:
    for cast_type in cast_types:
        try:
            return cast_to_any_type(cast_value, cast_type)
        except ObjectTypeNotCastableError:
            pass


def cast_to_complex_type(cast_value: Any, cast_type: Any) -> Any:
    if isinstance(cast_type, type):
        return cast_to_simple_type(cast_value, cast_type)
    origin = get_origin(cast_type)
    type_args = get_args(cast_type)
    if origin == Union or origin == UnionType:
        return cast_to_multiple_types(cast_value, type_args)
    if issubclass(origin, list):
        return [
            cast_to_any_type(sub_value, type_args) for sub_value in cast_value
        ]
    if issubclass(origin, set):
        return {
            cast_to_any_type(sub_value, type_args) for sub_value in cast_value
        }
    if issubclass(origin, tuple):
        casted_list = [
            cast_to_any_type(sub_value, type_args) for sub_value in cast_value
        ]
        return tuple(casted_list)
    if issubclass(origin, dict):
        return {
            sub_name: cast_to_any_type(sub_value, type_args)
            for sub_name, sub_value in cast_value.items()
        }
    raise ObjectTypeNotCastableError(cast_value, cast_type)


def cast_to_any_type(cast_value: Any, cast_type: type) -> Any:
    """Returns the value of cast_to_type attempt based on the provided
    value and cast_type. Iteratively attempts to cast cast_type
    for complex field types based on successive type lineage.
    """
    if cast_value == None:
        # Catching NoneType errors prior to casting
        # No Support for nested optionals
        if str(cast_type)[:15] == 'typing.Optional':
            # Hard coding for non-instantiable optional type
            return None
        raise ObjectTypeNotCastableError(cast_value, cast_type)
    if isinstance(cast_type, tuple):
        cast_types = cast_type
    else:
        cast_types = (cast_type,)
    for cast_type in cast_types:
        try:
            if isinstance(cast_value, cast_type):
                return cast_value
        except TypeError:
            # cast_type cannot be called as field in isinstance - next
            pass
        while (get_origin(cast_type) != None):
            return cast_to_complex_type(cast_value, cast_type)
        return cast_to_simple_type(cast_value, cast_type)
    raise ObjectTypeNotCastableError(cast_value, cast_type)
