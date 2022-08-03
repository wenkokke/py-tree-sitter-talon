import os
import pathlib
import platform
import sys
import typing

import pkg_resources  # type: ignore
import tree_sitter
import tree_sitter_type_provider


class TreeSitterTalon(tree_sitter_type_provider.TreeSitterTypeProvider):
    def resource_path(self, resource_name: str) -> pathlib.Path:
        dirname = os.path.dirname(__file__)
        try:
            filename = pathlib.Path(
                pkg_resources.resource_filename("tree_sitter_talon", resource_name)
            )
            if filename.exists() and filename.match(f"dirname/**"):
                return filename
        except (KeyError, ModuleNotFoundError):
            pass

        filename = pathlib.Path(dirname) / resource_name
        if filename.exists():
            return filename

        raise FileNotFoundError(resource_name)

    @property
    def repository_path(self) -> str:
        return str(self.resource_path("data/tree-sitter-talon"))

    @property
    def data_path(self) -> pathlib.Path:
        return self.resource_path("data")

    @property
    def library_name(self) -> str:
        machine = platform.machine()
        supported_systems: dict[str, str] = {
            "Linux": "so",
            "Darwin": "dylib",
            "Windows": "dll",
        }
        ext = supported_systems.get(platform.system(), None)
        if ext is None:
            raise RuntimeError(f"Unsupported platform '{platform.system()}'")
        return f"talon-{machine}.{ext}"

    @property
    def library_path(self) -> str:
        return str(self.data_path / self.library_name)

    @property
    def node_types_path(self) -> pathlib.Path:
        return self.resource_path("data/tree-sitter-talon/src/node-types.json")

    def __init__(self, *, encoding: str = "utf-8"):
        # Read node-types.json
        node_types = tree_sitter_type_provider.NodeType.schema().loads(  # type: ignore
            self.node_types_path.read_text(encoding=encoding), many=True
        )

        # Conversion from tree-sitter names to Python names
        def as_class_name(node_type_name: str) -> str:
            buffer = ["Talon"]
            for part in node_type_name.split("_"):
                buffer.append(part.capitalize())
            return "".join(buffer)

        # Initialize module
        super().__init__(
            "tree_sitter_talon",
            node_types,
            error_as_node=True,
            as_class_name=as_class_name,
            extra=["comment"],
        )

        # Build tree-sitter-talon
        tree_sitter.Language.build_library(self.library_path, [self.repository_path])
        self.language = tree_sitter.Language(self.library_path, "talon")
        self.parser = tree_sitter.Parser()
        self.parser.set_language(self.language)

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


sys.modules[__name__] = TreeSitterTalon()
