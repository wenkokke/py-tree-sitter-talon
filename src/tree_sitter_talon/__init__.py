import warnings
from dataclasses import fields, is_dataclass
from functools import partial
from typing import Any, Iterable, List, Optional, Sequence, Tuple, Type

from ._compat import _removeprefix
from ._internal.dynamic import (
    Branch,
    Leaf,
    Node,
    NodeFieldName,
    NodeTypeError,
    NodeTypeName,
    ParseError,
    Point,
    TalonAction,
    TalonArgumentList,
    TalonAssignmentStatement,
    TalonBinaryOperator,
    TalonBlock,
    TalonCapture,
    TalonChoice,
    TalonCommandDeclaration,
    TalonComment,
    TalonDeclaration,
    TalonDeclarations,
    TalonEndAnchor,
    TalonError,
    TalonExpression,
    TalonExpressionStatement,
    TalonFloat,
    TalonIdentifier,
    TalonImplicitString,
    TalonInteger,
    TalonInterpolation,
    TalonKeyAction,
    TalonKeyBindingDeclaration,
    TalonList,
    TalonMatch,
    TalonMatches,
    TalonMatchModifier,
    TalonNumber,
    TalonOperator,
    TalonOptional,
    TalonParenthesizedExpression,
    TalonParenthesizedRule,
    TalonRepeat,
    TalonRepeat1,
    TalonRule,
    TalonSeq,
    TalonSettingsDeclaration,
    TalonSleepAction,
    TalonSourceFile,
    TalonStartAnchor,
    TalonStatement,
    TalonString,
    TalonStringContent,
    TalonStringEscapeSequence,
    TalonTagImportDeclaration,
    TalonUnaryOperator,
    TalonVariable,
    TalonWord,
    from_tree_sitter,
    language,
    parse,
    parse_file,
    parser,
)
from ._internal.match import AnyTalonRule, ListValue, find_command, match
from ._version import VERSION

################################################################################
# Export List
################################################################################

__all__ = [
    "Branch",
    "Leaf",
    "Node",
    "NodeFieldName",
    "NodeTypeError",
    "NodeTypeName",
    "ParseError",
    "Point",
    "TalonAction",
    "TalonArgumentList",
    "TalonAssignmentStatement",
    "TalonBinaryOperator",
    "TalonBlock",
    "TalonCapture",
    "TalonChoice",
    "TalonCommandDeclaration",
    "TalonComment",
    "TalonDeclaration",
    "TalonDeclarations",
    "TalonEndAnchor",
    "TalonError",
    "TalonExpression",
    "TalonExpressionStatement",
    "TalonFloat",
    "TalonIdentifier",
    "TalonImplicitString",
    "TalonInteger",
    "TalonInterpolation",
    "TalonKeyAction",
    "TalonKeyBindingDeclaration",
    "TalonList",
    "TalonMatch",
    "TalonMatches",
    "TalonMatchModifier",
    "TalonNumber",
    "TalonOperator",
    "TalonOptional",
    "TalonParenthesizedExpression",
    "TalonParenthesizedRule",
    "TalonRepeat",
    "TalonRepeat1",
    "TalonRule",
    "TalonSeq",
    "TalonSettingsDeclaration",
    "TalonSleepAction",
    "TalonSourceFile",
    "TalonStartAnchor",
    "TalonStatement",
    "TalonString",
    "TalonStringContent",
    "TalonStringEscapeSequence",
    "TalonTagImportDeclaration",
    "TalonUnaryOperator",
    "TalonVariable",
    "TalonWord",
    "from_tree_sitter",
    "language",
    "parse",
    "parse_file",
    "parser",
    "AnyTalonRule",
    "ListValue",
    "find_command",
    "match",
    "VERSION",
]

################################################################################
# Properties for backwards compatibility
################################################################################


def _TalonMatch_key(self: TalonMatch) -> TalonIdentifier:
    warnings.warn(
        "'key' was deprecated in 1004.3.1.0; use 'left'",
        DeprecationWarning,
        stacklevel=2,
    )
    return self.left


setattr(
    TalonMatch,
    "key",
    property(_TalonMatch_key),
)


def _TalonMatch_modifier(self: TalonMatch) -> Sequence[TalonMatchModifier]:
    warnings.warn(
        "'modifier' was deprecated in 1004.3.1.0; use 'modifiers'",
        DeprecationWarning,
        stacklevel=2,
    )
    return self.modifiers


setattr(
    TalonMatch,
    "modifier",
    property(_TalonMatch_modifier),
)


def _TalonMatch_pattern(self: TalonMatch) -> TalonImplicitString:
    warnings.warn(
        "'pattern' was deprecated in 1004.3.1.0; use 'right'",
        DeprecationWarning,
        stacklevel=2,
    )
    return self.right


setattr(
    TalonMatch,
    "pattern",
    property(_TalonMatch_pattern),
)


def _TalonCommandDeclaration_rule(self: TalonCommandDeclaration) -> TalonRule:
    warnings.warn(
        "'rule' was deprecated in 1004.3.1.0; use 'left'",
        DeprecationWarning,
        stacklevel=2,
    )
    return self.left


setattr(
    TalonCommandDeclaration,
    "rule",
    property(_TalonCommandDeclaration_rule),
)


def _TalonCommandDeclaration_script(self: TalonCommandDeclaration) -> TalonBlock:
    warnings.warn(
        "'script' was deprecated in 1004.3.1.0; use 'right'",
        DeprecationWarning,
        stacklevel=2,
    )
    return self.right


setattr(
    TalonCommandDeclaration,
    "script",
    property(_TalonCommandDeclaration_script),
)


def _TalonKeyBindingDeclaration_key(self: TalonKeyBindingDeclaration) -> TalonKeyAction:
    warnings.warn(
        "'key' was deprecated in 1004.3.1.0; use 'left'",
        DeprecationWarning,
        stacklevel=2,
    )
    return self.left


setattr(
    TalonKeyBindingDeclaration,
    "key",
    property(_TalonKeyBindingDeclaration_key),
)


def _TalonKeyBindingDeclaration_script(self: TalonKeyBindingDeclaration) -> TalonBlock:
    warnings.warn(
        "'script' was deprecated in 1004.3.1.0; use 'right'",
        DeprecationWarning,
        stacklevel=2,
    )
    return self.right


setattr(
    TalonKeyBindingDeclaration,
    "script",
    property(_TalonKeyBindingDeclaration_script),
)


def _TalonTagImportDeclaration_tag(self: TalonTagImportDeclaration) -> TalonIdentifier:
    warnings.warn(
        "'tag' was deprecated in 1004.3.1.0; use 'right'",
        DeprecationWarning,
        stacklevel=2,
    )
    return self.right


setattr(
    TalonTagImportDeclaration,
    "tag",
    property(_TalonTagImportDeclaration_tag),
)

################################################################################
# Method to test if a matches block is explicit
################################################################################


def _TalonMatches_is_explicit(self: TalonMatches) -> bool:
    return self.text == "-" or self.text.endswith("\n-")


setattr(TalonMatches, "is_explicit", _TalonMatches_is_explicit)


################################################################################
# Redefine __init__ to merge comments into block
################################################################################


def _TalonBlock_with_comments(
    self: TalonBlock, comments: Optional[Sequence[TalonComment]]
) -> TalonBlock:
    return TalonBlock(
        text=self.text,
        type_name=self.type_name,
        start_position=self.start_position,
        end_position=self.end_position,
        children=[*(comments or ()), *self.children],
    )


def _TalonCommandDeclaration___init__(
    self: TalonCommandDeclaration,
    text: str,
    type_name: NodeTypeName,
    start_position: Point,
    end_position: Point,
    children: Optional[Sequence[TalonComment]],
    left: TalonRule,
    right: TalonBlock,
) -> None:
    self.text = text
    self.type_name = type_name
    self.start_position = start_position
    self.end_position = end_position
    self.children = None
    self.left = left
    self.right = _TalonBlock_with_comments(right, children)


setattr(TalonCommandDeclaration, "__init__", _TalonCommandDeclaration___init__)


def _TalonKeyBindingDeclaration___init__(
    self: TalonKeyBindingDeclaration,
    text: str,
    type_name: NodeTypeName,
    start_position: Point,
    end_position: Point,
    children: Optional[Sequence[TalonComment]],
    left: TalonKeyAction,
    right: TalonBlock,
) -> None:
    self.text = text
    self.type_name = type_name
    self.start_position = start_position
    self.end_position = end_position
    self.children = None
    self.left = left
    self.right = _TalonBlock_with_comments(right, children)


setattr(TalonKeyBindingDeclaration, "__init__", _TalonKeyBindingDeclaration___init__)


def _TalonSettingsDeclaration___init__(
    self: TalonSettingsDeclaration,
    text: str,
    type_name: NodeTypeName,
    start_position: Point,
    end_position: Point,
    children: Optional[Sequence[TalonComment]],
    right: TalonBlock,
) -> None:
    self.text = text
    self.type_name = type_name
    self.start_position = start_position
    self.end_position = end_position
    self.children = None
    self.right = _TalonBlock_with_comments(right, children)


setattr(TalonSettingsDeclaration, "__init__", _TalonSettingsDeclaration___init__)


################################################################################
# Method to test if a declaration is short
################################################################################


def _TalonBlock_is_short(self: TalonBlock) -> bool:
    return len(self.children) <= 1


setattr(TalonBlock, "is_short", _TalonBlock_is_short)


def _TalonCommandDeclaration_is_short(self: TalonCommandDeclaration) -> bool:
    return self.right.is_short()


setattr(TalonCommandDeclaration, "is_short", _TalonCommandDeclaration_is_short)


def _TalonSettingsDeclaration_is_short(self: TalonSettingsDeclaration) -> bool:
    return self.right.is_short()


setattr(TalonSettingsDeclaration, "is_short", _TalonSettingsDeclaration_is_short)


def _TalonKeyBindingDeclaration_is_short(self: TalonKeyBindingDeclaration) -> bool:
    return self.right.is_short()


setattr(TalonKeyBindingDeclaration, "is_short", _TalonKeyBindingDeclaration_is_short)


################################################################################
# Method to test if a node is extra
################################################################################


def _is_extra(self: Node) -> bool:
    """
    Check if a node is an extra node.
    """
    return isinstance(self, (TalonComment,))


setattr(Node, "is_extra", _is_extra)


################################################################################
# Method to get only non-extra child
################################################################################


def _get_child_fail_msg(self: Node, children: Iterable[Node] = []) -> str:
    return "\n".join(
        [
            f"Node '{self.type_name}' should have exactly one non-comment child, found:",
            *[f"- {child}" for child in children],
            f"in {self}",
        ]
    )


def _get_child(self: Node) -> Node:
    """
    Get the only non-extra child of a branch node.
    """
    assert isinstance(self, Branch)
    assert self.children is not None, _get_child_fail_msg(self)
    if isinstance(self.children, Node):
        assert not _is_extra(self.children), _get_child_fail_msg(
            self, children=[self.children]
        )
        return self.children
    else:
        for i in range(0, len(self.children)):
            if _is_extra(self.children[i]):
                continue
            assert all(
                _is_extra(child) for child in self.children[i + 1 :]
            ), _get_child_fail_msg(self, children=self.children)
            return self.children[i]
        raise AssertionError(_get_child_fail_msg(self, children=self.children))


setattr(TalonOptional, "get_child", _get_child)
setattr(TalonParenthesizedRule, "get_child", _get_child)
setattr(TalonRepeat, "get_child", _get_child)
setattr(TalonRepeat1, "get_child", _get_child)
setattr(TalonParenthesizedExpression, "get_child", _get_child)
setattr(TalonInterpolation, "get_child", _get_child)

################################################################################
# Method to get docstrings
##############################################_removeprefix##################################


def _TalonComment_get_docstring(self: TalonComment) -> Optional[str]:
    if self.text.startswith("###"):
        return _removeprefix(self.text, "###").strip()
    return None


setattr(TalonComment, "get_docstring", _TalonComment_get_docstring)


def _TalonSourceFile_get_docstring(self: TalonSourceFile) -> Optional[str]:
    docstrings: List[str] = []
    for comment in self.children:
        if isinstance(comment, TalonComment):
            docstring = _TalonComment_get_docstring(comment)
            if docstring:
                docstrings.append(docstring)
        else:
            break
    return "\n".join(docstrings) if docstrings else None


setattr(TalonSourceFile, "get_docstring", _TalonSourceFile_get_docstring)


def _TalonCommandDeclaration_get_docstring(
    self: TalonCommandDeclaration,
) -> Optional[str]:
    docstrings: List[str] = []
    for comment in self.right.children:
        if isinstance(comment, TalonComment):
            docstring = _TalonComment_get_docstring(comment)
            if docstring:
                docstrings.append(docstring)
    return "\n".join(docstrings) if docstrings else None


setattr(
    TalonCommandDeclaration, "get_docstring", _TalonCommandDeclaration_get_docstring
)


################################################################################
# Pickle Compatibility
################################################################################


def _fields(obj: Type[Any]) -> Tuple[Any, ...]:
    assert is_dataclass(obj)
    return tuple(getattr(obj, field.name) for field in fields(obj))


def _make_TalonAction(*args: Any) -> TalonAction:
    return TalonAction(*args)


setattr(
    TalonAction,
    "__reduce__",
    lambda self: (_make_TalonAction, _fields(self)),
)


def _make_TalonArgumentList(*args: Any) -> TalonArgumentList:
    return TalonArgumentList(*args)


setattr(
    TalonArgumentList,
    "__reduce__",
    lambda self: (_make_TalonArgumentList, _fields(self)),
)


def _make_TalonAssignmentStatement(*args: Any) -> TalonAssignmentStatement:
    return TalonAssignmentStatement(*args)


setattr(
    TalonAssignmentStatement,
    "__reduce__",
    lambda self: (_make_TalonAssignmentStatement, _fields(self)),
)


def _make_TalonBinaryOperator(*args: Any) -> TalonBinaryOperator:
    return TalonBinaryOperator(*args)


setattr(
    TalonBinaryOperator,
    "__reduce__",
    lambda self: (_make_TalonBinaryOperator, _fields(self)),
)


def _make_TalonBlock(*args: Any) -> TalonBlock:
    return TalonBlock(*args)


setattr(
    TalonBlock,
    "__reduce__",
    lambda self: (_make_TalonBlock, _fields(self)),
)


def _make_TalonCapture(*args: Any) -> TalonCapture:
    return TalonCapture(*args)


setattr(
    TalonCapture,
    "__reduce__",
    lambda self: (_make_TalonCapture, _fields(self)),
)


def _make_TalonChoice(*args: Any) -> TalonChoice:
    return TalonChoice(*args)


setattr(
    TalonChoice,
    "__reduce__",
    lambda self: (_make_TalonChoice, _fields(self)),
)


def _make_TalonCommandDeclaration(*args: Any) -> TalonCommandDeclaration:
    return TalonCommandDeclaration(*args)


setattr(
    TalonCommandDeclaration,
    "__reduce__",
    lambda self: (_make_TalonCommandDeclaration, _fields(self)),
)


def _make_TalonComment(*args: Any) -> TalonComment:
    return TalonComment(*args)


setattr(
    TalonComment,
    "__reduce__",
    lambda self: (_make_TalonComment, _fields(self)),
)


def _make_TalonDeclarations(*args: Any) -> TalonDeclarations:
    return TalonDeclarations(*args)


setattr(
    TalonDeclarations,
    "__reduce__",
    lambda self: (_make_TalonDeclarations, _fields(self)),
)


def _make_TalonDeclaration(*args: Any) -> TalonDeclaration:
    return TalonDeclaration(*args)


setattr(
    TalonDeclaration,
    "__reduce__",
    lambda self: (_make_TalonDeclaration, _fields(self)),
)


def _make_TalonEndAnchor(*args: Any) -> TalonEndAnchor:
    return TalonEndAnchor(*args)


setattr(
    TalonEndAnchor,
    "__reduce__",
    lambda self: (_make_TalonEndAnchor, _fields(self)),
)


def _make_TalonError(*args: Any) -> TalonError:
    return TalonError(*args)


setattr(
    TalonError,
    "__reduce__",
    lambda self: (_make_TalonError, _fields(self)),
)


def _make_TalonExpression(*args: Any) -> TalonExpression:
    return TalonExpression(*args)


setattr(
    TalonExpression,
    "__reduce__",
    lambda self: (_make_TalonExpression, _fields(self)),
)


def _make_TalonExpressionStatement(*args: Any) -> TalonExpressionStatement:
    return TalonExpressionStatement(*args)


setattr(
    TalonExpressionStatement,
    "__reduce__",
    lambda self: (_make_TalonExpressionStatement, _fields(self)),
)


def _make_TalonFloat(*args: Any) -> TalonFloat:
    return TalonFloat(*args)


setattr(
    TalonFloat,
    "__reduce__",
    lambda self: (_make_TalonFloat, _fields(self)),
)


def _make_TalonIdentifier(*args: Any) -> TalonIdentifier:
    return TalonIdentifier(*args)


setattr(
    TalonIdentifier,
    "__reduce__",
    lambda self: (_make_TalonIdentifier, _fields(self)),
)


def _make_TalonImplicitString(*args: Any) -> TalonImplicitString:
    return TalonImplicitString(*args)


setattr(
    TalonImplicitString,
    "__reduce__",
    lambda self: (_make_TalonImplicitString, _fields(self)),
)


def _make_TalonInteger(*args: Any) -> TalonInteger:
    return TalonInteger(*args)


setattr(
    TalonInteger,
    "__reduce__",
    lambda self: (_make_TalonInteger, _fields(self)),
)


def _make_TalonInterpolation(*args: Any) -> TalonInterpolation:
    return TalonInterpolation(*args)


setattr(
    TalonInterpolation,
    "__reduce__",
    lambda self: (_make_TalonInterpolation, _fields(self)),
)


def _make_TalonKeyAction(*args: Any) -> TalonKeyAction:
    return TalonKeyAction(*args)


setattr(
    TalonKeyAction,
    "__reduce__",
    lambda self: (_make_TalonKeyAction, _fields(self)),
)


def _make_TalonKeyBindingDeclaration(*args: Any) -> TalonKeyBindingDeclaration:
    return TalonKeyBindingDeclaration(*args)


setattr(
    TalonKeyBindingDeclaration,
    "__reduce__",
    lambda self: (_make_TalonKeyBindingDeclaration, _fields(self)),
)


def _make_TalonList(*args: Any) -> TalonList:
    return TalonList(*args)


setattr(
    TalonList,
    "__reduce__",
    lambda self: (_make_TalonList, _fields(self)),
)


def _make_TalonMatch(*args: Any) -> TalonMatch:
    return TalonMatch(*args)


setattr(
    TalonMatch,
    "__reduce__",
    lambda self: (_make_TalonMatch, _fields(self)),
)


def _make_TalonMatches(*args: Any) -> TalonMatches:
    return TalonMatches(*args)


setattr(
    TalonMatches,
    "__reduce__",
    lambda self: (_make_TalonMatches, _fields(self)),
)


def _make_TalonMatchModifier(*args: Any) -> TalonMatchModifier:
    return TalonMatchModifier(*args)


setattr(
    TalonMatchModifier,
    "__reduce__",
    lambda self: (_make_TalonMatchModifier, _fields(self)),
)


def _make_TalonNumber(*args: Any) -> TalonNumber:
    return TalonNumber(*args)


setattr(
    TalonNumber,
    "__reduce__",
    lambda self: (_make_TalonNumber, _fields(self)),
)


def _make_TalonOperator(*args: Any) -> TalonOperator:
    return TalonOperator(*args)


setattr(
    TalonOperator,
    "__reduce__",
    lambda self: (_make_TalonOperator, _fields(self)),
)


def _make_TalonOptional(*args: Any) -> TalonOptional:
    return TalonOptional(*args)


setattr(
    TalonOptional,
    "__reduce__",
    lambda self: (_make_TalonOptional, _fields(self)),
)


def _make_TalonParenthesizedExpression(*args: Any) -> TalonParenthesizedExpression:
    return TalonParenthesizedExpression(*args)


setattr(
    TalonParenthesizedExpression,
    "__reduce__",
    lambda self: (_make_TalonParenthesizedExpression, _fields(self)),
)


def _make_TalonParenthesizedRule(*args: Any) -> TalonParenthesizedRule:
    return TalonParenthesizedRule(*args)


setattr(
    TalonParenthesizedRule,
    "__reduce__",
    lambda self: (_make_TalonParenthesizedRule, _fields(self)),
)


def _make_TalonRepeat(*args: Any) -> TalonRepeat:
    return TalonRepeat(*args)


setattr(
    TalonRepeat,
    "__reduce__",
    lambda self: (_make_TalonRepeat, _fields(self)),
)


def _make_TalonRepeat1(*args: Any) -> TalonRepeat1:
    return TalonRepeat1(*args)


setattr(
    TalonRepeat1,
    "__reduce__",
    lambda self: (_make_TalonRepeat1, _fields(self)),
)


def _make_TalonRule(*args: Any) -> TalonRule:
    return TalonRule(*args)


setattr(
    TalonRule,
    "__reduce__",
    lambda self: (_make_TalonRule, _fields(self)),
)


def _make_TalonSeq(*args: Any) -> TalonSeq:
    return TalonSeq(*args)


setattr(
    TalonSeq,
    "__reduce__",
    lambda self: (_make_TalonSeq, _fields(self)),
)


def _make_TalonSettingsDeclaration(*args: Any) -> TalonSettingsDeclaration:
    return TalonSettingsDeclaration(*args)


setattr(
    TalonSettingsDeclaration,
    "__reduce__",
    lambda self: (_make_TalonSettingsDeclaration, _fields(self)),
)


def _make_TalonSleepAction(*args: Any) -> TalonSleepAction:
    return TalonSleepAction(*args)


setattr(
    TalonSleepAction,
    "__reduce__",
    lambda self: (_make_TalonSleepAction, _fields(self)),
)


def _make_TalonSourceFile(*args: Any) -> TalonSourceFile:
    return TalonSourceFile(*args)


setattr(
    TalonSourceFile,
    "__reduce__",
    lambda self: (_make_TalonSourceFile, _fields(self)),
)


def _make_TalonStartAnchor(*args: Any) -> TalonStartAnchor:
    return TalonStartAnchor(*args)


setattr(
    TalonStartAnchor,
    "__reduce__",
    lambda self: (_make_TalonStartAnchor, _fields(self)),
)


def _make_TalonStatement(*args: Any) -> TalonStatement:
    return TalonStatement(*args)


setattr(
    TalonStatement,
    "__reduce__",
    lambda self: (_make_TalonStatement, _fields(self)),
)


def _make_TalonString(*args: Any) -> TalonString:
    return TalonString(*args)


setattr(
    TalonString,
    "__reduce__",
    lambda self: (_make_TalonString, _fields(self)),
)


def _make_TalonStringContent(*args: Any) -> TalonStringContent:
    return TalonStringContent(*args)


setattr(
    TalonStringContent,
    "__reduce__",
    lambda self: (_make_TalonStringContent, _fields(self)),
)


def _make_TalonStringEscapeSequence(*args: Any) -> TalonStringEscapeSequence:
    return TalonStringEscapeSequence(*args)


setattr(
    TalonStringEscapeSequence,
    "__reduce__",
    lambda self: (_make_TalonStringEscapeSequence, _fields(self)),
)


def _make_TalonTagImportDeclaration(*args: Any) -> TalonTagImportDeclaration:
    return TalonTagImportDeclaration(*args)


setattr(
    TalonTagImportDeclaration,
    "__reduce__",
    lambda self: (_make_TalonTagImportDeclaration, _fields(self)),
)


def _make_TalonUnaryOperator(*args: Any) -> TalonUnaryOperator:
    return TalonUnaryOperator(*args)


setattr(
    TalonUnaryOperator,
    "__reduce__",
    lambda self: (_make_TalonUnaryOperator, _fields(self)),
)


def _make_TalonVariable(*args: Any) -> TalonVariable:
    return TalonVariable(*args)


setattr(
    TalonVariable,
    "__reduce__",
    lambda self: (_make_TalonVariable, _fields(self)),
)


def _make_TalonWord(*args: Any) -> TalonWord:
    return TalonWord(*args)


setattr(
    TalonWord,
    "__reduce__",
    lambda self: (_make_TalonWord, _fields(self)),
)
