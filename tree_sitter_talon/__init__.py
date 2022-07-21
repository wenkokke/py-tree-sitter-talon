from pathlib import Path
from tree_sitter_type_provider import TreeSitterTypeProvider, NodeType, Node, Point, ERROR
from pkg_resources import resource_filename  # type: ignore

import sys
import tree_sitter as ts
import typing
import os


class TreeSitterTalon(TreeSitterTypeProvider):
    def resource_path(self, resource_name: str) -> Path:
        dirname = os.path.dirname(__file__)
        try:
            filename = Path(resource_filename("tree_sitter_talon", resource_name))
            if filename.exists() and filename.match(f"dirname/**"):
                return filename
        except (KeyError, ModuleNotFoundError):
            pass

        filename = Path(dirname) / resource_name
        if filename.exists():
            return filename

        raise FileNotFoundError(resource_name)

    @property
    def repository_path(self) -> str:
        return str(self.resource_path("data/tree-sitter-talon"))

    @property
    def data_path(self) -> Path:
        return self.resource_path("data")

    @property
    def library_path(self) -> str:
        library_name = {
            "linux": "talon.so",
            "darwin": "talon.dylib",
            "win32": "talon.dll",
        }[sys.platform]
        return str(self.data_path / library_name)

    @property
    def node_types_path(self) -> Path:
        return self.resource_path("data/tree-sitter-talon/src/node-types.json")

    def __init__(self):
        # Read node-types.json
        node_types = NodeType.schema().loads(
            self.node_types_path.read_text(encoding="utf-8"), many=True
        )

        # Conversion from tree-sitter names to Python names
        def as_class_name(node_type_name: str) -> str:
            buffer = ["Talon"]
            for part in node_type_name.split("_"):
                buffer.append(part.capitalize())
            return "".join(buffer)

        # Initialize module
        super().__init__("tree_sitter_talon", node_types, as_class_name=as_class_name)

        # Build tree-sitter-talon
        ts.Language.build_library(self.library_path, [self.repository_path])
        self.language = ts.Language(self.library_path, "talon")
        self.parser = ts.Parser()
        self.parser.set_language(self.language)
        self.Point = Point
        self.Node = Node
        self.ERROR = ERROR

    def parse(
        self,
        contents: typing.Union[str, bytes],
        *,
        has_header: typing.Optional[bool] = None,
        encoding: str = "utf-8",
    ) -> typing.Union[typing.Sequence[Node], Node, None]:
        tree = self.parse_as_tree_sitter(
            contents, has_header=has_header, encoding=encoding
        )
        return self.from_tree_sitter(tree.root_node)

    def parse_file(
        self,
        path: typing.Union[str, Path],
        *,
        has_header: typing.Optional[bool] = None,
        encoding: str = "utf-8",
    ) -> typing.Union[typing.Sequence[Node], Node, None]:
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
    ) -> ts.Tree:
        if isinstance(contents, str):
            contents = bytes(contents, encoding)
        if has_header is None:
            has_header = contents.startswith(b"-\n") or (b"\n-\n" in contents)
        if not has_header:
            contents = b"-\n" + contents
        return self.parser.parse(contents)

    def parse_file_as_tree_sitter(
        self,
        path: typing.Union[str, Path],
        *,
        has_header: typing.Optional[bool] = None,
        encoding: str = "utf-8",
    ) -> ts.Tree:
        if not isinstance(path, Path):
            path = Path(path)
        contents = path.read_bytes()
        return self.parse_as_tree_sitter(
            contents, has_header=has_header, encoding=encoding
        )


sys.modules[__name__] = TreeSitterTalon()
