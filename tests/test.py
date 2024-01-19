from dataclasses import asdict, dataclass, fields
from typing import Any
from instancemethod import instancemethod
from casting import cast_to_any_type


@dataclass
class StrictDataclass:
    """Inheritable dataclass with custom functionality for dataclasses
    with stricter typing requirements. All methods should be overriden
    if not needed
    
    Modified dunder methods:
    - __post_init__: Implemented for automatic type-casting
    - __getitem__ & __setitem__: Implemented for both integer and string
    indexing
    - __delitem__ & __delattr__: Disabled to prevent dataclass errors

    Custom class & instance methods:
    - all_fields: Property (list) containing the class's field names
    - fields_dict: Property (dict) containg the class's field 
    names and types
    - create_default: Abstract method that returns an error with the
    suggested implementations if inheriting classes do not override.

    Custom instance-only methods:
    - todict: Returns a pure-type dictionary representation of an 
    instance.
    """
    def __post_init__(self) -> None:
        self.__type_cast_fields()

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

    def __delitem__(self, *args, **kwargs) -> NotImplementedError:
        error_message = f"Manually deleting dataclass attributes/items is "\
            + f"not supported"
        raise NotImplementedError(error_message)
    
    def __delattr__(self, *args, **kwargs) -> NotImplementedError:
        error_message = f"Manually deleting dataclass attributes/items is "\
            + f"not supported"
        raise NotImplementedError(error_message)

    @classmethod
    @property
    def all_fields(cls) -> list[str]:
        """Returns a list of the class's field names."""
        return [field.name for field in fields(cls)]
    
    @classmethod
    @property
    def fields_dict(cls) -> dict:
        """Returns a dict of the class's field names and types."""
        return {field.name: field.type for field in fields(cls)}

    @instancemethod
    def __type_cast_fields(self) -> None:
        """Attempts to cast all instance attribute values to the
        annotated type
        """
        for key, field_type in self.fields_dict.items():
            self[key] = cast_to_any_type(self[key], field_type)

    @instancemethod
    def to_dict(self):
        """Returns a pure-type representation of the object using
        dataclasses.asdict.
        """
        return asdict(self)