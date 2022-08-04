import collections.abc
import ctypes.util
import json
import os
import pathlib
import platform
import typing

import pkg_resources  # type: ignore
import tree_sitter  # type: ignore
import tree_sitter_type_provider


class TreeSitterTalon(tree_sitter_type_provider.TreeSitterTypeProvider):
    @classmethod
    def _resource_path(cls, *paths: str) -> str:
        resource_name = os.path.join(*paths)
        try:
            filename = pkg_resources.resource_filename(
                "tree_sitter_talon", resource_name
            )
            if os.path.exists(filename):
                return filename
        except (KeyError, ModuleNotFoundError):
            pass
        raise FileNotFoundError(resource_name)

    @classmethod
    def _repository_path(cls) -> str:
        return cls._resource_path("data", "tree-sitter-talon")

    @classmethod
    def _package_json_path(cls) -> str:
        return cls._resource_path("data", "tree-sitter-talon", "package.json")

    @classmethod
    def _node_types_json_path(cls) -> str:
        return cls._resource_path("data", "tree-sitter-talon", "src", "node-types.json")

    @classmethod
    def _node_types_json(cls, *, encoding: str = "utf-8") -> str:
        return pathlib.Path(cls._node_types_json_path()).read_text(encoding=encoding)

    @classmethod
    def _node_types(
        cls, *, encoding: str = "utf-8"
    ) -> collections.abc.Sequence[tree_sitter_type_provider.NodeType]:
        return tree_sitter_type_provider.NodeType.schema().loads(  # type: ignore
            cls._node_types_json(encoding=encoding), many=True
        )

    @classmethod
    def _tree_sitter_talon_version(cls) -> str:
        package_json_path = pathlib.Path(
            cls._resource_path("data", "tree-sitter-talon", "package.json")
        )
        package_json = json.loads(package_json_path.read_text())
        return package_json["version"]

    @classmethod
    def library_names(cls) -> collections.abc.Iterator[str]:
        version = cls._tree_sitter_talon_version()
        system = platform.system()
        machine = platform.machine()
        ext = {"Linux": "so", "Darwin": "dylib", "Windows": "dll"}.get(system, None)
        if ext is None:
            raise RuntimeError(f"Unsupported platform '{system}'")
        yield f"tree_sitter_talon-{version}-{machine}.{ext}"
        yield f"tree_sitter_talon-{version}.{ext}"
        yield f"tree_sitter_talon.{ext}"

    _library_path: typing.ClassVar[typing.Optional[str]] = None

    @property
    def library_path(self) -> str:
        return self.__class__.find_library() or self.__class__.build_library()

    @classmethod
    def find_library(cls) -> typing.Optional[str]:
        if not cls._library_path:
            for library_name in cls.library_names():
                try:
                    cls._library_path = cls._resource_path("data", library_name)
                except FileNotFoundError:
                    cls._library_path = ctypes.util.find_library(library_name)
                if cls._library_path:
                    break
        return cls._library_path

    @classmethod
    def build_library(cls, library_path: typing.Optional[str] = None) -> str:
        if not cls._library_path:
            library_name = next(cls.library_names())
            if library_path:
                cls._library_path = os.path.join(library_path, library_name)
            else:
                cls._library_path = os.path.join("_build", library_name)
            tree_sitter.Language.build_library(
                cls._library_path, [cls._repository_path()]
            )
        return cls._library_path

    _language: typing.ClassVar[typing.Optional[tree_sitter.Language]] = None

    @property
    def language(self) -> tree_sitter.Language:
        if not self.__class__._language:
            self.__class__._language = tree_sitter.Language(self.library_path, "talon")
        return self.__class__._language

    _parser: typing.ClassVar[typing.Optional[tree_sitter.Parser]] = None

    @property
    def parser(self) -> tree_sitter.Parser:
        if not self.__class__._parser:
            self.__class__._parser = tree_sitter.Parser()
            self.__class__._parser.set_language(self.language)
        return self.__class__._parser

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
            self.__class__._node_types(encoding=encoding),
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
