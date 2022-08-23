import collections.abc
import json
import os
import pathlib
import typing

import pkg_resources  # type: ignore
import tree_sitter  # type: ignore
import tree_sitter_type_provider

from .binding import _tree_sitter_talon_id


class TalonLanguage(tree_sitter.Language):
    def __init__(self):
        self.language_id = _tree_sitter_talon_id()


class TreeSitterTalon(tree_sitter_type_provider.TreeSitterTypeProvider):

    __version__: str = "3.0.2"

    _library_path: typing.Optional[str] = None

    _language: typing.Optional[tree_sitter.Language] = None

    _parser: typing.Optional[tree_sitter.Parser] = None

    @property
    def _node_types(
        self,
    ) -> collections.abc.Sequence[tree_sitter_type_provider.NodeType]:
        node_types_path = pathlib.Path(
            pkg_resources.resource_filename(
                "tree_sitter_talon",
                os.path.join("data", "tree-sitter-talon", "src", "node-types.json"),
            )
        )
        return tree_sitter_type_provider.NodeType.schema().loads(  # type: ignore
            node_types_path.read_text(), many=True
        )

    @property
    def __grammar_version__(self) -> str:
        package_json_path = pathlib.Path(
            pkg_resources.resource_filename(
                "tree_sitter_talon",
                os.path.join("data", "tree-sitter-talon", "package.json"),
            )
        )
        package_json = json.loads(package_json_path.read_text())
        return package_json["version"]

    @property
    def language(self) -> tree_sitter.Language:
        if not self._language:
            self._language = TalonLanguage()
        return self._language

    @property
    def parser(self) -> tree_sitter.Parser:
        if not self._parser:
            self._parser = tree_sitter.Parser()
            self._parser.set_language(self.language)
        return self._parser

    def __init__(self):
        # Conversion from tree-sitter names to Python names
        def as_class_name(node_type_name: str) -> str:
            buffer = ["Talon"]
            for part in node_type_name.split("_"):
                buffer.append(part.capitalize())
            return "".join(buffer)

        # Initialize module
        super().__init__(
            "tree_sitter_talon",
            self._node_types,
            as_class_name=as_class_name,
            extra=["comment"],
        )
        self.NodeTypeError = tree_sitter_type_provider.NodeTypeError
        self.NodeTypeName = tree_sitter_type_provider.NodeTypeName
        self.Node = tree_sitter_type_provider.Node
        self.Leaf = tree_sitter_type_provider.Leaf
        self.Branch = tree_sitter_type_provider.Branch
        self.Point = tree_sitter_type_provider.Point
        self.ParseError = tree_sitter_type_provider.ParseError

    def parse(
        self,
        contents: typing.Union[str, bytes],
        *,
        encoding: str = "utf-8",
        filename: typing.Optional[str] = None,
        raise_parse_error: bool = False,
    ) -> typing.Union[
        typing.Sequence[tree_sitter_type_provider.Node],
        tree_sitter_type_provider.Node,
        None,
    ]:
        tree = self._parse(contents, encoding=encoding)
        return self.from_tree_sitter(
            tree.root_node, filename=filename, raise_parse_error=raise_parse_error
        )

    def parse_file(
        self,
        path: typing.Union[str, pathlib.Path],
        *,
        encoding: str = "utf-8",
        raise_parse_error: bool = False,
    ) -> typing.Union[
        typing.Sequence[tree_sitter_type_provider.Node],
        tree_sitter_type_provider.Node,
        None,
    ]:
        tree = self._parse_file(path, encoding=encoding)
        return self.from_tree_sitter(
            tree.root_node, filename=str(path), raise_parse_error=raise_parse_error
        )

    def _parse(
        self,
        contents: typing.Union[str, bytes],
        *,
        encoding: str = "utf-8",
    ) -> tree_sitter.Tree:
        if isinstance(contents, str):
            contents = bytes(contents, encoding)
        return self.parser.parse(contents)

    def _parse_file(
        self,
        path: typing.Union[str, pathlib.Path],
        *,
        encoding: str = "utf-8",
    ) -> tree_sitter.Tree:
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        contents = path.read_bytes()
        return self._parse(contents, encoding=encoding)
