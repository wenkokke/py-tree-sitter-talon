import dataclasses
import pathlib
import typing

import dataclasses_json
import tree_sitter  # type: ignore
from tree_sitter_type_provider.node_types import Branch as Branch
from tree_sitter_type_provider.node_types import Leaf as Leaf
from tree_sitter_type_provider.node_types import Node as Node
from tree_sitter_type_provider.node_types import NodeTypeError as NodeTypeError
from tree_sitter_type_provider.node_types import NodeTypeName as NodeTypeName
from tree_sitter_type_provider.node_types import Point as Point

parser: tree_sitter.Parser

language: tree_sitter.Language

def parse(
    contents: typing.Union[str, bytes],
    *,
    has_header: typing.Optional[bool] = None,
    encoding: str = "utf-8",
) -> Node: ...
def parse_file(
    path: typing.Union[str, pathlib.Path],
    *,
    has_header: typing.Optional[bool] = None,
    encoding: str = "utf-8",
) -> Node: ...
def parse_as_tree_sitter(
    contents: typing.Union[str, bytes],
    *,
    has_header: typing.Optional[bool] = None,
    encoding: str = "utf-8",
) -> tree_sitter.Tree: ...
def parse_file_as_tree_sitter(
    path: typing.Union[str, pathlib.Path],
    *,
    has_header: typing.Optional[bool] = None,
    encoding: str = "utf-8",
) -> tree_sitter.Tree: ...
def from_tree_sitter(
    tsvalue: typing.Union[tree_sitter.Tree, tree_sitter.Node, tree_sitter.TreeCursor],
    *,
    encoding: str = "utf-8",
) -> Node: ...
@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonAction(Branch):
    children: list[TalonComment]
    action_name: TalonIdentifier
    arguments: TalonArgumentList

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonAnd(Branch):
    children: list[typing.Union[TalonAnd, TalonMatch, TalonNot, TalonComment]]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonArgumentList(Branch):
    children: list[
        typing.Union[
            TalonAction,
            TalonBinaryOperator,
            TalonFloat,
            TalonInteger,
            TalonKeyAction,
            TalonParenthesizedExpression,
            TalonSleepAction,
            TalonString,
            TalonVariable,
            TalonComment,
        ]
    ]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonAssignment(Branch):
    children: list[TalonComment]
    left: TalonIdentifier
    right: typing.Union[
        TalonAction,
        TalonBinaryOperator,
        TalonFloat,
        TalonInteger,
        TalonKeyAction,
        TalonParenthesizedExpression,
        TalonSleepAction,
        TalonString,
        TalonVariable,
        TalonComment,
    ]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonBinaryOperator(Branch):
    children: list[TalonComment]
    left: typing.Union[
        TalonAction,
        TalonBinaryOperator,
        TalonFloat,
        TalonInteger,
        TalonKeyAction,
        TalonParenthesizedExpression,
        TalonSleepAction,
        TalonString,
        TalonVariable,
        TalonComment,
    ]
    operator: TalonOperator
    right: typing.Union[
        TalonAction,
        TalonBinaryOperator,
        TalonFloat,
        TalonInteger,
        TalonKeyAction,
        TalonParenthesizedExpression,
        TalonSleepAction,
        TalonString,
        TalonVariable,
        TalonComment,
    ]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonBlock(Branch):
    children: list[
        typing.Union[TalonAssignment, TalonDocstring, TalonExpression, TalonComment]
    ]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonCapture(Branch):
    children: list[TalonComment]
    capture_name: TalonIdentifier

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonChoice(Branch):
    children: list[
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

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonCommand(Branch):
    children: list[TalonComment]
    rule: TalonRule
    script: TalonBlock

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonComment(Leaf):
    pass

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonContext(Branch):
    children: list[
        typing.Union[
            TalonAnd, TalonDocstring, TalonMatch, TalonNot, TalonOr, TalonComment
        ]
    ]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonDocstring(Leaf):
    pass

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonEndAnchor(Leaf):
    pass

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonError(Branch):
    children: list[
        typing.Union[
            TalonAction,
            TalonAnd,
            TalonArgumentList,
            TalonAssignment,
            TalonBinaryOperator,
            TalonBlock,
            TalonCapture,
            TalonChoice,
            TalonCommand,
            TalonContext,
            TalonExpression,
            TalonIncludeTag,
            TalonInterpolation,
            TalonKeyAction,
            TalonList,
            TalonMatch,
            TalonNot,
            TalonNumber,
            TalonOptional,
            TalonOr,
            TalonParenthesizedExpression,
            TalonParenthesizedRule,
            TalonRegexEscapeSequence,
            TalonRepeat,
            TalonRepeat1,
            TalonRule,
            TalonSeq,
            TalonSettings,
            TalonSleepAction,
            TalonSourceFile,
            TalonString,
            TalonStringContent,
            TalonVariable,
            TalonComment,
            TalonDocstring,
            TalonEndAnchor,
            TalonFloat,
            TalonIdentifier,
            TalonImplicitString,
            TalonInteger,
            TalonOperator,
            TalonStartAnchor,
            TalonStringEscapeSequence,
            TalonWord,
            TalonError,
        ]
    ]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonExpression(Branch):
    children: list[TalonComment]
    expression: typing.Union[
        TalonAction,
        TalonBinaryOperator,
        TalonFloat,
        TalonInteger,
        TalonKeyAction,
        TalonParenthesizedExpression,
        TalonSleepAction,
        TalonString,
        TalonVariable,
        TalonComment,
    ]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonFloat(Leaf):
    pass

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonIdentifier(Leaf):
    pass

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonImplicitString(Leaf):
    pass

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonIncludeTag(Branch):
    children: list[TalonComment]
    tag: TalonIdentifier

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonInteger(Leaf):
    pass

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonInterpolation(Branch):
    children: list[
        typing.Union[
            TalonAction,
            TalonBinaryOperator,
            TalonFloat,
            TalonInteger,
            TalonKeyAction,
            TalonParenthesizedExpression,
            TalonSleepAction,
            TalonString,
            TalonVariable,
            TalonComment,
        ]
    ]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonKeyAction(Branch):
    children: list[TalonComment]
    arguments: TalonImplicitString

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonList(Branch):
    children: list[TalonComment]
    list_name: TalonIdentifier

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonMatch(Branch):
    children: list[TalonComment]
    key: TalonIdentifier
    pattern: TalonImplicitString

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonNot(Branch):
    children: list[typing.Union[TalonMatch, TalonComment]]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonNumber(Branch):
    children: list[typing.Union[TalonFloat, TalonInteger, TalonComment]]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonOperator(Leaf):
    pass

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonOptional(Branch):
    children: list[
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

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonOr(Branch):
    children: list[typing.Union[TalonAnd, TalonMatch, TalonNot, TalonComment]]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonParenthesizedExpression(Branch):
    children: list[
        typing.Union[
            TalonAction,
            TalonBinaryOperator,
            TalonFloat,
            TalonInteger,
            TalonKeyAction,
            TalonParenthesizedExpression,
            TalonSleepAction,
            TalonString,
            TalonVariable,
            TalonComment,
        ]
    ]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonParenthesizedRule(Branch):
    children: list[
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

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonRegexEscapeSequence(Branch):
    children: list[typing.Union[TalonRegexEscapeSequence, TalonComment]]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonRepeat(Branch):
    children: list[
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

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonRepeat1(Branch):
    children: list[
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

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonRule(Branch):
    children: list[
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

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonSeq(Branch):
    children: list[
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

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonSettings(Branch):
    children: list[typing.Union[TalonBlock, TalonComment]]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonSleepAction(Branch):
    children: list[TalonComment]
    arguments: TalonImplicitString

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonSourceFile(Branch):
    children: list[
        typing.Union[
            TalonCommand, TalonContext, TalonIncludeTag, TalonSettings, TalonComment
        ]
    ]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonStartAnchor(Leaf):
    pass

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonString(Branch):
    children: list[
        typing.Union[
            TalonInterpolation,
            TalonStringContent,
            TalonStringEscapeSequence,
            TalonComment,
        ]
    ]

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonStringContent(Leaf):
    pass

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonStringEscapeSequence(Leaf):
    pass

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonVariable(Branch):
    children: list[TalonComment]
    variable_name: TalonIdentifier

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TalonWord(Leaf):
    pass
