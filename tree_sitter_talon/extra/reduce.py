import dataclasses

from ..dynamic import *

__extra_reduce__ = ()


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
