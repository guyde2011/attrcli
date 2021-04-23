from typing import Any, List, Protocol

from attr import Attribute


class AttrClass(Protocol):
    @property
    def __attrs_attrs__(cls):
        # type: () -> List[Attribute]
        return NotImplemented

    def __call__(cls, **kwargs):
        # type: (Any) -> Any
        return NotImplemented


__all__ = ['AttrClass']
