import typing

from .core import TreeSitterTalon


def find_library(
    extra_library_path: typing.Optional[str] = None,
) -> typing.Optional[str]:
    return TreeSitterTalon.find_library(extra_library_path)


def build_library(library_path: typing.Optional[str] = None) -> str:
    return TreeSitterTalon.build_library(library_path)
