from pathlib import Path
from typing import Optional, Union
from tree_sitter_type_provider import TreeSitterTypeProvider
from tree_sitter_type_provider.node_types import NodeType, Node, Point
from pkg_resources import resource_filename  # type: ignore

import sys
import tree_sitter as ts
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
        print(filename)
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
            self.node_types_path.read_text(), many=True
        )

        # Initialize module
        super().__init__("tree_sitter_talon", node_types)

        # Build tree-sitter-talon
        ts.Language.build_library(self.library_path, [self.repository_path])
        self.language = ts.Language(self.library_path, "talon")
        self.parser = ts.Parser()
        self.parser.set_language(self.language)
        self.Point = Point
        self.Node = Node

    def parse(self, contents: bytes, has_header: Optional[bool] = None) -> ts.Tree:
        if has_header is None:
            has_header = contents.startswith(b"-\n") or (b"\n-\n" in contents)
        if not has_header:
            contents = b"-\n" + contents
        return self.parser.parse(contents)

    def parse_file(
        self, path: Union[str, Path], has_header: Optional[bool] = None
    ) -> ts.Tree:
        if not isinstance(path, Path):
            path = Path(path)
        return self.parse(path.read_bytes(), has_header=has_header)


sys.modules[__name__] = TreeSitterTalon()
