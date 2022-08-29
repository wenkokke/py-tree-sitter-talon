import dataclasses

from .dynamic import Branch as Branch
from .dynamic import Leaf as Leaf
from .dynamic import Node as Node
from .dynamic import NodeTypeError as NodeTypeError
from .dynamic import NodeTypeName as NodeTypeName
from .dynamic import ParseError as ParseError
from .dynamic import Point as Point
from .dynamic import TalonAction as TalonAction
from .dynamic import TalonArgumentList as TalonArgumentList
from .dynamic import TalonAssignmentStatement as TalonAssignmentStatement
from .dynamic import TalonBinaryOperator as TalonBinaryOperator
from .dynamic import TalonBlock as TalonBlock
from .dynamic import TalonCapture as TalonCapture
from .dynamic import TalonChoice as TalonChoice
from .dynamic import TalonCommandDeclaration as TalonCommandDeclaration
from .dynamic import TalonComment as TalonComment
from .dynamic import TalonDeclaration as TalonDeclaration
from .dynamic import TalonEndAnchor as TalonEndAnchor
from .dynamic import TalonError as TalonError
from .dynamic import TalonExpression as TalonExpression
from .dynamic import TalonExpressionStatement as TalonExpressionStatement
from .dynamic import TalonFloat as TalonFloat
from .dynamic import TalonIdentifier as TalonIdentifier
from .dynamic import TalonImplicitString as TalonImplicitString
from .dynamic import TalonInteger as TalonInteger
from .dynamic import TalonInterpolation as TalonInterpolation
from .dynamic import TalonKeyAction as TalonKeyAction
from .dynamic import TalonKeyBindingDeclaration as TalonKeyBindingDeclaration
from .dynamic import TalonList as TalonList
from .dynamic import TalonMatch as TalonMatch
from .dynamic import TalonMatches as TalonMatches
from .dynamic import TalonMatchModifier as TalonMatchModifier
from .dynamic import TalonNumber as TalonNumber
from .dynamic import TalonOperator as TalonOperator
from .dynamic import TalonOptional as TalonOptional
from .dynamic import TalonParenthesizedExpression as TalonParenthesizedExpression
from .dynamic import TalonParenthesizedRule as TalonParenthesizedRule
from .dynamic import TalonRepeat as TalonRepeat
from .dynamic import TalonRepeat1 as TalonRepeat1
from .dynamic import TalonRule as TalonRule
from .dynamic import TalonSeq as TalonSeq
from .dynamic import TalonSettingsDeclaration as TalonSettingsDeclaration
from .dynamic import TalonSleepAction as TalonSleepAction
from .dynamic import TalonSourceFile as TalonSourceFile
from .dynamic import TalonStartAnchor as TalonStartAnchor
from .dynamic import TalonStatement as TalonStatement
from .dynamic import TalonString as TalonString
from .dynamic import TalonStringContent as TalonStringContent
from .dynamic import TalonStringEscapeSequence as TalonStringEscapeSequence
from .dynamic import TalonTagImportDeclaration as TalonTagImportDeclaration
from .dynamic import TalonVariable as TalonVariable
from .dynamic import TalonWord as TalonWord
from .dynamic import __grammar_version__ as __grammar_version__
from .dynamic import __version__ as __version__
from .dynamic import from_tree_sitter as from_tree_sitter
from .dynamic import language as language
from .dynamic import parse as parse
from .dynamic import parse_file as parse_file
from .dynamic import parser as parser

# Implement __reduce__

setattr(
    TalonAction,
    "__reduce__",
    lambda self: (TalonAction, dataclasses.astuple(self)),
)
setattr(
    TalonArgumentList,
    "__reduce__",
    lambda self: (TalonArgumentList, dataclasses.astuple(self)),
)
setattr(
    TalonAssignmentStatement,
    "__reduce__",
    lambda self: (TalonAssignmentStatement, dataclasses.astuple(self)),
)
setattr(
    TalonBinaryOperator,
    "__reduce__",
    lambda self: (TalonBinaryOperator, dataclasses.astuple(self)),
)
setattr(
    TalonBlock,
    "__reduce__",
    lambda self: (TalonBlock, dataclasses.astuple(self)),
)
setattr(
    TalonCapture,
    "__reduce__",
    lambda self: (TalonCapture, dataclasses.astuple(self)),
)
setattr(
    TalonChoice,
    "__reduce__",
    lambda self: (TalonChoice, dataclasses.astuple(self)),
)
setattr(
    TalonCommandDeclaration,
    "__reduce__",
    lambda self: (TalonCommandDeclaration, dataclasses.astuple(self)),
)
setattr(
    TalonComment,
    "__reduce__",
    lambda self: (TalonComment, dataclasses.astuple(self)),
)
setattr(
    TalonDeclaration,
    "__reduce__",
    lambda self: (TalonDeclaration, dataclasses.astuple(self)),
)
setattr(
    TalonEndAnchor,
    "__reduce__",
    lambda self: (TalonEndAnchor, dataclasses.astuple(self)),
)
setattr(
    TalonError,
    "__reduce__",
    lambda self: (TalonError, dataclasses.astuple(self)),
)
setattr(
    TalonExpression,
    "__reduce__",
    lambda self: (TalonExpression, dataclasses.astuple(self)),
)
setattr(
    TalonExpressionStatement,
    "__reduce__",
    lambda self: (TalonExpressionStatement, dataclasses.astuple(self)),
)
setattr(
    TalonFloat,
    "__reduce__",
    lambda self: (TalonFloat, dataclasses.astuple(self)),
)
setattr(
    TalonIdentifier,
    "__reduce__",
    lambda self: (TalonIdentifier, dataclasses.astuple(self)),
)
setattr(
    TalonImplicitString,
    "__reduce__",
    lambda self: (TalonImplicitString, dataclasses.astuple(self)),
)
setattr(
    TalonInteger,
    "__reduce__",
    lambda self: (
        TalonInteger,
        dataclasses.astuple(self),
    ),
)
setattr(
    TalonInterpolation,
    "__reduce__",
    lambda self: (TalonInterpolation, dataclasses.astuple(self)),
)
setattr(
    TalonKeyAction,
    "__reduce__",
    lambda self: (TalonKeyAction, dataclasses.astuple(self)),
)
setattr(
    TalonKeyBindingDeclaration,
    "__reduce__",
    lambda self: (TalonKeyBindingDeclaration, dataclasses.astuple(self)),
)
setattr(
    TalonList,
    "__reduce__",
    lambda self: (TalonList, dataclasses.astuple(self)),
)
setattr(
    TalonMatch,
    "__reduce__",
    lambda self: (TalonMatch, dataclasses.astuple(self)),
)
setattr(
    TalonMatches, "__reduce__", lambda self: (TalonMatches, dataclasses.astuple(self))
)
setattr(
    TalonMatchModifier,
    "__reduce__",
    lambda self: (TalonMatchModifier, dataclasses.astuple(self)),
)
setattr(
    TalonNumber,
    "__reduce__",
    lambda self: (TalonNumber, dataclasses.astuple(self)),
)
setattr(
    TalonOperator,
    "__reduce__",
    lambda self: (TalonOperator, dataclasses.astuple(self)),
)
setattr(
    TalonOptional,
    "__reduce__",
    lambda self: (TalonOptional, dataclasses.astuple(self)),
)
setattr(
    TalonParenthesizedExpression,
    "__reduce__",
    lambda self: (TalonParenthesizedExpression, dataclasses.astuple(self)),
)
setattr(
    TalonParenthesizedRule,
    "__reduce__",
    lambda self: (TalonParenthesizedRule, dataclasses.astuple(self)),
)
setattr(
    TalonRepeat,
    "__reduce__",
    lambda self: (TalonRepeat, dataclasses.astuple(self)),
)
setattr(
    TalonRepeat1,
    "__reduce__",
    lambda self: (TalonRepeat1, dataclasses.astuple(self)),
)
setattr(
    TalonRule,
    "__reduce__",
    lambda self: (TalonRule, dataclasses.astuple(self)),
)
setattr(
    TalonSeq,
    "__reduce__",
    lambda self: (TalonSeq, dataclasses.astuple(self)),
)
setattr(
    TalonSettingsDeclaration,
    "__reduce__",
    lambda self: (TalonSettingsDeclaration, dataclasses.astuple(self)),
)
setattr(
    TalonSleepAction,
    "__reduce__",
    lambda self: (TalonSleepAction, dataclasses.astuple(self)),
)
setattr(
    TalonSourceFile,
    "__reduce__",
    lambda self: (TalonSourceFile, dataclasses.astuple(self)),
)
setattr(
    TalonStartAnchor,
    "__reduce__",
    lambda self: (TalonStartAnchor, dataclasses.astuple(self)),
)
setattr(
    TalonStatement,
    "__reduce__",
    lambda self: (TalonStatement, dataclasses.astuple(self)),
)
setattr(
    TalonString,
    "__reduce__",
    lambda self: (TalonString, dataclasses.astuple(self)),
)
setattr(
    TalonStringContent,
    "__reduce__",
    lambda self: (TalonStringContent, dataclasses.astuple(self)),
)
setattr(
    TalonStringEscapeSequence,
    "__reduce__",
    lambda self: (TalonStringEscapeSequence, dataclasses.astuple(self)),
)
setattr(
    TalonTagImportDeclaration,
    "__reduce__",
    lambda self: (TalonTagImportDeclaration, dataclasses.astuple(self)),
)
setattr(
    TalonVariable,
    "__reduce__",
    lambda self: (TalonVariable, dataclasses.astuple(self)),
)
setattr(
    TalonWord,
    "__reduce__",
    lambda self: (TalonWord, dataclasses.astuple(self)),
)
