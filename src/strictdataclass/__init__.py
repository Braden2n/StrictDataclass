"""This module contains the `StrictDataclass` class that implements 
custom dunder, class, property, and instancemethods that aid in type 
verification, attribute access/utilization, and side-effect 
introduction for custom dataclasses where type safety is important.

This module also contains the `ObjectTypeNotCastableError` error class 
that is thrown during a failed attempt at type casting
"""
from dataclasses import asdict, dataclass, fields
from typing import Any, Iterator
from any_cast import cast
from instancemethod import instancemethod
__all__ = [
    "StrictDataclass",
]
__refs__ = {
    "AUTHOR": {
        "Name": "Braden Toone",
        "Email": "braden@toonetown.com"
    },
    "HOMEPAGE": "https://github.com/Braden2n/StrictDataclass",
    "DOCUMENTATION": "https://github.com/Braden2n/StrictDataclass",
    "ISSUES": "https://github.com/Braden2n/StrictDataclass/issues",
    "REPOSITORY": "https://github.com",
    "CHANGELOG": "https://github.com/Braden2n/StrictDataclass/activity",
}


class classproperty:
    def __init__(self, func: Any):
        self.getter = func
    def __get__(self, _, owner):
        return self.getter(owner)


@dataclass
class StrictDataclass:
    """Inheritable dataclass with custom functionality for dataclasses
    with stricter typing requirements. All methods should be overriden
    if not needed
    
    Modified dunder methods:
    - __post_init__: Implemented for automatic type-casting. Overwrite
    to remove the automatic functionality.
    - __getitem__ & __setitem__: Implemented for both integer and 
    string indexing.
    - __delitem__ & __delattr__: Disabled to prevent dataclass errors.

    Custom class & instance methods:
    - all_fields: Property (list) containing the class's field names.
    - fields_dict: Property (dict) containg the class's field 
    names and types.
    - create_default: Abstract method that returns an error with the
    suggested implementations if inheriting classes do not override.

    Custom instance-only methods:
    - type_cast_fields: Iteratively attempts to cast each attribute
    to the class's field type for that attribute.
    - to_dict: Returns a pure-type dictionary representation of an 
    instance.
    """
    def __post_init__(self) -> None:
        self.type_cast_fields()

    def __getitem__(self, item: int | str) -> Any:
        if isinstance(item, int):
            return self.__getattribute__(fields(self)[item].name)
        elif isinstance(item, str):
            return self.__getattribute__(item)
        else:
            raise NotImplementedError(
                f"Accessing `{type(self)}` attributes "\
                + f"by `{type(item)}` type is not supported"
            )

    def __setitem__(self, item: int | str, value: Any) -> None:
        if isinstance(item, int):
            self.__setattr__(fields(self)[item].name, value)
        elif isinstance(item, str):
            self.__setattr__(item, value)
        else:
            error_message = f"Setting `{type(self)}` attribute by "\
                + f"`{type(item)}` is not supported"
            raise NotImplementedError(error_message)

    def __delitem__(self, *args, **kwargs) -> None:
        error_message = f"Manually deleting dataclass attributes/items is "\
            + f"not supported"
        raise NotImplementedError(error_message)
    
    def __delattr__(self, *args, **kwargs) -> None:
        error_message = f"Manually deleting dataclass attributes/items is "\
            + f"not supported"
        raise NotImplementedError(error_message)
    
    def __iter__(self) -> Iterator:
        return iter([{k: v} for k, v in self.to_dict().items()])
    
    def __len__(self) -> int:
        return len([{k: v} for k, v in self.to_dict().items()])

    @classproperty
    def all_fields(cls) -> list[str]:
        """Returns a list of the class's field names."""
        return [field.name for field in fields(cls)]
    
    @classproperty
    def fields_dict(cls) -> dict[str, Any]:
        """Returns a dict of the class's field names and types."""
        return {field.name: field.type for field in fields(cls)}

    @instancemethod
    def type_cast_fields(self) -> None:
        """Attempts to cast all instance attribute values to the
        annotated type.
        
        Can throw `ObjectTypeNotCastableError` in unsupported type
        cases.
        """
        for key, field_type in self.fields_dict.items():
            self[key] = cast(self[key], field_type)

    @instancemethod
    def to_dict(self) -> dict[str, Any]:
        """Returns a pure-type representation of the object using
        dataclasses.asdict.
        """
        return asdict(self)
