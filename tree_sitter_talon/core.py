import collections.abc
import json
import os
import pathlib
import typing

import pkg_resources  # type: ignore
import tree_sitter  # type: ignore
import tree_sitter_type_provider

from .binding import _tree_sitter_talon_id  # type: ignore


class TalonLanguage(tree_sitter.Language):
    def __init__(self):
        self.language_id = _tree_sitter_talon_id()


class TreeSitterTalon(tree_sitter_type_provider.TreeSitterTypeProvider):

    __version__: str = "1.7.0"

    _library_path: typing.Optional[str] = None

    _language: typing.Optional[tree_sitter.Language] = None

    _parser: typing.Optional[tree_sitter.Parser] = None

    @property
    def _package_json_path(self) -> str:
        return pkg_resources.resource_filename(
            "tree_sitter_talon",
            os.path.join("data", "tree-sitter-talon", "package.json"),
        )

    @property
    def _node_types_json_path(self) -> str:
        return pkg_resources.resource_filename(
            "tree_sitter_talon",
            os.path.join("data", "tree-sitter-talon", "src", "node-types.json"),
        )

    def _node_types_json(self, *, encoding: str = "utf-8") -> str:
        return pathlib.Path(self._node_types_json_path).read_text(encoding=encoding)

    def _node_types(
        self, *, encoding: str = "utf-8"
    ) -> collections.abc.Sequence[tree_sitter_type_provider.NodeType]:
        return tree_sitter_type_provider.NodeType.schema().loads(  # type: ignore
            self._node_types_json(encoding=encoding), many=True
        )

    @property
    def __grammar_version__(self) -> str:
        package_json_path = pathlib.Path(self._package_json_path)
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

    def __init__(self, *, encoding: str = "utf-8"):
        # Conversion from tree-sitter names to Python names
        def as_class_name(node_type_name: str) -> str:
            buffer = ["Talon"]
            for part in node_type_name.split("_"):
                buffer.append(part.capitalize())
            return "".join(buffer)

        # Initialize module
        super().__init__(
            "tree_sitter_talon",
            self._node_types(encoding=encoding),
            error_as_node=True,
            as_class_name=as_class_name,
            extra=["comment"],
        )
        self.NodeTypeError = tree_sitter_type_provider.NodeTypeError
        self.NodeTypeName = tree_sitter_type_provider.NodeTypeName
        self.Node = tree_sitter_type_provider.Node
        self.Leaf = tree_sitter_type_provider.Leaf
        self.Branch = tree_sitter_type_provider.Branch
        self.Point = tree_sitter_type_provider.Point

    def parse(
        self,
        contents: typing.Union[str, bytes],
        *,
        has_header: typing.Optional[bool] = None,
        encoding: str = "utf-8",
    ) -> typing.Union[
        typing.Sequence[tree_sitter_type_provider.Node],
        tree_sitter_type_provider.Node,
        None,
    ]:
        tree = self.parse_as_tree_sitter(
            contents, has_header=has_header, encoding=encoding
        )
        return self.from_tree_sitter(tree.root_node)

    def parse_file(
        self,
        path: typing.Union[str, pathlib.Path],
        *,
        has_header: typing.Optional[bool] = None,
        encoding: str = "utf-8",
    ) -> typing.Union[
        typing.Sequence[tree_sitter_type_provider.Node],
        tree_sitter_type_provider.Node,
        None,
    ]:
        tree = self.parse_file_as_tree_sitter(
            path, has_header=has_header, encoding=encoding
        )
        return self.from_tree_sitter(tree.root_node)

    def parse_as_tree_sitter(
        self,
        contents: typing.Union[str, bytes],
        *,
        has_header: typing.Optional[bool] = None,
        encoding: str = "utf-8",
    ) -> tree_sitter.Tree:
        if isinstance(contents, str):
            contents = bytes(contents, encoding)
        if has_header is None:
            has_header = contents.startswith(b"-\n") or (b"\n-\n" in contents)
        if not has_header:
            contents = b"-\n" + contents
        return self.parser.parse(contents)

    def parse_file_as_tree_sitter(
        self,
        path: typing.Union[str, pathlib.Path],
        *,
        has_header: typing.Optional[bool] = None,
        encoding: str = "utf-8",
    ) -> tree_sitter.Tree:
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        contents = path.read_bytes()
        return self.parse_as_tree_sitter(
            contents, has_header=has_header, encoding=encoding
        )
