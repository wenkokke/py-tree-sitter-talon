from pathlib import Path
from typing import Optional, Union
import sys
import tree_sitter_type_provider as tstp
import tree_sitter as ts
import pkg_resources as pkg
import os


class TreeSitterTalon:
    def resource_filename(self, resource_name: str) -> str:
        return pkg.resource_filename("tree_sitter_talon", resource_name)

    @property
    def repository_path(self) -> str:
        return self.resource_filename("data/tree-sitter-talon")

    @property
    def data_path(self) -> str:
        return self.resource_filename("data")

    @property
    def library_path(self) -> str:
        return os.path.join(
            self.data_path,
            {
                "linux": "talon.so",
                "darwin": "talon.dylib",
                "win32": "talon.dll",
            }[sys.platform],
        )

    @property
    def node_types_path(self) -> str:
        return self.resource_filename("data/tree-sitter-talon/src/node-types.json")

    def __init__(self):
        # Build tree-sitter-talon
        ts.Language.build_library(self.library_path, [self.repository_path])
        self.language = ts.Language(self.library_path, "talon")
        self.parser = ts.Parser()
        self.parser.set_language(self.language)

        # Build tree-sitter node types
        with open(self.node_types_path, "r") as fp:
            node_types = tstp.NodeType.schema().loads(fp.read(), many=True)
        self.types = tstp.TypeProvider("types", node_types)

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
