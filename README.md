# strictdataclass

Sections:

- [Purpose](#purpose)
- [Contents](#contents)
- [Installation](#installation)
- [Usage](#usage)
    - [Declaration](#declaration)
- [Issues/Limitations](#issueslimitations)
- [Author](#author)
- [License](#license)

## Purpose

This package contains the necessary base class structure for strict,
auto-casting dataclasses for use in an inheritence architecture.
The inheritable base class has custom double-underscore (dunder),
convenience, and property methods.

## Contents

This package contains two modules written in pure Python (3.7 or newer)
with the following code blocks accessible from the root module:

- `StrictDataclass`: Inheritable base class for automatic type casting 
on instantiation
- `ObjectTypeNotCastableError`: Error raised when type casting fails

## Installation

This package is distributed to PyPi, and can be installed with either
of the following commands:

- `pip install strictdataclass`
- `pip3 install strictdataclass`

## Usage

Inherit the base class `StrictDataclass` in a dataclass-decorated 
class definition to inherit the type casting properties.

### Declaration

    @dataclass
    class Foo(StrictDataclass):
        bar: bool
        foo: int = 5

## Issues/Limitations

Although there are currently no known cast failing cases or 
performance issues, this package is in its infancy and has been marked
as:

***Beta***

## Author

Braden Toone is the sole author and maintainer of this code, and can
be contacted via email at braden@toonetown.com

## License

This package is licensed under the OSI Approved MIT License for free
commercial and personal use as stated in the LICENSE file.
