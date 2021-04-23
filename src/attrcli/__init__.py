from typing import Any, Callable, TypeVar


from .argument import Argument
from .attrcli import attrcli


cli = attrcli
argument = arg = Argument


T = TypeVar('T')
C = TypeVar('C', bound='Callable[..., Any]')


def run_cli(function):
    # type: (Callable[..., T]) -> T
    import sys

    if not hasattr(function, '__run_cli__'):
        raise RuntimeError('Function {} is not a cli function'.format(function))

    _run_cli = getattr(function, '__run_cli__')
    return _run_cli(sys.argv[1:])


def make_cli(cls, **kwargs):
    # type: (Any, Argument) -> Callable[[C], C]
    if not hasattr(cls, 'cli'):
        raise RuntimeError()
    else:
        _cli = getattr(cls, 'cli')
        return _cli(**kwargs)


__all__ = ['attrcli', 'argument', 'Argument', 'arg', 'run_cli', 'make_cli', 'cli']
