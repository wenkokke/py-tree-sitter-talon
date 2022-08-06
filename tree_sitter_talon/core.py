import collections.abc
import ctypes.util
import json
import logging
import os
import pathlib
import platform
import typing

import appdirs  # type: ignore
import pkg_resources  # type: ignore
import tree_sitter  # type: ignore
import tree_sitter_type_provider
import wget  # type: ignore


class TreeSitterTalon(tree_sitter_type_provider.TreeSitterTypeProvider):

    __version__: str = "1.6.16"

    DEFAULT_LIBRARY_PATH: str = appdirs.user_cache_dir("tree_sitter_talon", "wenkokke")

    _library_path: typing.Optional[str] = None

    _language: typing.Optional[tree_sitter.Language] = None

    _parser: typing.Optional[tree_sitter.Parser] = None

    _allow_build: bool = True

    @property
    def allow_build(self) -> bool:
        return self._allow_build

    @allow_build.setter
    def allow_build(self, allow_build: bool) -> None:
        self._allow_build = allow_build

    _allow_download: bool = True

    @property
    def allow_download(self) -> bool:
        return self._allow_download

    @allow_download.setter
    def allow_download(self, allow_download: bool) -> None:
        self._allow_download = allow_download

    def _resource_path(self, *paths: str) -> str:
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

    @property
    def _repository_path(self) -> str:
        return self._resource_path("data", "tree-sitter-talon")

    @property
    def _package_json_path(self) -> str:
        return self._resource_path("data", "tree-sitter-talon", "package.json")

    @property
    def _node_types_json_path(self) -> str:
        return self._resource_path(
            "data", "tree-sitter-talon", "src", "node-types.json"
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
    def _tree_sitter_talon_version(self) -> str:
        package_json_path = pathlib.Path(
            self._resource_path("data", "tree-sitter-talon", "package.json")
        )
        package_json = json.loads(package_json_path.read_text())
        return package_json["version"]

    @property
    def _library_names(self) -> collections.abc.Iterator[str]:
        version = self._tree_sitter_talon_version
        system = platform.system()
        machine = platform.machine()
        ext = {"Linux": "so", "Darwin": "dylib", "Windows": "dll"}.get(system, None)
        if ext is None:
            raise RuntimeError(f"Unsupported platform '{system}'")
        yield f"tree_sitter_talon-{version}-{machine}.{ext}"
        yield f"tree_sitter_talon-{version}.{ext}"
        yield f"tree_sitter_talon.{ext}"

    @property
    def library_name(self) -> str:
        return os.path.basename(self.library_path)

    @property
    def library_path(self) -> str:
        library_path = self.find_library()
        if library_path:
            return library_path
        else:
            raise FileNotFoundError(tuple(self._library_names))

    @library_path.setter
    def library_path(self, library_or_library_path: str) -> None:
        if os.path.exists(library_or_library_path):
            if os.path.isdir(library_or_library_path):
                self.find_library(library_or_library_path)
            else:
                self._library_path = library_or_library_path

    def find_library(self, *extra_library_paths: str) -> typing.Optional[str]:
        if not self._library_path:
            for library_name in self._library_names:
                # try extra_library_path
                for extra_library_path in extra_library_paths:
                    library_path = os.path.join(extra_library_path, library_name)
                    if os.path.exists(library_path):
                        self._library_path = library_path
                        return self._library_path
                # try package resource_path
                try:
                    library_path = self._resource_path("data", library_name)
                    if library_path:
                        self._library_path = library_path
                        return self._library_path
                except FileNotFoundError:
                    pass
                # try DEFAULT_LIBRARY_PATH
                library_path = os.path.join(self.DEFAULT_LIBRARY_PATH, library_name)
                if os.path.exists(library_path):
                    self._library_path = library_path
                    return self._library_path
                # try ctypes.util.find_library
                self._library_path = ctypes.util.find_library(library_name)
                if self._library_path:
                    return self._library_path
        return self._library_path

    def _or_default_library_path(
        self, library_path: typing.Optional[str]
    ) -> tuple[str, str]:
        library_name = next(self._library_names)
        if library_path:
            return (os.path.join(library_path, library_name), library_name)
        else:
            return (os.path.join(self.DEFAULT_LIBRARY_PATH, library_name), library_name)

    def build_library(
        self, library_path: typing.Optional[str] = None
    ) -> typing.Optional[str]:
        if self.allow_build:
            library_path, _ = self._or_default_library_path(library_path)
            logging.info(f"Building {os.path.basename(library_path)}")
            tree_sitter.Language.build_library(library_path, [self._repository_path])
            self._library_path = library_path
            return self._library_path
        return None

    def download_library(
        self, library_path: typing.Optional[str] = None
    ) -> typing.Optional[str]:
        if self.allow_download:
            library_path, library_name = self._or_default_library_path(library_path)
            logging.info(f"Downloading {library_name}")
            url = f"https://github.com/wenkokke/py-tree-sitter-talon/releases/download/{self.__version__}/{library_name}"
            self._library_path = wget.download(url, library_path)
            return self._library_path
        return None

    @property
    def language(self) -> tree_sitter.Language:
        if not self._language:
            error_buffer: list[typing.Union[FileNotFoundError, OSError]] = []
            try:
                # try to load library_path
                self._language = tree_sitter.Language(self.library_path, "talon")
                return self._language
            except (FileNotFoundError, OSError) as e:
                error_buffer.append(e)
                logging.warn(f"Could not load {tuple(self._library_names)}", e)
            try:
                # fallback #1: rebuild library
                library_path = self.build_library()
                if library_path:
                    self._language = tree_sitter.Language(library_path, "talon")
                    return self._language
            except (FileNotFoundError, OSError) as e:
                error_buffer.append(e)
                logging.warn(f"Could not build {tuple(self._library_names)}", e)
            try:
                # fallback #2: download library
                library_path = self.download_library()
                if library_path:
                    self._language = tree_sitter.Language(library_path, "talon")
                    return self._language
            except (FileNotFoundError, OSError) as e:
                error_buffer.append(e)
                logging.warn(f"Could not download {tuple(self._library_names)}", e)
            raise OSError(
                f"Could not find, build, or download {tuple(self._library_names)}",
                *error_buffer,
            )
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
