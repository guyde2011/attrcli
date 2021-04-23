from typing import Any, Dict, List, Optional, cast


import attr
from attr import Attribute, NOTHING


@attr.s
class ArgparseArgument(object):
    attribute = attr.ib()  # type: Attribute
    names = attr.ib()  # type: List[str]
    keywords = attr.ib()  # type: Dict[str, Any]


class Argument(object):
    def __init__(self, alias=[], **kwargs):
        # type: (Optional[List[str]], Any) -> None
        self.alias = list(alias)
        self.kwargs = dict(kwargs)
        self.name = None  # type: Optional[str]
        if 'name' in self.kwargs:
            self.name = cast(str, self.kwargs.pop('name'))

    def to_argparse(self, attribute):
        # type: (Attribute) -> ArgparseArgument
        keywords = {}
        if self.name is None:
            name = attribute.name
        else:
            name = self.name

        if attribute.default is not NOTHING:
            keywords['default'] = attribute.default
        if attribute.type is not None:
            keywords['type'] = attribute.type

        names = [name]
        names.extend(self.alias)
        if name.startswith('-'):
            keywords['required'] = ('default' not in keywords)
        keywords.update(self.kwargs)
        return ArgparseArgument(attribute, names, keywords)


__all__ = ['Argument, ArgparseArgument']
