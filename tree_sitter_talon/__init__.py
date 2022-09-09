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

__version__: str = "1000.2.0.0"

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


def _make_TalonAction(*args, **kwargs) -> TalonAction:
    return TalonAction(*args, **kwargs)


setattr(
    TalonAction,
    "__reduce__",
    lambda self: (_make_TalonAction, dataclasses.astuple(self)),
)


def _make_TalonArgumentList(*args, **kwargs) -> TalonArgumentList:
    return TalonArgumentList(*args, **kwargs)


setattr(
    TalonArgumentList,
    "__reduce__",
    lambda self: (_make_TalonArgumentList, dataclasses.astuple(self)),
)


def _make_TalonAssignmentStatement(*args, **kwargs) -> TalonAssignmentStatement:
    return TalonAssignmentStatement(*args, **kwargs)


setattr(
    TalonAssignmentStatement,
    "__reduce__",
    lambda self: (_make_TalonAssignmentStatement, dataclasses.astuple(self)),
)


def _make_TalonBinaryOperator(*args, **kwargs) -> TalonBinaryOperator:
    return TalonBinaryOperator(*args, **kwargs)


setattr(
    TalonBinaryOperator,
    "__reduce__",
    lambda self: (_make_TalonBinaryOperator, dataclasses.astuple(self)),
)


def _make_TalonBlock(*args, **kwargs) -> TalonBlock:
    return TalonBlock(*args, **kwargs)


setattr(
    TalonBlock,
    "__reduce__",
    lambda self: (_make_TalonBlock, dataclasses.astuple(self)),
)


def _make_TalonCapture(*args, **kwargs) -> TalonCapture:
    return TalonCapture(*args, **kwargs)


setattr(
    TalonCapture,
    "__reduce__",
    lambda self: (_make_TalonCapture, dataclasses.astuple(self)),
)


def _make_TalonChoice(*args, **kwargs) -> TalonChoice:
    return TalonChoice(*args, **kwargs)


setattr(
    TalonChoice,
    "__reduce__",
    lambda self: (_make_TalonChoice, dataclasses.astuple(self)),
)


def _make_TalonCommandDeclaration(*args, **kwargs) -> TalonCommandDeclaration:
    return TalonCommandDeclaration(*args, **kwargs)


setattr(
    TalonCommandDeclaration,
    "__reduce__",
    lambda self: (_make_TalonCommandDeclaration, dataclasses.astuple(self)),
)


def _make_TalonComment(*args, **kwargs) -> TalonComment:
    return TalonComment(*args, **kwargs)


setattr(
    TalonComment,
    "__reduce__",
    lambda self: (_make_TalonComment, dataclasses.astuple(self)),
)


def _make_TalonDeclaration(*args, **kwargs) -> TalonDeclaration:
    return TalonDeclaration(*args, **kwargs)


setattr(
    TalonDeclaration,
    "__reduce__",
    lambda self: (_make_TalonDeclaration, dataclasses.astuple(self)),
)


def _make_TalonEndAnchor(*args, **kwargs) -> TalonEndAnchor:
    return TalonEndAnchor(*args, **kwargs)


setattr(
    TalonEndAnchor,
    "__reduce__",
    lambda self: (_make_TalonEndAnchor, dataclasses.astuple(self)),
)


def _make_TalonError(*args, **kwargs) -> TalonError:
    return TalonError(*args, **kwargs)


setattr(
    TalonError,
    "__reduce__",
    lambda self: (_make_TalonError, dataclasses.astuple(self)),
)


def _make_TalonExpression(*args, **kwargs) -> TalonExpression:
    return TalonExpression(*args, **kwargs)


setattr(
    TalonExpression,
    "__reduce__",
    lambda self: (_make_TalonExpression, dataclasses.astuple(self)),
)


def _make_TalonExpressionStatement(*args, **kwargs) -> TalonExpressionStatement:
    return TalonExpressionStatement(*args, **kwargs)


setattr(
    TalonExpressionStatement,
    "__reduce__",
    lambda self: (_make_TalonExpressionStatement, dataclasses.astuple(self)),
)


def _make_TalonFloat(*args, **kwargs) -> TalonFloat:
    return TalonFloat(*args, **kwargs)


setattr(
    TalonFloat,
    "__reduce__",
    lambda self: (_make_TalonFloat, dataclasses.astuple(self)),
)


def _make_TalonIdentifier(*args, **kwargs) -> TalonIdentifier:
    return TalonIdentifier(*args, **kwargs)


setattr(
    TalonIdentifier,
    "__reduce__",
    lambda self: (_make_TalonIdentifier, dataclasses.astuple(self)),
)


def _make_TalonImplicitString(*args, **kwargs) -> TalonImplicitString:
    return TalonImplicitString(*args, **kwargs)


setattr(
    TalonImplicitString,
    "__reduce__",
    lambda self: (_make_TalonImplicitString, dataclasses.astuple(self)),
)


def _make_TalonInteger(*args, **kwargs) -> TalonInteger:
    return TalonInteger(*args, **kwargs)


setattr(
    TalonInteger,
    "__reduce__",
    lambda self: (_make_TalonInteger, dataclasses.astuple(self)),
)


def _make_TalonInterpolation(*args, **kwargs) -> TalonInterpolation:
    return TalonInterpolation(*args, **kwargs)


setattr(
    TalonInterpolation,
    "__reduce__",
    lambda self: (_make_TalonInterpolation, dataclasses.astuple(self)),
)


def _make_TalonKeyAction(*args, **kwargs) -> TalonKeyAction:
    return TalonKeyAction(*args, **kwargs)


setattr(
    TalonKeyAction,
    "__reduce__",
    lambda self: (_make_TalonKeyAction, dataclasses.astuple(self)),
)


def _make_TalonKeyBindingDeclaration(*args, **kwargs) -> TalonKeyBindingDeclaration:
    return TalonKeyBindingDeclaration(*args, **kwargs)


setattr(
    TalonKeyBindingDeclaration,
    "__reduce__",
    lambda self: (_make_TalonKeyBindingDeclaration, dataclasses.astuple(self)),
)


def _make_TalonList(*args, **kwargs) -> TalonList:
    return TalonList(*args, **kwargs)


setattr(
    TalonList,
    "__reduce__",
    lambda self: (_make_TalonList, dataclasses.astuple(self)),
)


def _make_TalonMatch(*args, **kwargs) -> TalonMatch:
    return TalonMatch(*args, **kwargs)


setattr(
    TalonMatch,
    "__reduce__",
    lambda self: (_make_TalonMatch, dataclasses.astuple(self)),
)


def _make_TalonMatches(*args, **kwargs) -> TalonMatches:
    return TalonMatches(*args, **kwargs)


setattr(
    TalonMatches,
    "__reduce__",
    lambda self: (_make_TalonMatches, dataclasses.astuple(self)),
)


def _make_TalonMatchModifier(*args, **kwargs) -> TalonMatchModifier:
    return TalonMatchModifier(*args, **kwargs)


setattr(
    TalonMatchModifier,
    "__reduce__",
    lambda self: (_make_TalonMatchModifier, dataclasses.astuple(self)),
)


def _make_TalonNumber(*args, **kwargs) -> TalonNumber:
    return TalonNumber(*args, **kwargs)


setattr(
    TalonNumber,
    "__reduce__",
    lambda self: (_make_TalonNumber, dataclasses.astuple(self)),
)


def _make_TalonOperator(*args, **kwargs) -> TalonOperator:
    return TalonOperator(*args, **kwargs)


setattr(
    TalonOperator,
    "__reduce__",
    lambda self: (_make_TalonOperator, dataclasses.astuple(self)),
)


def _make_TalonOptional(*args, **kwargs) -> TalonOptional:
    return TalonOptional(*args, **kwargs)


setattr(
    TalonOptional,
    "__reduce__",
    lambda self: (_make_TalonOptional, dataclasses.astuple(self)),
)


def _make_TalonParenthesizedExpression(*args, **kwargs) -> TalonParenthesizedExpression:
    return TalonParenthesizedExpression(*args, **kwargs)


setattr(
    TalonParenthesizedExpression,
    "__reduce__",
    lambda self: (_make_TalonParenthesizedExpression, dataclasses.astuple(self)),
)


def _make_TalonParenthesizedRule(*args, **kwargs) -> TalonParenthesizedRule:
    return TalonParenthesizedRule(*args, **kwargs)


setattr(
    TalonParenthesizedRule,
    "__reduce__",
    lambda self: (_make_TalonParenthesizedRule, dataclasses.astuple(self)),
)


def _make_TalonRepeat(*args, **kwargs) -> TalonRepeat:
    return TalonRepeat(*args, **kwargs)


setattr(
    TalonRepeat,
    "__reduce__",
    lambda self: (_make_TalonRepeat, dataclasses.astuple(self)),
)


def _make_TalonRepeat1(*args, **kwargs) -> TalonRepeat1:
    return TalonRepeat1(*args, **kwargs)


setattr(
    TalonRepeat1,
    "__reduce__",
    lambda self: (_make_TalonRepeat1, dataclasses.astuple(self)),
)


def _make_TalonRule(*args, **kwargs) -> TalonRule:
    return TalonRule(*args, **kwargs)


setattr(
    TalonRule,
    "__reduce__",
    lambda self: (_make_TalonRule, dataclasses.astuple(self)),
)


def _make_TalonSeq(*args, **kwargs) -> TalonSeq:
    return TalonSeq(*args, **kwargs)


setattr(
    TalonSeq,
    "__reduce__",
    lambda self: (_make_TalonSeq, dataclasses.astuple(self)),
)


def _make_TalonSettingsDeclaration(*args, **kwargs) -> TalonSettingsDeclaration:
    return TalonSettingsDeclaration(*args, **kwargs)


setattr(
    TalonSettingsDeclaration,
    "__reduce__",
    lambda self: (_make_TalonSettingsDeclaration, dataclasses.astuple(self)),
)


def _make_TalonSleepAction(*args, **kwargs) -> TalonSleepAction:
    return TalonSleepAction(*args, **kwargs)


setattr(
    TalonSleepAction,
    "__reduce__",
    lambda self: (_make_TalonSleepAction, dataclasses.astuple(self)),
)


def _make_TalonSourceFile(*args, **kwargs) -> TalonSourceFile:
    return TalonSourceFile(*args, **kwargs)


setattr(
    TalonSourceFile,
    "__reduce__",
    lambda self: (_make_TalonSourceFile, dataclasses.astuple(self)),
)


def _make_TalonStartAnchor(*args, **kwargs) -> TalonStartAnchor:
    return TalonStartAnchor(*args, **kwargs)


setattr(
    TalonStartAnchor,
    "__reduce__",
    lambda self: (_make_TalonStartAnchor, dataclasses.astuple(self)),
)


def _make_TalonStatement(*args, **kwargs) -> TalonStatement:
    return TalonStatement(*args, **kwargs)


setattr(
    TalonStatement,
    "__reduce__",
    lambda self: (_make_TalonStatement, dataclasses.astuple(self)),
)


def _make_TalonString(*args, **kwargs) -> TalonString:
    return TalonString(*args, **kwargs)


setattr(
    TalonString,
    "__reduce__",
    lambda self: (_make_TalonString, dataclasses.astuple(self)),
)


def _make_TalonStringContent(*args, **kwargs) -> TalonStringContent:
    return TalonStringContent(*args, **kwargs)


setattr(
    TalonStringContent,
    "__reduce__",
    lambda self: (_make_TalonStringContent, dataclasses.astuple(self)),
)


def _make_TalonStringEscapeSequence(*args, **kwargs) -> TalonStringEscapeSequence:
    return TalonStringEscapeSequence(*args, **kwargs)


setattr(
    TalonStringEscapeSequence,
    "__reduce__",
    lambda self: (_make_TalonStringEscapeSequence, dataclasses.astuple(self)),
)


def _make_TalonTagImportDeclaration(*args, **kwargs) -> TalonTagImportDeclaration:
    return TalonTagImportDeclaration(*args, **kwargs)


setattr(
    TalonTagImportDeclaration,
    "__reduce__",
    lambda self: (_make_TalonTagImportDeclaration, dataclasses.astuple(self)),
)


def _make_TalonVariable(*args, **kwargs) -> TalonVariable:
    return TalonVariable(*args, **kwargs)


setattr(
    TalonVariable,
    "__reduce__",
    lambda self: (_make_TalonVariable, dataclasses.astuple(self)),
)


def _make_TalonWord(*args, **kwargs) -> TalonWord:
    return TalonWord(*args, **kwargs)


setattr(
    TalonWord,
    "__reduce__",
    lambda self: (_make_TalonWord, dataclasses.astuple(self)),
)
