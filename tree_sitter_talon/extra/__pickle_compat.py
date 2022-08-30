import dataclasses

from .. import dynamic as _dynamic


def _make_TalonAction(*args, **kwargs) -> _dynamic.TalonAction:
    return _dynamic.TalonAction(*args, **kwargs)


setattr(
    _dynamic.TalonAction,
    "__reduce__",
    lambda self: (_make_TalonAction, dataclasses.astuple(self)),
)


def _make_TalonArgumentList(*args, **kwargs) -> _dynamic.TalonArgumentList:
    return _dynamic.TalonArgumentList(*args, **kwargs)


setattr(
    _dynamic.TalonArgumentList,
    "__reduce__",
    lambda self: (_make_TalonArgumentList, dataclasses.astuple(self)),
)


def _make_TalonAssignmentStatement(
    *args, **kwargs
) -> _dynamic.TalonAssignmentStatement:
    return _dynamic.TalonAssignmentStatement(*args, **kwargs)


setattr(
    _dynamic.TalonAssignmentStatement,
    "__reduce__",
    lambda self: (_make_TalonAssignmentStatement, dataclasses.astuple(self)),
)


def _make_TalonBinaryOperator(*args, **kwargs) -> _dynamic.TalonBinaryOperator:
    return _dynamic.TalonBinaryOperator(*args, **kwargs)


setattr(
    _dynamic.TalonBinaryOperator,
    "__reduce__",
    lambda self: (_make_TalonBinaryOperator, dataclasses.astuple(self)),
)


def _make_TalonBlock(*args, **kwargs) -> _dynamic.TalonBlock:
    return _dynamic.TalonBlock(*args, **kwargs)


setattr(
    _dynamic.TalonBlock,
    "__reduce__",
    lambda self: (_make_TalonBlock, dataclasses.astuple(self)),
)


def _make_TalonCapture(*args, **kwargs) -> _dynamic.TalonCapture:
    return _dynamic.TalonCapture(*args, **kwargs)


setattr(
    _dynamic.TalonCapture,
    "__reduce__",
    lambda self: (_make_TalonCapture, dataclasses.astuple(self)),
)


def _make_TalonChoice(*args, **kwargs) -> _dynamic.TalonChoice:
    return _dynamic.TalonChoice(*args, **kwargs)


setattr(
    _dynamic.TalonChoice,
    "__reduce__",
    lambda self: (_make_TalonChoice, dataclasses.astuple(self)),
)


def _make_TalonCommandDeclaration(*args, **kwargs) -> _dynamic.TalonCommandDeclaration:
    return _dynamic.TalonCommandDeclaration(*args, **kwargs)


setattr(
    _dynamic.TalonCommandDeclaration,
    "__reduce__",
    lambda self: (_make_TalonCommandDeclaration, dataclasses.astuple(self)),
)


def _make_TalonComment(*args, **kwargs) -> _dynamic.TalonComment:
    return _dynamic.TalonComment(*args, **kwargs)


setattr(
    _dynamic.TalonComment,
    "__reduce__",
    lambda self: (_make_TalonComment, dataclasses.astuple(self)),
)


def _make_TalonDeclaration(*args, **kwargs) -> _dynamic.TalonDeclaration:
    return _dynamic.TalonDeclaration(*args, **kwargs)


setattr(
    _dynamic.TalonDeclaration,
    "__reduce__",
    lambda self: (_make_TalonDeclaration, dataclasses.astuple(self)),
)


def _make_TalonEndAnchor(*args, **kwargs) -> _dynamic.TalonEndAnchor:
    return _dynamic.TalonEndAnchor(*args, **kwargs)


setattr(
    _dynamic.TalonEndAnchor,
    "__reduce__",
    lambda self: (_make_TalonEndAnchor, dataclasses.astuple(self)),
)


def _make_TalonError(*args, **kwargs) -> _dynamic.TalonError:
    return _dynamic.TalonError(*args, **kwargs)


setattr(
    _dynamic.TalonError,
    "__reduce__",
    lambda self: (_make_TalonError, dataclasses.astuple(self)),
)


def _make_TalonExpression(*args, **kwargs) -> _dynamic.TalonExpression:
    return _dynamic.TalonExpression(*args, **kwargs)


setattr(
    _dynamic.TalonExpression,
    "__reduce__",
    lambda self: (_make_TalonExpression, dataclasses.astuple(self)),
)


def _make_TalonExpressionStatement(
    *args, **kwargs
) -> _dynamic.TalonExpressionStatement:
    return _dynamic.TalonExpressionStatement(*args, **kwargs)


setattr(
    _dynamic.TalonExpressionStatement,
    "__reduce__",
    lambda self: (_make_TalonExpressionStatement, dataclasses.astuple(self)),
)


def _make_TalonFloat(*args, **kwargs) -> _dynamic.TalonFloat:
    return _dynamic.TalonFloat(*args, **kwargs)


setattr(
    _dynamic.TalonFloat,
    "__reduce__",
    lambda self: (_make_TalonFloat, dataclasses.astuple(self)),
)


def _make_TalonIdentifier(*args, **kwargs) -> _dynamic.TalonIdentifier:
    return _dynamic.TalonIdentifier(*args, **kwargs)


setattr(
    _dynamic.TalonIdentifier,
    "__reduce__",
    lambda self: (_make_TalonIdentifier, dataclasses.astuple(self)),
)


def _make_TalonImplicitString(*args, **kwargs) -> _dynamic.TalonImplicitString:
    return _dynamic.TalonImplicitString(*args, **kwargs)


setattr(
    _dynamic.TalonImplicitString,
    "__reduce__",
    lambda self: (_make_TalonImplicitString, dataclasses.astuple(self)),
)


def _make_TalonInteger(*args, **kwargs) -> _dynamic.TalonInteger:
    return _dynamic.TalonInteger(*args, **kwargs)


setattr(
    _dynamic.TalonInteger,
    "__reduce__",
    lambda self: (_make_TalonInteger, dataclasses.astuple(self)),
)


def _make_TalonInterpolation(*args, **kwargs) -> _dynamic.TalonInterpolation:
    return _dynamic.TalonInterpolation(*args, **kwargs)


setattr(
    _dynamic.TalonInterpolation,
    "__reduce__",
    lambda self: (_make_TalonInterpolation, dataclasses.astuple(self)),
)


def _make_TalonKeyAction(*args, **kwargs) -> _dynamic.TalonKeyAction:
    return _dynamic.TalonKeyAction(*args, **kwargs)


setattr(
    _dynamic.TalonKeyAction,
    "__reduce__",
    lambda self: (_make_TalonKeyAction, dataclasses.astuple(self)),
)


def _make_TalonKeyBindingDeclaration(
    *args, **kwargs
) -> _dynamic.TalonKeyBindingDeclaration:
    return _dynamic.TalonKeyBindingDeclaration(*args, **kwargs)


setattr(
    _dynamic.TalonKeyBindingDeclaration,
    "__reduce__",
    lambda self: (_make_TalonKeyBindingDeclaration, dataclasses.astuple(self)),
)


def _make_TalonList(*args, **kwargs) -> _dynamic.TalonList:
    return _dynamic.TalonList(*args, **kwargs)


setattr(
    _dynamic.TalonList,
    "__reduce__",
    lambda self: (_make_TalonList, dataclasses.astuple(self)),
)


def _make_TalonMatch(*args, **kwargs) -> _dynamic.TalonMatch:
    return _dynamic.TalonMatch(*args, **kwargs)


setattr(
    _dynamic.TalonMatch,
    "__reduce__",
    lambda self: (_make_TalonMatch, dataclasses.astuple(self)),
)


def _make_TalonMatches(*args, **kwargs) -> _dynamic.TalonMatches:
    return _dynamic.TalonMatches(*args, **kwargs)


setattr(
    _dynamic.TalonMatches,
    "__reduce__",
    lambda self: (_make_TalonMatches, dataclasses.astuple(self)),
)


def _make_TalonMatchModifier(*args, **kwargs) -> _dynamic.TalonMatchModifier:
    return _dynamic.TalonMatchModifier(*args, **kwargs)


setattr(
    _dynamic.TalonMatchModifier,
    "__reduce__",
    lambda self: (_make_TalonMatchModifier, dataclasses.astuple(self)),
)


def _make_TalonNumber(*args, **kwargs) -> _dynamic.TalonNumber:
    return _dynamic.TalonNumber(*args, **kwargs)


setattr(
    _dynamic.TalonNumber,
    "__reduce__",
    lambda self: (_make_TalonNumber, dataclasses.astuple(self)),
)


def _make_TalonOperator(*args, **kwargs) -> _dynamic.TalonOperator:
    return _dynamic.TalonOperator(*args, **kwargs)


setattr(
    _dynamic.TalonOperator,
    "__reduce__",
    lambda self: (_make_TalonOperator, dataclasses.astuple(self)),
)


def _make_TalonOptional(*args, **kwargs) -> _dynamic.TalonOptional:
    return _dynamic.TalonOptional(*args, **kwargs)


setattr(
    _dynamic.TalonOptional,
    "__reduce__",
    lambda self: (_make_TalonOptional, dataclasses.astuple(self)),
)


def _make_TalonParenthesizedExpression(
    *args, **kwargs
) -> _dynamic.TalonParenthesizedExpression:
    return _dynamic.TalonParenthesizedExpression(*args, **kwargs)


setattr(
    _dynamic.TalonParenthesizedExpression,
    "__reduce__",
    lambda self: (_make_TalonParenthesizedExpression, dataclasses.astuple(self)),
)


def _make_TalonParenthesizedRule(*args, **kwargs) -> _dynamic.TalonParenthesizedRule:
    return _dynamic.TalonParenthesizedRule(*args, **kwargs)


setattr(
    _dynamic.TalonParenthesizedRule,
    "__reduce__",
    lambda self: (_make_TalonParenthesizedRule, dataclasses.astuple(self)),
)


def _make_TalonRepeat(*args, **kwargs) -> _dynamic.TalonRepeat:
    return _dynamic.TalonRepeat(*args, **kwargs)


setattr(
    _dynamic.TalonRepeat,
    "__reduce__",
    lambda self: (_make_TalonRepeat, dataclasses.astuple(self)),
)


def _make_TalonRepeat1(*args, **kwargs) -> _dynamic.TalonRepeat1:
    return _dynamic.TalonRepeat1(*args, **kwargs)


setattr(
    _dynamic.TalonRepeat1,
    "__reduce__",
    lambda self: (_make_TalonRepeat1, dataclasses.astuple(self)),
)


def _make_TalonRule(*args, **kwargs) -> _dynamic.TalonRule:
    return _dynamic.TalonRule(*args, **kwargs)


setattr(
    _dynamic.TalonRule,
    "__reduce__",
    lambda self: (_make_TalonRule, dataclasses.astuple(self)),
)


def _make_TalonSeq(*args, **kwargs) -> _dynamic.TalonSeq:
    return _dynamic.TalonSeq(*args, **kwargs)


setattr(
    _dynamic.TalonSeq,
    "__reduce__",
    lambda self: (_make_TalonSeq, dataclasses.astuple(self)),
)


def _make_TalonSettingsDeclaration(
    *args, **kwargs
) -> _dynamic.TalonSettingsDeclaration:
    return _dynamic.TalonSettingsDeclaration(*args, **kwargs)


setattr(
    _dynamic.TalonSettingsDeclaration,
    "__reduce__",
    lambda self: (_make_TalonSettingsDeclaration, dataclasses.astuple(self)),
)


def _make_TalonSleepAction(*args, **kwargs) -> _dynamic.TalonSleepAction:
    return _dynamic.TalonSleepAction(*args, **kwargs)


setattr(
    _dynamic.TalonSleepAction,
    "__reduce__",
    lambda self: (_make_TalonSleepAction, dataclasses.astuple(self)),
)


def _make_TalonSourceFile(*args, **kwargs) -> _dynamic.TalonSourceFile:
    return _dynamic.TalonSourceFile(*args, **kwargs)


setattr(
    _dynamic.TalonSourceFile,
    "__reduce__",
    lambda self: (_make_TalonSourceFile, dataclasses.astuple(self)),
)


def _make_TalonStartAnchor(*args, **kwargs) -> _dynamic.TalonStartAnchor:
    return _dynamic.TalonStartAnchor(*args, **kwargs)


setattr(
    _dynamic.TalonStartAnchor,
    "__reduce__",
    lambda self: (_make_TalonStartAnchor, dataclasses.astuple(self)),
)


def _make_TalonStatement(*args, **kwargs) -> _dynamic.TalonStatement:
    return _dynamic.TalonStatement(*args, **kwargs)


setattr(
    _dynamic.TalonStatement,
    "__reduce__",
    lambda self: (_make_TalonStatement, dataclasses.astuple(self)),
)


def _make_TalonString(*args, **kwargs) -> _dynamic.TalonString:
    return _dynamic.TalonString(*args, **kwargs)


setattr(
    _dynamic.TalonString,
    "__reduce__",
    lambda self: (_make_TalonString, dataclasses.astuple(self)),
)


def _make_TalonStringContent(*args, **kwargs) -> _dynamic.TalonStringContent:
    return _dynamic.TalonStringContent(*args, **kwargs)


setattr(
    _dynamic.TalonStringContent,
    "__reduce__",
    lambda self: (_make_TalonStringContent, dataclasses.astuple(self)),
)


def _make_TalonStringEscapeSequence(
    *args, **kwargs
) -> _dynamic.TalonStringEscapeSequence:
    return _dynamic.TalonStringEscapeSequence(*args, **kwargs)


setattr(
    _dynamic.TalonStringEscapeSequence,
    "__reduce__",
    lambda self: (_make_TalonStringEscapeSequence, dataclasses.astuple(self)),
)


def _make_TalonTagImportDeclaration(
    *args, **kwargs
) -> _dynamic.TalonTagImportDeclaration:
    return _dynamic.TalonTagImportDeclaration(*args, **kwargs)


setattr(
    _dynamic.TalonTagImportDeclaration,
    "__reduce__",
    lambda self: (_make_TalonTagImportDeclaration, dataclasses.astuple(self)),
)


def _make_TalonVariable(*args, **kwargs) -> _dynamic.TalonVariable:
    return _dynamic.TalonVariable(*args, **kwargs)


setattr(
    _dynamic.TalonVariable,
    "__reduce__",
    lambda self: (_make_TalonVariable, dataclasses.astuple(self)),
)


def _make_TalonWord(*args, **kwargs) -> _dynamic.TalonWord:
    return _dynamic.TalonWord(*args, **kwargs)


setattr(
    _dynamic.TalonWord,
    "__reduce__",
    lambda self: (_make_TalonWord, dataclasses.astuple(self)),
)
