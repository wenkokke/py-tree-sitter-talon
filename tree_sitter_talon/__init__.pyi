from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pathlib import Path
from typing import Optional, Union
from tree_sitter_type_provider import *

import tree_sitter # type: ignore

parser: tree_sitter.Parser

language: tree_sitter.Language


def parse(
    contents: Union[str, bytes],
    has_header: Optional[bool] = None,
    encoding: str = "utf-8",
) -> Node: ...


def parse_file(
    path: Union[str, Path],
    has_header: Optional[bool] = None,
    encoding: str = "utf-8",
) -> Node: ...


def parse_as_tree_sitter(
    contents: Union[str, bytes],
    has_header: Optional[bool] = None,
    encoding: str = "utf-8",
) -> tree_sitter.Tree: ...


def parse_file_as_tree_sitter(
    path: Union[str, Path],
    has_header: Optional[bool] = None,
    encoding: str = "utf-8",
) -> tree_sitter.Tree: ...


def from_tree_sitter(
    tsvalue: Union[tree_sitter.Tree, tree_sitter.Node, tree_sitter.TreeCursor],
    *,
    encoding: str = "utf-8"
) -> Node: ...


@dataclass_json
@dataclass
class TalonAction(Branch):
    children: list[TalonComment]
    action_name: TalonIdentifier
    arguments: TalonArgumentList


@dataclass_json
@dataclass
class TalonAnd(Branch):
    children: list[Union[TalonAnd, TalonMatch, TalonNot, TalonComment]]


@dataclass_json
@dataclass
class TalonArgumentList(Branch):
    children: list[Union[TalonAction, TalonBinaryOperator, TalonFloat, TalonInteger, TalonKeyAction, TalonParenthesizedExpression, TalonSleepAction, TalonString, TalonVariable, TalonComment]]


@dataclass_json
@dataclass
class TalonAssignment(Branch):
    children: list[TalonComment]
    left: TalonIdentifier
    right: Union[TalonAction, TalonBinaryOperator, TalonFloat, TalonInteger, TalonKeyAction, TalonParenthesizedExpression, TalonSleepAction, TalonString, TalonVariable, TalonComment]


@dataclass_json
@dataclass
class TalonBinaryOperator(Branch):
    children: list[TalonComment]
    left: Union[TalonAction, TalonBinaryOperator, TalonFloat, TalonInteger, TalonKeyAction, TalonParenthesizedExpression, TalonSleepAction, TalonString, TalonVariable, TalonComment]
    operator: TalonOperator
    right: Union[TalonAction, TalonBinaryOperator, TalonFloat, TalonInteger, TalonKeyAction, TalonParenthesizedExpression, TalonSleepAction, TalonString, TalonVariable, TalonComment]


@dataclass_json
@dataclass
class TalonBlock(Branch):
    children: list[Union[TalonAssignment, TalonDocstring, TalonExpression, TalonComment]]


@dataclass_json
@dataclass
class TalonCapture(Branch):
    children: list[TalonComment]
    capture_name: TalonIdentifier


@dataclass_json
@dataclass
class TalonChoice(Branch):
    children: list[Union[TalonCapture, TalonEndAnchor, TalonList, TalonOptional, TalonParenthesizedRule, TalonRepeat, TalonRepeat1, TalonSeq, TalonStartAnchor, TalonWord, TalonComment]]


@dataclass_json
@dataclass
class TalonCommand(Branch):
    children: list[TalonComment]
    rule: TalonRule
    script: TalonBlock


@dataclass_json
@dataclass
class TalonComment(Leaf):
    pass


@dataclass_json
@dataclass
class TalonContext(Branch):
    children: list[Union[TalonAnd, TalonDocstring, TalonMatch, TalonNot, TalonOr, TalonComment]]


@dataclass_json
@dataclass
class TalonDocstring(Leaf):
    pass


@dataclass_json
@dataclass
class TalonEndAnchor(Leaf):
    pass


@dataclass_json
@dataclass
class TalonError(Branch):
    children: list[Union[TalonAction, TalonAnd, TalonArgumentList, TalonAssignment, TalonBinaryOperator, TalonBlock, TalonCapture, TalonChoice, TalonCommand, TalonContext, TalonExpression, TalonIncludeTag, TalonInterpolation, TalonKeyAction, TalonList, TalonMatch, TalonNot, TalonNumber, TalonOptional, TalonOr, TalonParenthesizedExpression, TalonParenthesizedRule, TalonRegexEscapeSequence, TalonRepeat, TalonRepeat1, TalonRule, TalonSeq, TalonSettings, TalonSleepAction, TalonSourceFile, TalonString, TalonStringContent, TalonVariable, TalonComment, TalonDocstring, TalonEndAnchor, TalonFloat, TalonIdentifier, TalonImplicitString, TalonInteger, TalonOperator, TalonStartAnchor, TalonStringEscapeSequence, TalonWord, TalonError]]


@dataclass_json
@dataclass
class TalonExpression(Branch):
    children: list[TalonComment]
    expression: Union[TalonAction, TalonBinaryOperator, TalonFloat, TalonInteger, TalonKeyAction, TalonParenthesizedExpression, TalonSleepAction, TalonString, TalonVariable, TalonComment]


@dataclass_json
@dataclass
class TalonFloat(Leaf):
    pass


@dataclass_json
@dataclass
class TalonIdentifier(Leaf):
    pass


@dataclass_json
@dataclass
class TalonImplicitString(Leaf):
    pass


@dataclass_json
@dataclass
class TalonIncludeTag(Branch):
    children: list[TalonComment]
    tag: TalonIdentifier


@dataclass_json
@dataclass
class TalonInteger(Leaf):
    pass


@dataclass_json
@dataclass
class TalonInterpolation(Branch):
    children: list[Union[TalonAction, TalonBinaryOperator, TalonFloat, TalonInteger, TalonKeyAction, TalonParenthesizedExpression, TalonSleepAction, TalonString, TalonVariable, TalonComment]]


@dataclass_json
@dataclass
class TalonKeyAction(Branch):
    children: list[TalonComment]
    arguments: TalonImplicitString


@dataclass_json
@dataclass
class TalonList(Branch):
    children: list[TalonComment]
    list_name: TalonIdentifier


@dataclass_json
@dataclass
class TalonMatch(Branch):
    children: list[TalonComment]
    key: TalonIdentifier
    pattern: TalonImplicitString


@dataclass_json
@dataclass
class TalonNot(Branch):
    children: list[Union[TalonMatch, TalonComment]]


@dataclass_json
@dataclass
class TalonNumber(Branch):
    children: list[Union[TalonFloat, TalonInteger, TalonComment]]


@dataclass_json
@dataclass
class TalonOperator(Leaf):
    pass


@dataclass_json
@dataclass
class TalonOptional(Branch):
    children: list[Union[TalonCapture, TalonChoice, TalonEndAnchor, TalonList, TalonOptional, TalonParenthesizedRule, TalonRepeat, TalonRepeat1, TalonSeq, TalonStartAnchor, TalonWord, TalonComment]]


@dataclass_json
@dataclass
class TalonOr(Branch):
    children: list[Union[TalonAnd, TalonMatch, TalonNot, TalonComment]]


@dataclass_json
@dataclass
class TalonParenthesizedExpression(Branch):
    children: list[Union[TalonAction, TalonBinaryOperator, TalonFloat, TalonInteger, TalonKeyAction, TalonParenthesizedExpression, TalonSleepAction, TalonString, TalonVariable, TalonComment]]


@dataclass_json
@dataclass
class TalonParenthesizedRule(Branch):
    children: list[Union[TalonCapture, TalonChoice, TalonEndAnchor, TalonList, TalonOptional, TalonParenthesizedRule, TalonRepeat, TalonRepeat1, TalonSeq, TalonStartAnchor, TalonWord, TalonComment]]


@dataclass_json
@dataclass
class TalonRegexEscapeSequence(Branch):
    children: list[Union[TalonRegexEscapeSequence, TalonComment]]


@dataclass_json
@dataclass
class TalonRepeat(Branch):
    children: list[Union[TalonCapture, TalonList, TalonOptional, TalonParenthesizedRule, TalonRepeat, TalonRepeat1, TalonWord, TalonComment]]


@dataclass_json
@dataclass
class TalonRepeat1(Branch):
    children: list[Union[TalonCapture, TalonList, TalonOptional, TalonParenthesizedRule, TalonRepeat, TalonRepeat1, TalonWord, TalonComment]]


@dataclass_json
@dataclass
class TalonRule(Branch):
    children: list[Union[TalonCapture, TalonChoice, TalonEndAnchor, TalonList, TalonOptional, TalonParenthesizedRule, TalonRepeat, TalonRepeat1, TalonSeq, TalonStartAnchor, TalonWord, TalonComment]]


@dataclass_json
@dataclass
class TalonSeq(Branch):
    children: list[Union[TalonCapture, TalonList, TalonOptional, TalonParenthesizedRule, TalonRepeat, TalonRepeat1, TalonWord, TalonComment]]


@dataclass_json
@dataclass
class TalonSettings(Branch):
    children: list[Union[TalonBlock, TalonComment]]


@dataclass_json
@dataclass
class TalonSleepAction(Branch):
    children: list[TalonComment]
    arguments: TalonImplicitString


@dataclass_json
@dataclass
class TalonSourceFile(Branch):
    children: list[Union[TalonCommand, TalonContext, TalonIncludeTag, TalonSettings, TalonComment]]


@dataclass_json
@dataclass
class TalonStartAnchor(Leaf):
    pass


@dataclass_json
@dataclass
class TalonString(Branch):
    children: list[Union[TalonInterpolation, TalonStringContent, TalonStringEscapeSequence, TalonComment]]


@dataclass_json
@dataclass
class TalonStringContent(Leaf):
    pass


@dataclass_json
@dataclass
class TalonStringEscapeSequence(Leaf):
    pass


@dataclass_json
@dataclass
class TalonVariable(Branch):
    children: list[TalonComment]
    variable_name: TalonIdentifier


@dataclass_json
@dataclass
class TalonWord(Leaf):
    pass