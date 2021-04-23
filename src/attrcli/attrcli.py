from argparse import ArgumentParser
from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar, Union, overload

from .argument import ArgparseArgument, Argument
from .attr_class import AttrClass


T = TypeVar('T', bound='AttrClass')
C = TypeVar('C', bound='Callable[..., Any]')


def _run_cli(cls, function, arguments, parser):
    # type: (AttrClass, C, List[ArgparseArgument], ArgumentParser) -> Callable[[str], Any]
    arg_dict = {}
    for argument in arguments:
        parser.add_argument(*argument.names, **argument.keywords)
        arg_dict[argument.attribute.name] = argument
    
    def wrapper(args):
        # type: (str) -> Any
        namespace = parser.parse_args(args)
        parsed_arg_dict = dict(namespace._get_kwargs())
        converted_args = {}
        for name, parsed_arg in parsed_arg_dict.items():
            attribute = arg_dict[name].attribute
            if attribute.converter is None:
                converted_args[name] = parsed_arg
            else:
                converted_args[name] = attribute.converter(parsed_arg)
        
        try:
            value = cls(**converted_args)
        except Exception as e:
            import colorama
            import sys
            print(''.join((colorama.Fore.RED, 'Error: ', e.args[0], colorama.Fore.RESET)))
            sys.exit(1)
        return function(value)

    return wrapper   


def _attrcli(cls, parser, **kwargs):
    # type: (AttrClass, ArgumentParser, Dict[str, Argument]) -> Callable[[C], C]
    attributes = cls.__attrs_attrs__
    name_to_attr = {attribute.name: attribute for attribute in attributes if attribute.init}
    name_to_args = {name: kwargs.get(name, Argument()) for name in name_to_attr}
    arguments = []
    for name, arg in name_to_args.items():
        arguments.append(arg.to_argparse(name_to_attr[name]))

    def wrapper(function):
        # type: (C) -> C
        function.__run_cli__ = _run_cli(cls, function, arguments, parser)
        return function
    return wrapper


def attrcli(
    cls, # type: Optional[AttrClass]
    parser=None,  # type: Optional[Union[ArgumentParser, str]]
    **kwargs  # type: Argument
):
    # type: (...) -> Callable[[C], C]
    if parser is None:
        parser = ArgumentParser()
    elif isinstance(parser, str):
        parser = ArgumentParser(parser)
    
    return _attrcli(cls, parser, **kwargs)
