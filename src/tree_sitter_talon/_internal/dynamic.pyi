from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple, Union

import tree_sitter
from dataclasses_json import DataClassJsonMixin, config

from .match import AnyTalonRule, ListValue

################################################################################
# Export List
################################################################################

__all__: List[str] = [
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

################################################################################
# Extended node types (from tree-sitter-type-provider)
################################################################################

class NodeTypeError(Exception):
    pass

@dataclass
class Point:
    line: int
    column: int

    @staticmethod
    def from_tree_sitter(tspoint: Tuple[int, int]) -> "Point":
        return Point(line=tspoint[0], column=tspoint[1])

NodeTypeName = str

NodeFieldName = str

@dataclass
class Node(DataClassJsonMixin):
    text: str
    type_name: NodeTypeName = field(metadata=config(field_name="type"))
    start_position: Point
    end_position: Point

    def is_extra(self) -> bool: ...
    def is_equivalent(self, other: "Node") -> bool: ...
    def assert_equivalent(self, other: "Node") -> None: ...

@dataclass
class Leaf(Node):
    pass

@dataclass
class Branch(Node):
    children: Union[None, Node, Sequence[Node]]

@dataclass
class ParseError(Exception, Branch):
    children: List[Node]
    contents: Optional[str] = None
    filename: Optional[str] = None

parser: tree_sitter.Parser

language: tree_sitter.Language

def parse(
    contents: Union[str, bytes],
    *,
    encoding: str = "utf-8",
    filename: Optional[str] = None,
    raise_parse_error: bool = False,
) -> Node: ...
def parse_file(
    path: Union[str, Path],
    *,
    encoding: str = "utf-8",
    raise_parse_error: bool = False,
) -> Node: ...
def from_tree_sitter(
    tsvalue: Union[tree_sitter.Tree, tree_sitter.Node, tree_sitter.TreeCursor],
    *,
    encoding: str = "utf-8",
    filename: Optional[str] = None,
    raise_parse_error: bool = False,
) -> Node: ...

# AST node classes.

@dataclass
class TalonSourceFile(Branch):
    children: Sequence[Union[TalonDeclarations, TalonMatches, TalonComment]]
    def get_docstring(self) -> Optional[str]: ...
    def find_command(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> Optional["TalonCommandDeclaration"]: ...

@dataclass
class TalonComment(Leaf):
    def get_docstring(self) -> Optional[str]: ...

@dataclass
class TalonError(Exception, Branch):
    children: Sequence[Node]
    contents: Optional[str] = None
    filename: Optional[str] = None

# Matches.

@dataclass
class TalonMatches(Branch):
    children: Sequence[Union[TalonMatch, TalonComment]]

    def is_explicit(self) -> bool: ...

@dataclass
class TalonMatch(Branch):
    children: Sequence[TalonComment]
    left: TalonIdentifier
    modifiers: Sequence[TalonMatchModifier]
    right: TalonImplicitString

    @property
    def key(self) -> TalonIdentifier: ...
    @property
    def modifier(self) -> Sequence[TalonMatchModifier]: ...
    @property
    def pattern(self) -> TalonImplicitString: ...

@dataclass
class TalonMatchModifier(Leaf):
    pass

# Declarations.

@dataclass
class TalonDeclarations(Branch):
    children: Sequence[TalonDeclaration]

@dataclass
class TalonDeclaration(Node):
    pass

@dataclass(init=False)
class TalonCommandDeclaration(Branch, TalonDeclaration):
    children: None
    left: TalonRule
    right: TalonBlock

    def __init__(
        self,
        text: str,
        type_name: NodeTypeName,
        start_position: Point,
        end_position: Point,
        children: Optional[Sequence[TalonComment]],
        left: TalonRule,
        right: TalonBlock,
    ) -> None: ...
    @property
    def rule(self) -> TalonRule: ...
    @property
    def script(self) -> TalonBlock: ...
    def get_docstring(self) -> Optional[str]: ...
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...
    def is_short(self) -> bool: ...

@dataclass(init=False)
class TalonKeyBindingDeclaration(Branch, TalonDeclaration):
    children: None
    left: TalonKeyAction
    right: TalonBlock

    def __init__(
        self,
        text: str,
        type_name: NodeTypeName,
        start_position: Point,
        end_position: Point,
        children: Optional[Sequence[TalonComment]],
        left: TalonKeyAction,
        right: TalonBlock,
    ) -> None: ...
    @property
    def key(self) -> TalonKeyAction: ...
    @property
    def script(self) -> TalonBlock: ...
    def is_short(self) -> bool: ...

@dataclass(init=False)
class TalonSettingsDeclaration(Branch, TalonDeclaration):
    children: None
    right: TalonBlock

    def __init__(
        self,
        text: str,
        type_name: NodeTypeName,
        start_position: Point,
        end_position: Point,
        children: Optional[Sequence[TalonComment]],
        right: TalonBlock,
    ) -> None: ...
    def is_short(self) -> bool: ...

@dataclass
class TalonTagImportDeclaration(Branch, TalonDeclaration):
    children: Sequence[TalonComment]
    right: TalonIdentifier

    @property
    def tag(self) -> TalonIdentifier: ...

# Rules.

@dataclass
class TalonCapture(Branch):
    children: Sequence[TalonComment]
    capture_name: TalonIdentifier
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...

@dataclass
class TalonChoice(Branch):
    children: Sequence[
        Union[
            TalonCapture,
            TalonEndAnchor,
            TalonList,
            TalonOptional,
            TalonParenthesizedRule,
            TalonRepeat,
            TalonRepeat1,
            TalonSeq,
            TalonStartAnchor,
            TalonWord,
            TalonComment,
        ]
    ]
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...

@dataclass
class TalonEndAnchor(Leaf):
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...

@dataclass
class TalonList(Branch):
    children: Sequence[TalonComment]
    list_name: TalonIdentifier
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...

@dataclass
class TalonOptional(Branch):
    children: Sequence[
        Union[
            TalonCapture,
            TalonChoice,
            TalonEndAnchor,
            TalonList,
            TalonOptional,
            TalonParenthesizedRule,
            TalonRepeat,
            TalonRepeat1,
            TalonSeq,
            TalonStartAnchor,
            TalonWord,
            TalonComment,
        ]
    ]
    def get_child(
        self,
    ) -> Union[
        TalonCapture,
        TalonChoice,
        TalonEndAnchor,
        TalonList,
        TalonOptional,
        TalonParenthesizedRule,
        TalonRepeat,
        TalonRepeat1,
        TalonSeq,
        TalonStartAnchor,
        TalonWord,
    ]: ...
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...

@dataclass
class TalonParenthesizedRule(Branch):
    children: Sequence[
        Union[
            TalonCapture,
            TalonChoice,
            TalonEndAnchor,
            TalonList,
            TalonOptional,
            TalonParenthesizedRule,
            TalonRepeat,
            TalonRepeat1,
            TalonSeq,
            TalonStartAnchor,
            TalonWord,
            TalonComment,
        ]
    ]
    def get_child(
        self,
    ) -> Union[
        TalonCapture,
        TalonChoice,
        TalonEndAnchor,
        TalonList,
        TalonOptional,
        TalonParenthesizedRule,
        TalonRepeat,
        TalonRepeat1,
        TalonSeq,
        TalonStartAnchor,
        TalonWord,
    ]: ...
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...

@dataclass
class TalonRepeat(Branch):
    children: Sequence[
        Union[
            TalonCapture,
            TalonList,
            TalonOptional,
            TalonParenthesizedRule,
            TalonRepeat,
            TalonRepeat1,
            TalonWord,
            TalonComment,
        ]
    ]
    def get_child(
        self,
    ) -> Union[
        TalonCapture,
        TalonList,
        TalonOptional,
        TalonParenthesizedRule,
        TalonRepeat,
        TalonRepeat1,
        TalonWord,
    ]: ...
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...

@dataclass
class TalonRepeat1(Branch):
    children: Sequence[
        Union[
            TalonCapture,
            TalonList,
            TalonOptional,
            TalonParenthesizedRule,
            TalonRepeat,
            TalonRepeat1,
            TalonWord,
            TalonComment,
        ]
    ]
    def get_child(
        self,
    ) -> Union[
        TalonCapture,
        TalonList,
        TalonOptional,
        TalonParenthesizedRule,
        TalonRepeat,
        TalonRepeat1,
        TalonWord,
    ]: ...
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...

@dataclass
class TalonRule(Branch):
    children: Sequence[
        Union[
            TalonCapture,
            TalonChoice,
            TalonEndAnchor,
            TalonList,
            TalonOptional,
            TalonParenthesizedRule,
            TalonRepeat,
            TalonRepeat1,
            TalonSeq,
            TalonStartAnchor,
            TalonWord,
            TalonComment,
        ]
    ]
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...

@dataclass
class TalonSeq(Branch):
    children: Sequence[
        Union[
            TalonCapture,
            TalonList,
            TalonOptional,
            TalonParenthesizedRule,
            TalonRepeat,
            TalonRepeat1,
            TalonWord,
            TalonComment,
        ]
    ]
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...

@dataclass
class TalonStartAnchor(Leaf):
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...

@dataclass
class TalonWord(Leaf):
    def match(
        self,
        text: Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: Optional[Callable[[str], Optional[AnyTalonRule]]] = None,
        get_list: Optional[Callable[[str], Optional[ListValue]]] = None,
    ) -> bool: ...

# Statements.

@dataclass
class TalonStatement(Node):
    pass

@dataclass
class TalonAssignmentStatement(Branch, TalonStatement):
    children: Sequence[TalonComment]
    left: TalonIdentifier
    right: TalonExpression

@dataclass
class TalonExpressionStatement(Branch, TalonStatement):
    children: Sequence[TalonComment]
    expression: TalonExpression

@dataclass
class TalonBlock(Branch):
    children: Sequence[Union[TalonStatement, TalonComment]]

    def is_short(self) -> bool: ...

# Expressions.

@dataclass
class TalonExpression(Node):
    pass

@dataclass
class TalonAction(Branch, TalonExpression):
    children: Sequence[TalonComment]
    action_name: TalonIdentifier
    arguments: TalonArgumentList

@dataclass
class TalonArgumentList(Branch):
    children: Sequence[Union[TalonExpression, TalonComment]]

@dataclass
class TalonUnaryOperator(Branch, TalonExpression):
    children: Sequence[TalonComment]
    operator: TalonOperator
    right: TalonExpression

@dataclass
class TalonBinaryOperator(Branch, TalonExpression):
    children: Sequence[TalonComment]
    left: TalonExpression
    operator: TalonOperator
    right: TalonExpression

@dataclass
class TalonKeyAction(Branch, TalonExpression):
    children: Sequence[TalonComment]
    arguments: TalonImplicitString

@dataclass
class TalonParenthesizedExpression(Branch, TalonExpression):
    children: Sequence[Union[TalonExpression, TalonComment]]

    def get_child(self) -> TalonExpression: ...

@dataclass
class TalonSleepAction(Branch, TalonExpression):
    children: Sequence[TalonComment]
    arguments: TalonImplicitString

@dataclass
class TalonVariable(Branch, TalonExpression):
    children: Sequence[TalonComment]
    variable_name: TalonIdentifier

# Identifiers.

@dataclass
class TalonIdentifier(Leaf):
    pass

@dataclass
class TalonOperator(Leaf):
    pass

# Strings.

@dataclass
class TalonImplicitString(Leaf):
    pass

@dataclass
class TalonInterpolation(Branch):
    children: Sequence[Union[TalonExpression, TalonComment]]

    def get_child(self) -> TalonExpression: ...

@dataclass
class TalonString(Branch):
    children: Sequence[
        Union[
            TalonInterpolation,
            TalonStringContent,
            TalonStringEscapeSequence,
            TalonComment,
        ]
    ]

@dataclass
class TalonStringContent(Leaf):
    pass

@dataclass
class TalonStringEscapeSequence(Leaf):
    pass

# Numbers.

@dataclass
class TalonNumber(Node):
    pass

@dataclass
class TalonFloat(Leaf, TalonNumber):
    pass

@dataclass
class TalonInteger(Leaf, TalonNumber):
    pass
