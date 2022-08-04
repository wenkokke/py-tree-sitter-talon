import typing

import core


def set_library(library_path: str) -> None:
    core.TreeSitterTalon.library_path = library_path


def find_library(extra_library_path: typing.Optional[str] = None) -> str:
    return core.TreeSitterTalon.find_library(extra_library_path)


def build_library(library_path: typing.Optional[str] = None) -> str:
    return core.TreeSitterTalon.build_library(library_path)
