import dataclasses
import re
import typing

from .internal.dynamic import Branch as Branch
from .internal.dynamic import Leaf as Leaf
from .internal.dynamic import Node as Node
from .internal.dynamic import NodeTypeError as NodeTypeError
from .internal.dynamic import NodeTypeName as NodeTypeName
from .internal.dynamic import ParseError as ParseError
from .internal.dynamic import Point as Point
from .internal.dynamic import TalonAction as TalonAction
from .internal.dynamic import TalonArgumentList as TalonArgumentList
from .internal.dynamic import TalonAssignmentStatement as TalonAssignmentStatement
from .internal.dynamic import TalonBinaryOperator as TalonBinaryOperator
from .internal.dynamic import TalonBlock as TalonBlock
from .internal.dynamic import TalonCapture as TalonCapture
from .internal.dynamic import TalonChoice as TalonChoice
from .internal.dynamic import TalonCommandDeclaration as TalonCommandDeclaration
from .internal.dynamic import TalonComment as TalonComment
from .internal.dynamic import TalonDeclaration as TalonDeclaration
from .internal.dynamic import TalonEndAnchor as TalonEndAnchor
from .internal.dynamic import TalonError as TalonError
from .internal.dynamic import TalonExpression as TalonExpression
from .internal.dynamic import TalonExpressionStatement as TalonExpressionStatement
from .internal.dynamic import TalonFloat as TalonFloat
from .internal.dynamic import TalonIdentifier as TalonIdentifier
from .internal.dynamic import TalonImplicitString as TalonImplicitString
from .internal.dynamic import TalonInteger as TalonInteger
from .internal.dynamic import TalonInterpolation as TalonInterpolation
from .internal.dynamic import TalonKeyAction as TalonKeyAction
from .internal.dynamic import TalonKeyBindingDeclaration as TalonKeyBindingDeclaration
from .internal.dynamic import TalonList as TalonList
from .internal.dynamic import TalonMatch as TalonMatch
from .internal.dynamic import TalonMatches as TalonMatches
from .internal.dynamic import TalonMatchModifier as TalonMatchModifier
from .internal.dynamic import TalonNumber as TalonNumber
from .internal.dynamic import TalonOperator as TalonOperator
from .internal.dynamic import TalonOptional as TalonOptional
from .internal.dynamic import (
    TalonParenthesizedExpression as TalonParenthesizedExpression,
)
from .internal.dynamic import TalonParenthesizedRule as TalonParenthesizedRule
from .internal.dynamic import TalonRepeat as TalonRepeat
from .internal.dynamic import TalonRepeat1 as TalonRepeat1
from .internal.dynamic import TalonRule as TalonRule
from .internal.dynamic import TalonSeq as TalonSeq
from .internal.dynamic import TalonSettingsDeclaration as TalonSettingsDeclaration
from .internal.dynamic import TalonSleepAction as TalonSleepAction
from .internal.dynamic import TalonSourceFile as TalonSourceFile
from .internal.dynamic import TalonStartAnchor as TalonStartAnchor
from .internal.dynamic import TalonStatement as TalonStatement
from .internal.dynamic import TalonString as TalonString
from .internal.dynamic import TalonStringContent as TalonStringContent
from .internal.dynamic import TalonStringEscapeSequence as TalonStringEscapeSequence
from .internal.dynamic import TalonTagImportDeclaration as TalonTagImportDeclaration
from .internal.dynamic import TalonVariable as TalonVariable
from .internal.dynamic import TalonWord as TalonWord
from .internal.dynamic import from_tree_sitter as from_tree_sitter
from .internal.dynamic import language as language
from .internal.dynamic import parse as parse
from .internal.dynamic import parse_file as parse_file
from .internal.dynamic import parser as parser

################################################################################
# Compile TalonRule to re.Pattern
################################################################################

__version__: str = "1001.2.0.0"

################################################################################
# Compile TalonRule to re.Pattern
################################################################################


def _to_pattern(
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
    lists: typing.Optional[typing.Callable[[str], typing.Optional[list[str]]]] = None,
) -> re.Pattern[str]:
    captures = captures or (lambda capture_name: None)
    lists = lists or (lambda list_name: None)
    return re.compile(_to_pattern_str(self, captures=captures, lists=lists))


def _get_only_child(
    children: typing.Sequence[
        typing.Union[
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
            ],
            TalonComment,
        ]
    ]
) -> typing.Union[
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
]:
    for i, child in enumerate(children):
        if not isinstance(child, TalonComment):
            assert all(isinstance(child, TalonComment) for child in children[i + 1 :])
            return child
    raise ValueError(children)


def _to_pattern_str(
    rule: typing.Union[
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
    ],
    *,
    captures: typing.Callable[
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
    ],
    lists: typing.Callable[[str], typing.Optional[list[str]]],
) -> str:
    if isinstance(rule, TalonCapture):
        capture_name = rule.capture_name.text.strip()
        capture_rule = captures(capture_name)
        if capture_rule:
            return _to_pattern_str(capture_rule, captures=captures, lists=lists)
        else:
            return re.escape(rf"<{capture_name}>")
    elif isinstance(rule, TalonChoice):
        pattern_str = r"|".join(
            [
                _to_pattern_str(child, captures=captures, lists=lists)
                for child in rule.children
                if not isinstance(child, TalonComment)
            ]
        )
        return rf"({pattern_str})"
    elif isinstance(rule, TalonEndAnchor):
        return r"$"
    elif isinstance(rule, TalonList):
        list_name = rule.list_name.text.strip()
        list_items = lists(list_name)
        if list_items:
            list_item_pattern = r"|".join(list_items)
            return rf"({list_item_pattern})"
        else:
            return re.escape(rf"<{list_name}>")
    elif isinstance(rule, TalonOptional):
        child = _get_only_child(rule.children)
        pattern_str = _to_pattern_str(child, captures=captures, lists=lists)
        return rf"({pattern_str})?"
    elif isinstance(rule, TalonParenthesizedRule):
        child = _get_only_child(rule.children)
        pattern_str = _to_pattern_str(child, captures=captures, lists=lists)
        return rf"({pattern_str})"
    elif isinstance(rule, TalonRepeat):
        child = _get_only_child(rule.children)
        pattern_str = _to_pattern_str(child, captures=captures, lists=lists)
        return rf"({pattern_str})*"
    elif isinstance(rule, TalonRepeat1):
        child = _get_only_child(rule.children)
        pattern_str = _to_pattern_str(child, captures=captures, lists=lists)
        return rf"({pattern_str})+"
    elif isinstance(rule, TalonRule):
        return r"\s+".join(
            [
                _to_pattern_str(child, captures=captures, lists=lists)
                for child in rule.children
                if not isinstance(child, TalonComment)
            ]
        )
    elif isinstance(rule, TalonSeq):
        return r"\s+".join(
            [
                _to_pattern_str(child, captures=captures, lists=lists)
                for child in rule.children
                if not isinstance(child, TalonComment)
            ]
        )
    elif isinstance(rule, TalonStartAnchor):
        return r"^"
    elif isinstance(rule, TalonWord):
        return re.escape(rule.text.strip())
    else:
        raise TypeError(type(rule))


setattr(TalonCapture, "to_pattern", _to_pattern)
setattr(TalonChoice, "to_pattern", _to_pattern)
setattr(TalonEndAnchor, "to_pattern", _to_pattern)
setattr(TalonList, "to_pattern", _to_pattern)
setattr(TalonOptional, "to_pattern", _to_pattern)
setattr(TalonParenthesizedRule, "to_pattern", _to_pattern)
setattr(TalonRepeat, "to_pattern", _to_pattern)
setattr(TalonRepeat1, "to_pattern", _to_pattern)
setattr(TalonRule, "to_pattern", _to_pattern)
setattr(TalonSeq, "to_pattern", _to_pattern)
setattr(TalonStartAnchor, "to_pattern", _to_pattern)
setattr(TalonWord, "to_pattern", _to_pattern)


################################################################################
# Pickle Compatibility
################################################################################


def _fields(obj) -> tuple[typing.Any, ...]:
    assert dataclasses.is_dataclass(obj)
    return tuple(getattr(obj, field.name) for field in dataclasses.fields(obj))


def _make_TalonAction(*args) -> TalonAction:
    return TalonAction(*args)


setattr(
    TalonAction,
    "__reduce__",
    lambda self: (_make_TalonAction, _fields(self)),
)


def _make_TalonArgumentList(*args) -> TalonArgumentList:
    return TalonArgumentList(*args)


setattr(
    TalonArgumentList,
    "__reduce__",
    lambda self: (_make_TalonArgumentList, _fields(self)),
)


def _make_TalonAssignmentStatement(*args) -> TalonAssignmentStatement:
    return TalonAssignmentStatement(*args)


setattr(
    TalonAssignmentStatement,
    "__reduce__",
    lambda self: (_make_TalonAssignmentStatement, _fields(self)),
)


def _make_TalonBinaryOperator(*args) -> TalonBinaryOperator:
    return TalonBinaryOperator(*args)


setattr(
    TalonBinaryOperator,
    "__reduce__",
    lambda self: (_make_TalonBinaryOperator, _fields(self)),
)


def _make_TalonBlock(*args) -> TalonBlock:
    return TalonBlock(*args)


setattr(
    TalonBlock,
    "__reduce__",
    lambda self: (_make_TalonBlock, _fields(self)),
)


def _make_TalonCapture(*args) -> TalonCapture:
    return TalonCapture(*args)


setattr(
    TalonCapture,
    "__reduce__",
    lambda self: (_make_TalonCapture, _fields(self)),
)


def _make_TalonChoice(*args) -> TalonChoice:
    return TalonChoice(*args)


setattr(
    TalonChoice,
    "__reduce__",
    lambda self: (_make_TalonChoice, _fields(self)),
)


def _make_TalonCommandDeclaration(*args) -> TalonCommandDeclaration:
    return TalonCommandDeclaration(*args)


setattr(
    TalonCommandDeclaration,
    "__reduce__",
    lambda self: (_make_TalonCommandDeclaration, _fields(self)),
)


def _make_TalonComment(*args) -> TalonComment:
    return TalonComment(*args)


setattr(
    TalonComment,
    "__reduce__",
    lambda self: (_make_TalonComment, _fields(self)),
)


def _make_TalonDeclaration(*args) -> TalonDeclaration:
    return TalonDeclaration(*args)


setattr(
    TalonDeclaration,
    "__reduce__",
    lambda self: (_make_TalonDeclaration, _fields(self)),
)


def _make_TalonEndAnchor(*args) -> TalonEndAnchor:
    return TalonEndAnchor(*args)


setattr(
    TalonEndAnchor,
    "__reduce__",
    lambda self: (_make_TalonEndAnchor, _fields(self)),
)


def _make_TalonError(*args) -> TalonError:
    return TalonError(*args)


setattr(
    TalonError,
    "__reduce__",
    lambda self: (_make_TalonError, _fields(self)),
)


def _make_TalonExpression(*args) -> TalonExpression:
    return TalonExpression(*args)


setattr(
    TalonExpression,
    "__reduce__",
    lambda self: (_make_TalonExpression, _fields(self)),
)


def _make_TalonExpressionStatement(*args) -> TalonExpressionStatement:
    return TalonExpressionStatement(*args)


setattr(
    TalonExpressionStatement,
    "__reduce__",
    lambda self: (_make_TalonExpressionStatement, _fields(self)),
)


def _make_TalonFloat(*args) -> TalonFloat:
    return TalonFloat(*args)


setattr(
    TalonFloat,
    "__reduce__",
    lambda self: (_make_TalonFloat, _fields(self)),
)


def _make_TalonIdentifier(*args) -> TalonIdentifier:
    return TalonIdentifier(*args)


setattr(
    TalonIdentifier,
    "__reduce__",
    lambda self: (_make_TalonIdentifier, _fields(self)),
)


def _make_TalonImplicitString(*args) -> TalonImplicitString:
    return TalonImplicitString(*args)


setattr(
    TalonImplicitString,
    "__reduce__",
    lambda self: (_make_TalonImplicitString, _fields(self)),
)


def _make_TalonInteger(*args) -> TalonInteger:
    return TalonInteger(*args)


setattr(
    TalonInteger,
    "__reduce__",
    lambda self: (_make_TalonInteger, _fields(self)),
)


def _make_TalonInterpolation(*args) -> TalonInterpolation:
    return TalonInterpolation(*args)


setattr(
    TalonInterpolation,
    "__reduce__",
    lambda self: (_make_TalonInterpolation, _fields(self)),
)


def _make_TalonKeyAction(*args) -> TalonKeyAction:
    return TalonKeyAction(*args)


setattr(
    TalonKeyAction,
    "__reduce__",
    lambda self: (_make_TalonKeyAction, _fields(self)),
)


def _make_TalonKeyBindingDeclaration(*args) -> TalonKeyBindingDeclaration:
    return TalonKeyBindingDeclaration(*args)


setattr(
    TalonKeyBindingDeclaration,
    "__reduce__",
    lambda self: (_make_TalonKeyBindingDeclaration, _fields(self)),
)


def _make_TalonList(*args) -> TalonList:
    return TalonList(*args)


setattr(
    TalonList,
    "__reduce__",
    lambda self: (_make_TalonList, _fields(self)),
)


def _make_TalonMatch(*args) -> TalonMatch:
    return TalonMatch(*args)


setattr(
    TalonMatch,
    "__reduce__",
    lambda self: (_make_TalonMatch, _fields(self)),
)


def _make_TalonMatches(*args) -> TalonMatches:
    return TalonMatches(*args)


setattr(
    TalonMatches,
    "__reduce__",
    lambda self: (_make_TalonMatches, _fields(self)),
)


def _make_TalonMatchModifier(*args) -> TalonMatchModifier:
    return TalonMatchModifier(*args)


setattr(
    TalonMatchModifier,
    "__reduce__",
    lambda self: (_make_TalonMatchModifier, _fields(self)),
)


def _make_TalonNumber(*args) -> TalonNumber:
    return TalonNumber(*args)


setattr(
    TalonNumber,
    "__reduce__",
    lambda self: (_make_TalonNumber, _fields(self)),
)


def _make_TalonOperator(*args) -> TalonOperator:
    return TalonOperator(*args)


setattr(
    TalonOperator,
    "__reduce__",
    lambda self: (_make_TalonOperator, _fields(self)),
)


def _make_TalonOptional(*args) -> TalonOptional:
    return TalonOptional(*args)


setattr(
    TalonOptional,
    "__reduce__",
    lambda self: (_make_TalonOptional, _fields(self)),
)


def _make_TalonParenthesizedExpression(*args) -> TalonParenthesizedExpression:
    return TalonParenthesizedExpression(*args)


setattr(
    TalonParenthesizedExpression,
    "__reduce__",
    lambda self: (_make_TalonParenthesizedExpression, _fields(self)),
)


def _make_TalonParenthesizedRule(*args) -> TalonParenthesizedRule:
    return TalonParenthesizedRule(*args)


setattr(
    TalonParenthesizedRule,
    "__reduce__",
    lambda self: (_make_TalonParenthesizedRule, _fields(self)),
)


def _make_TalonRepeat(*args) -> TalonRepeat:
    return TalonRepeat(*args)


setattr(
    TalonRepeat,
    "__reduce__",
    lambda self: (_make_TalonRepeat, _fields(self)),
)


def _make_TalonRepeat1(*args) -> TalonRepeat1:
    return TalonRepeat1(*args)


setattr(
    TalonRepeat1,
    "__reduce__",
    lambda self: (_make_TalonRepeat1, _fields(self)),
)


def _make_TalonRule(*args) -> TalonRule:
    return TalonRule(*args)


setattr(
    TalonRule,
    "__reduce__",
    lambda self: (_make_TalonRule, _fields(self)),
)


def _make_TalonSeq(*args) -> TalonSeq:
    return TalonSeq(*args)


setattr(
    TalonSeq,
    "__reduce__",
    lambda self: (_make_TalonSeq, _fields(self)),
)


def _make_TalonSettingsDeclaration(*args) -> TalonSettingsDeclaration:
    return TalonSettingsDeclaration(*args)


setattr(
    TalonSettingsDeclaration,
    "__reduce__",
    lambda self: (_make_TalonSettingsDeclaration, _fields(self)),
)


def _make_TalonSleepAction(*args) -> TalonSleepAction:
    return TalonSleepAction(*args)


setattr(
    TalonSleepAction,
    "__reduce__",
    lambda self: (_make_TalonSleepAction, _fields(self)),
)


def _make_TalonSourceFile(*args) -> TalonSourceFile:
    return TalonSourceFile(*args)


setattr(
    TalonSourceFile,
    "__reduce__",
    lambda self: (_make_TalonSourceFile, _fields(self)),
)


def _make_TalonStartAnchor(*args) -> TalonStartAnchor:
    return TalonStartAnchor(*args)


setattr(
    TalonStartAnchor,
    "__reduce__",
    lambda self: (_make_TalonStartAnchor, _fields(self)),
)


def _make_TalonStatement(*args) -> TalonStatement:
    return TalonStatement(*args)


setattr(
    TalonStatement,
    "__reduce__",
    lambda self: (_make_TalonStatement, _fields(self)),
)


def _make_TalonString(*args) -> TalonString:
    return TalonString(*args)


setattr(
    TalonString,
    "__reduce__",
    lambda self: (_make_TalonString, _fields(self)),
)


def _make_TalonStringContent(*args) -> TalonStringContent:
    return TalonStringContent(*args)


setattr(
    TalonStringContent,
    "__reduce__",
    lambda self: (_make_TalonStringContent, _fields(self)),
)


def _make_TalonStringEscapeSequence(*args) -> TalonStringEscapeSequence:
    return TalonStringEscapeSequence(*args)


setattr(
    TalonStringEscapeSequence,
    "__reduce__",
    lambda self: (_make_TalonStringEscapeSequence, _fields(self)),
)


def _make_TalonTagImportDeclaration(*args) -> TalonTagImportDeclaration:
    return TalonTagImportDeclaration(*args)


setattr(
    TalonTagImportDeclaration,
    "__reduce__",
    lambda self: (_make_TalonTagImportDeclaration, _fields(self)),
)


def _make_TalonVariable(*args) -> TalonVariable:
    return TalonVariable(*args)


setattr(
    TalonVariable,
    "__reduce__",
    lambda self: (_make_TalonVariable, _fields(self)),
)


def _make_TalonWord(*args) -> TalonWord:
    return TalonWord(*args)


setattr(
    TalonWord,
    "__reduce__",
    lambda self: (_make_TalonWord, _fields(self)),
)
