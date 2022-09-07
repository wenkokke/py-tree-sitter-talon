import dataclasses
import pathlib
import re
import typing

import tree_sitter  # type: ignore
from tree_sitter_type_provider import Branch as Branch
from tree_sitter_type_provider import Leaf as Leaf
from tree_sitter_type_provider import Node as Node
from tree_sitter_type_provider import NodeTypeError as NodeTypeError
from tree_sitter_type_provider import NodeTypeName as NodeTypeName
from tree_sitter_type_provider import ParseError as ParseError
from tree_sitter_type_provider import Point as Point

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
        typing.Union[TalonDeclaration, TalonMatches, TalonComment]
    ]

class TalonComment(Leaf):
    pass

@dataclasses.dataclass
class TalonError(Exception, Branch):
    children: typing.Sequence[Node]
    contents: typing.Optional[str] = None
    filename: typing.Optional[str] = None

# Matches.

@dataclasses.dataclass
class TalonMatches(Branch):
    children: typing.Sequence[typing.Union[TalonMatch, TalonComment]]

@dataclasses.dataclass
class TalonMatch(Branch):
    children: typing.Sequence[TalonComment]
    key: TalonIdentifier
    modifier: typing.Sequence[TalonMatchModifier]
    pattern: TalonImplicitString

class TalonMatchModifier(Leaf):
    pass

# Declarations.

class TalonDeclaration(Node):
    pass

@dataclasses.dataclass
class TalonCommandDeclaration(Branch, TalonDeclaration):
    children: typing.Sequence[TalonComment]
    rule: TalonRule
    script: TalonBlock

@dataclasses.dataclass
class TalonKeyBindingDeclaration(Branch, TalonDeclaration):
    children: typing.Sequence[TalonComment]
    key: TalonKeyAction
    script: TalonBlock

@dataclasses.dataclass
class TalonSettingsDeclaration(Branch, TalonDeclaration):
    children: typing.Sequence[typing.Union[TalonBlock, TalonComment]]

@dataclasses.dataclass
class TalonTagImportDeclaration(Branch, TalonDeclaration):
    children: typing.Sequence[TalonComment]
    tag: TalonIdentifier

# Rules.

@dataclasses.dataclass
class TalonCapture(Branch):
    children: typing.Sequence[TalonComment]
    capture_name: TalonIdentifier
    def to_pattern(
        self,
        *,
        captures: typing.Optional[
            typing.Callable[
                [str],
                typing.Optional[
                    typing.Union[
                        TalonCapture,
                        TalonChoice,
                        TalonEndAnchor,
                        TalonList,
                        TalonOptional,
                        TalonParenthesizedRule,
                        TalonRepeat,
                        TalonRepeat1,
                        TalonRule,
                        TalonSeq,
                        TalonStartAnchor,
                        TalonWord,
                    ]
                ],
            ]
        ] = None,
        lists: typing.Optional[
            typing.Callable[[str], typing.Optional[list[str]]]
        ] = None,
    ) -> re.Pattern[str]: ...

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
    def to_pattern(
        self,
        *,
        captures: typing.Optional[
            typing.Callable[
                [str],
                typing.Optional[
                    typing.Union[
                        TalonCapture,
                        TalonChoice,
                        TalonEndAnchor,
                        TalonList,
                        TalonOptional,
                        TalonParenthesizedRule,
                        TalonRepeat,
                        TalonRepeat1,
                        TalonRule,
                        TalonSeq,
                        TalonStartAnchor,
                        TalonWord,
                    ]
                ],
            ]
        ] = None,
        lists: typing.Optional[
            typing.Callable[[str], typing.Optional[list[str]]]
        ] = None,
    ) -> re.Pattern[str]: ...

class TalonEndAnchor(Leaf):
    def to_pattern(
        self,
        *,
        captures: typing.Optional[
            typing.Callable[
                [str],
                typing.Optional[
                    typing.Union[
                        TalonCapture,
                        TalonChoice,
                        TalonEndAnchor,
                        TalonList,
                        TalonOptional,
                        TalonParenthesizedRule,
                        TalonRepeat,
                        TalonRepeat1,
                        TalonRule,
                        TalonSeq,
                        TalonStartAnchor,
                        TalonWord,
                    ]
                ],
            ]
        ] = None,
        lists: typing.Optional[
            typing.Callable[[str], typing.Optional[list[str]]]
        ] = None,
    ) -> re.Pattern[str]: ...

@dataclasses.dataclass
class TalonList(Branch):
    children: typing.Sequence[TalonComment]
    list_name: TalonIdentifier
    def to_pattern(
        self,
        *,
        captures: typing.Optional[
            typing.Callable[
                [str],
                typing.Optional[
                    typing.Union[
                        TalonCapture,
                        TalonChoice,
                        TalonEndAnchor,
                        TalonList,
                        TalonOptional,
                        TalonParenthesizedRule,
                        TalonRepeat,
                        TalonRepeat1,
                        TalonRule,
                        TalonSeq,
                        TalonStartAnchor,
                        TalonWord,
                    ]
                ],
            ]
        ] = None,
        lists: typing.Optional[
            typing.Callable[[str], typing.Optional[list[str]]]
        ] = None,
    ) -> re.Pattern[str]: ...

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
    def to_pattern(
        self,
        *,
        captures: typing.Optional[
            typing.Callable[
                [str],
                typing.Optional[
                    typing.Union[
                        TalonCapture,
                        TalonChoice,
                        TalonEndAnchor,
                        TalonList,
                        TalonOptional,
                        TalonParenthesizedRule,
                        TalonRepeat,
                        TalonRepeat1,
                        TalonRule,
                        TalonSeq,
                        TalonStartAnchor,
                        TalonWord,
                    ]
                ],
            ]
        ] = None,
        lists: typing.Optional[
            typing.Callable[[str], typing.Optional[list[str]]]
        ] = None,
    ) -> re.Pattern[str]: ...

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
    def to_pattern(
        self,
        *,
        captures: typing.Optional[
            typing.Callable[
                [str],
                typing.Optional[
                    typing.Union[
                        TalonCapture,
                        TalonChoice,
                        TalonEndAnchor,
                        TalonList,
                        TalonOptional,
                        TalonParenthesizedRule,
                        TalonRepeat,
                        TalonRepeat1,
                        TalonRule,
                        TalonSeq,
                        TalonStartAnchor,
                        TalonWord,
                    ]
                ],
            ]
        ] = None,
        lists: typing.Optional[
            typing.Callable[[str], typing.Optional[list[str]]]
        ] = None,
    ) -> re.Pattern[str]: ...

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
    def to_pattern(
        self,
        *,
        captures: typing.Optional[
            typing.Callable[
                [str],
                typing.Optional[
                    typing.Union[
                        TalonCapture,
                        TalonChoice,
                        TalonEndAnchor,
                        TalonList,
                        TalonOptional,
                        TalonParenthesizedRule,
                        TalonRepeat,
                        TalonRepeat1,
                        TalonRule,
                        TalonSeq,
                        TalonStartAnchor,
                        TalonWord,
                    ]
                ],
            ]
        ] = None,
        lists: typing.Optional[
            typing.Callable[[str], typing.Optional[list[str]]]
        ] = None,
    ) -> re.Pattern[str]: ...

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
    def to_pattern(
        self,
        *,
        captures: typing.Optional[
            typing.Callable[
                [str],
                typing.Optional[
                    typing.Union[
                        TalonCapture,
                        TalonChoice,
                        TalonEndAnchor,
                        TalonList,
                        TalonOptional,
                        TalonParenthesizedRule,
                        TalonRepeat,
                        TalonRepeat1,
                        TalonRule,
                        TalonSeq,
                        TalonStartAnchor,
                        TalonWord,
                    ]
                ],
            ]
        ] = None,
        lists: typing.Optional[
            typing.Callable[[str], typing.Optional[list[str]]]
        ] = None,
    ) -> re.Pattern[str]: ...

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
    def to_pattern(
        self,
        *,
        captures: typing.Optional[
            typing.Callable[
                [str],
                typing.Optional[
                    typing.Union[
                        TalonCapture,
                        TalonChoice,
                        TalonEndAnchor,
                        TalonList,
                        TalonOptional,
                        TalonParenthesizedRule,
                        TalonRepeat,
                        TalonRepeat1,
                        TalonRule,
                        TalonSeq,
                        TalonStartAnchor,
                        TalonWord,
                    ]
                ],
            ]
        ] = None,
        lists: typing.Optional[
            typing.Callable[[str], typing.Optional[list[str]]]
        ] = None,
    ) -> re.Pattern[str]: ...

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
    def to_pattern(
        self,
        *,
        captures: typing.Optional[
            typing.Callable[
                [str],
                typing.Optional[
                    typing.Union[
                        TalonCapture,
                        TalonChoice,
                        TalonEndAnchor,
                        TalonList,
                        TalonOptional,
                        TalonParenthesizedRule,
                        TalonRepeat,
                        TalonRepeat1,
                        TalonRule,
                        TalonSeq,
                        TalonStartAnchor,
                        TalonWord,
                    ]
                ],
            ]
        ] = None,
        lists: typing.Optional[
            typing.Callable[[str], typing.Optional[list[str]]]
        ] = None,
    ) -> re.Pattern[str]: ...

class TalonStartAnchor(Leaf):
    def to_pattern(
        self,
        *,
        captures: typing.Optional[
            typing.Callable[
                [str],
                typing.Optional[
                    typing.Union[
                        TalonCapture,
                        TalonChoice,
                        TalonEndAnchor,
                        TalonList,
                        TalonOptional,
                        TalonParenthesizedRule,
                        TalonRepeat,
                        TalonRepeat1,
                        TalonRule,
                        TalonSeq,
                        TalonStartAnchor,
                        TalonWord,
                    ]
                ],
            ]
        ] = None,
        lists: typing.Optional[
            typing.Callable[[str], typing.Optional[list[str]]]
        ] = None,
    ) -> re.Pattern[str]: ...

class TalonWord(Leaf):
    def to_pattern(
        self,
        *,
        captures: typing.Optional[
            typing.Callable[
                [str],
                typing.Optional[
                    typing.Union[
                        TalonCapture,
                        TalonChoice,
                        TalonEndAnchor,
                        TalonList,
                        TalonOptional,
                        TalonParenthesizedRule,
                        TalonRepeat,
                        TalonRepeat1,
                        TalonRule,
                        TalonSeq,
                        TalonStartAnchor,
                        TalonWord,
                    ]
                ],
            ]
        ] = None,
        lists: typing.Optional[
            typing.Callable[[str], typing.Optional[list[str]]]
        ] = None,
    ) -> re.Pattern[str]: ...

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

class TalonFloat(Leaf, TalonNumber):
    pass

class TalonInteger(Leaf, TalonNumber):
    pass

class TalonNumber(Node):
    pass
