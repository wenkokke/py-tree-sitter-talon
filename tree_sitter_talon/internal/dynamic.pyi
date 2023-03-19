import dataclasses
import pathlib
import typing

import dataclasses_json
import tree_sitter

from . import __version__
from .match import AnyListValue, AnyTalonRule

################################################################################
# Extended node types (from tree-sitter-type-provider)
################################################################################

class NodeTypeError(Exception):
    pass

@dataclasses.dataclass
class Point:
    line: int
    column: int

    @staticmethod
    def from_tree_sitter(tspoint: typing.Tuple[int, int]) -> "Point":
        return Point(line=tspoint[0], column=tspoint[1])

NodeTypeName = str

NodeFieldName = str

@dataclasses.dataclass
class Node(dataclasses_json.DataClassJsonMixin):
    text: str
    type_name: NodeTypeName = dataclasses.field(
        metadata=dataclasses_json.config(field_name="type")
    )
    start_position: Point
    end_position: Point

    def is_extra(self) -> bool: ...
    def is_equivalent(self, other: "Node") -> bool: ...
    def assert_equivalent(self, other: "Node") -> None: ...

@dataclasses.dataclass
class Leaf(Node):
    pass

@dataclasses.dataclass
class Branch(Node):
    children: typing.Union[None, Node, typing.Sequence[Node]]

@dataclasses.dataclass
class ParseError(Exception, Branch):
    children: typing.List[Node]
    contents: typing.Optional[str] = None
    filename: typing.Optional[str] = None

parser: tree_sitter.Parser

language: tree_sitter.Language

def parse(
    contents: typing.Union[str, bytes],
    *,
    encoding: str = "utf-8",
    filename: typing.Optional[str] = None,
    raise_parse_error: bool = False,
) -> Node: ...
def parse_file(
    path: typing.Union[str, pathlib.Path],
    *,
    encoding: str = "utf-8",
    raise_parse_error: bool = False,
) -> Node: ...
def from_tree_sitter(
    tsvalue: typing.Union[tree_sitter.Tree, tree_sitter.Node, tree_sitter.TreeCursor],
    *,
    encoding: str = "utf-8",
    filename: typing.Optional[str] = None,
    raise_parse_error: bool = False,
) -> Node: ...

# AST node classes.

@dataclasses.dataclass
class TalonSourceFile(Branch):
    children: typing.Sequence[
        typing.Union[TalonDeclarations, TalonMatches, TalonComment]
    ]
    def get_docstring(self) -> typing.Optional[str]: ...
    def find_command(
        self,
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> typing.Optional["TalonCommandDeclaration"]: ...

class TalonComment(Leaf):
    def get_docstring(self) -> typing.Optional[str]: ...

@dataclasses.dataclass
class TalonError(Exception, Branch):
    children: typing.Sequence[Node]
    contents: typing.Optional[str] = None
    filename: typing.Optional[str] = None

# Matches.

@dataclasses.dataclass
class TalonMatches(Branch):
    children: typing.Sequence[typing.Union[TalonMatch, TalonComment]]

    def is_explicit(self) -> bool: ...

@dataclasses.dataclass
class TalonMatch(Branch):
    children: typing.Sequence[TalonComment]
    left: TalonIdentifier
    modifiers: typing.Sequence[TalonMatchModifier]
    right: TalonImplicitString

    @property
    def key(self) -> TalonIdentifier: ...
    @property
    def modifier(self) -> typing.Sequence[TalonMatchModifier]: ...
    @property
    def pattern(self) -> TalonImplicitString: ...

class TalonMatchModifier(Leaf):
    pass

# Declarations.

class TalonDeclarations(Branch):
    children: typing.Sequence[TalonDeclaration]

class TalonDeclaration(Node):
    pass

@dataclasses.dataclass(init=False)
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
        children: typing.Optional[typing.Sequence[TalonComment]],
        left: TalonRule,
        right: TalonBlock,
    ) -> None: ...
    @property
    def rule(self) -> TalonRule: ...
    @property
    def script(self) -> TalonBlock: ...
    def get_docstring(self) -> typing.Optional[str]: ...
    def match(
        self,
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...
    def is_short(self) -> bool: ...

@dataclasses.dataclass(init=False)
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
        children: typing.Optional[typing.Sequence[TalonComment]],
        left: TalonKeyAction,
        right: TalonBlock,
    ) -> None: ...
    @property
    def key(self) -> TalonKeyAction: ...
    @property
    def script(self) -> TalonBlock: ...
    def is_short(self) -> bool: ...

@dataclasses.dataclass(init=False)
class TalonSettingsDeclaration(Branch, TalonDeclaration):
    children: None
    right: TalonBlock

    def __init__(
        self,
        text: str,
        type_name: NodeTypeName,
        start_position: Point,
        end_position: Point,
        children: typing.Optional[typing.Sequence[TalonComment]],
        right: TalonBlock,
    ) -> None: ...
    def is_short(self) -> bool: ...

@dataclasses.dataclass
class TalonTagImportDeclaration(Branch, TalonDeclaration):
    children: typing.Sequence[TalonComment]
    right: TalonIdentifier

    @property
    def tag(self) -> TalonIdentifier: ...

# Rules.

@dataclasses.dataclass
class TalonCapture(Branch):
    children: typing.Sequence[TalonComment]
    capture_name: TalonIdentifier
    def match(
        self,
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...

@dataclasses.dataclass
class TalonChoice(Branch):
    children: typing.Sequence[
        typing.Union[
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
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...

class TalonEndAnchor(Leaf):
    def match(
        self,
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...

@dataclasses.dataclass
class TalonList(Branch):
    children: typing.Sequence[TalonComment]
    list_name: TalonIdentifier
    def match(
        self,
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...

@dataclasses.dataclass
class TalonOptional(Branch):
    children: typing.Sequence[
        typing.Union[
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
    ) -> typing.Union[
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
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...

@dataclasses.dataclass
class TalonParenthesizedRule(Branch):
    children: typing.Sequence[
        typing.Union[
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
    ) -> typing.Union[
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
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...

@dataclasses.dataclass
class TalonRepeat(Branch):
    children: typing.Sequence[
        typing.Union[
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
    ) -> typing.Union[
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
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...

@dataclasses.dataclass
class TalonRepeat1(Branch):
    children: typing.Sequence[
        typing.Union[
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
    ) -> typing.Union[
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
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...

@dataclasses.dataclass
class TalonRule(Branch):
    children: typing.Sequence[
        typing.Union[
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
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...

@dataclasses.dataclass
class TalonSeq(Branch):
    children: typing.Sequence[
        typing.Union[
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
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...

class TalonStartAnchor(Leaf):
    def match(
        self,
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...

class TalonWord(Leaf):
    def match(
        self,
        text: typing.Sequence[str],
        *,
        fullmatch: bool = False,
        get_capture: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyTalonRule]]
        ] = None,
        get_list: typing.Optional[
            typing.Callable[[str], typing.Optional[AnyListValue]]
        ] = None,
    ) -> bool: ...

# Statements.

class TalonStatement(Node):
    pass

@dataclasses.dataclass
class TalonAssignmentStatement(Branch, TalonStatement):
    children: typing.Sequence[TalonComment]
    left: TalonIdentifier
    right: TalonExpression

@dataclasses.dataclass
class TalonExpressionStatement(Branch, TalonStatement):
    children: typing.Sequence[TalonComment]
    expression: TalonExpression

@dataclasses.dataclass
class TalonBlock(Branch):
    children: typing.Sequence[typing.Union[TalonStatement, TalonComment]]

    def is_short(self) -> bool: ...

# Expressions.

class TalonExpression(Node):
    pass

@dataclasses.dataclass
class TalonAction(Branch, TalonExpression):
    children: typing.Sequence[TalonComment]
    action_name: TalonIdentifier
    arguments: TalonArgumentList

@dataclasses.dataclass
class TalonArgumentList(Branch):
    children: typing.Sequence[typing.Union[TalonExpression, TalonComment]]

@dataclasses.dataclass
class TalonUnaryOperator(Branch, TalonExpression):
    children: typing.Sequence[TalonComment]
    operator: TalonOperator
    right: TalonExpression

@dataclasses.dataclass
class TalonBinaryOperator(Branch, TalonExpression):
    children: typing.Sequence[TalonComment]
    left: TalonExpression
    operator: TalonOperator
    right: TalonExpression

@dataclasses.dataclass
class TalonKeyAction(Branch, TalonExpression):
    children: typing.Sequence[TalonComment]
    arguments: TalonImplicitString

@dataclasses.dataclass
class TalonParenthesizedExpression(Branch, TalonExpression):
    children: typing.Sequence[typing.Union[TalonExpression, TalonComment]]

    def get_child(self) -> TalonExpression: ...

@dataclasses.dataclass
class TalonSleepAction(Branch, TalonExpression):
    children: typing.Sequence[TalonComment]
    arguments: TalonImplicitString

@dataclasses.dataclass
class TalonVariable(Branch, TalonExpression):
    children: typing.Sequence[TalonComment]
    variable_name: TalonIdentifier

# Identifiers.

class TalonIdentifier(Leaf):
    pass

class TalonOperator(Leaf):
    pass

# Strings.

class TalonImplicitString(Leaf):
    pass

@dataclasses.dataclass
class TalonInterpolation(Branch):
    children: typing.Sequence[typing.Union[TalonExpression, TalonComment]]

    def get_child(self) -> TalonExpression: ...

@dataclasses.dataclass
class TalonString(Branch):
    children: typing.Sequence[
        typing.Union[
            TalonInterpolation,
            TalonStringContent,
            TalonStringEscapeSequence,
            TalonComment,
        ]
    ]

class TalonStringContent(Leaf):
    pass

class TalonStringEscapeSequence(Leaf):
    pass

# Numbers.

class TalonNumber(Node):
    pass

class TalonFloat(Leaf, TalonNumber):
    pass

class TalonInteger(Leaf, TalonNumber):
    pass
