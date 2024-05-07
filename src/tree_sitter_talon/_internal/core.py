from pathlib import Path
from typing import List, Optional, Sequence, Union

import importlib_resources
import tree_sitter
import tree_sitter_type_provider

from .binding import _tree_sitter_talon_id

################################################################################
# Export List
################################################################################

__all__: List[str] = [
    "TalonLanguage",
    "TreeSitterTalon",
]


################################################################################
# Core Classes
################################################################################


class TalonLanguage(tree_sitter.Language):  # type: ignore
    def __init__(self) -> None:
        super().__init__(_tree_sitter_talon_id(), "talon")


class TreeSitterTalon(tree_sitter_type_provider.TreeSitterTypeProvider):  # type: ignore
    _library_path: Optional[str] = None

    _language: Optional[tree_sitter.Language] = None

    _parser: Optional[tree_sitter.Parser] = None

    @property
    def _node_types(
        self,
    ) -> Sequence[tree_sitter_type_provider.NodeType]:
        _node_types_text = (
            importlib_resources.files("tree_sitter_talon")
            .joinpath("_tree_sitter_talon", "src", "node-types.json")
            .read_text(encoding="utf-8")
        )
        return tree_sitter_type_provider.NodeType.schema().loads(  # type: ignore
            _node_types_text, many=True
        )

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

    def __init__(self) -> None:
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
        self.NodeFieldName = tree_sitter_type_provider.NodeFieldName
        self.Node = tree_sitter_type_provider.Node
        self.Leaf = tree_sitter_type_provider.Leaf
        self.Branch = tree_sitter_type_provider.Branch
        self.Point = tree_sitter_type_provider.Point
        self.ParseError = tree_sitter_type_provider.ParseError

        ################################################################################
        # Export List
        ################################################################################

        self.__all__: List[str] = [
            "parser",
            "language",
            "parse",
            "parse_file",
            "from_tree_sitter",
            "NodeTypeName",
            "NodeFieldName",
            "NodeTypeError",
            "Point",
            "Node",
            "Leaf",
            "Branch",
            "ParseError",
            "TalonSourceFile",
            "TalonComment",
            "TalonError",
            "TalonMatches",
            "TalonMatch",
            "TalonMatchModifier",
            "TalonDeclarations",
            "TalonDeclaration",
            "TalonCommandDeclaration",
            "TalonKeyBindingDeclaration",
            "TalonSettingsDeclaration",
            "TalonTagImportDeclaration",
            "TalonCapture",
            "TalonChoice",
            "TalonEndAnchor",
            "TalonList",
            "TalonOptional",
            "TalonParenthesizedRule",
            "TalonRepeat",
            "TalonRepeat1",
            "TalonRule",
            "TalonSeq",
            "TalonStartAnchor",
            "TalonWord",
            "TalonStatement",
            "TalonAssignmentStatement",
            "TalonExpressionStatement",
            "TalonBlock",
            "TalonExpression",
            "TalonAction",
            "TalonArgumentList",
            "TalonUnaryOperator",
            "TalonBinaryOperator",
            "TalonKeyAction",
            "TalonParenthesizedExpression",
            "TalonSleepAction",
            "TalonVariable",
            "TalonIdentifier",
            "TalonOperator",
            "TalonImplicitString",
            "TalonInterpolation",
            "TalonString",
            "TalonStringContent",
            "TalonStringEscapeSequence",
            "TalonNumber",
            "TalonFloat",
            "TalonInteger",
        ]

    def parse(
        self,
        contents: Union[str, bytes],
        *,
        encoding: str = "utf-8",
        filename: Optional[str] = None,
        raise_parse_error: bool = False,
    ) -> Optional[
        Union[
            tree_sitter_type_provider.Node,
            Sequence[tree_sitter_type_provider.Node],
        ]
    ]:
        tree = self._parse(contents, encoding=encoding)
        return self.from_tree_sitter(
            tree.root_node,
            encoding=encoding,
            filename=filename,
            raise_parse_error=raise_parse_error,
        )

    def parse_file(
        self,
        path: Union[str, Path],
        *,
        encoding: str = "utf-8",
        raise_parse_error: bool = False,
    ) -> Optional[
        Union[
            tree_sitter_type_provider.Node,
            Sequence[tree_sitter_type_provider.Node],
        ]
    ]:
        tree = self._parse_file(path, encoding=encoding)
        return self.from_tree_sitter(
            tree.root_node,
            encoding=encoding,
            filename=str(path),
            raise_parse_error=raise_parse_error,
        )

    def _parse(
        self,
        contents: Union[str, bytes],
        *,
        encoding: str = "utf-8",
    ) -> tree_sitter.Tree:
        if isinstance(contents, str):
            contents = bytes(contents, encoding)
        return self.parser.parse(contents)

    def _parse_file(
        self,
        path: Union[str, Path],
        *,
        encoding: str = "utf-8",
    ) -> tree_sitter.Tree:
        if not isinstance(path, Path):
            path = Path(path)
        contents = path.read_bytes()
        return self._parse(contents, encoding=encoding)
