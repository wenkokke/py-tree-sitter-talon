import collections.abc
import re
import typing

from .dynamic import (
    TalonCapture,
    TalonChoice,
    TalonComment,
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
)

TalonRuleTop = typing.Union[
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

TalonCaptureLookup = collections.abc.Callable[[str], typing.Optional[TalonRuleTop]]
TalonListLookup = collections.abc.Callable[[str], typing.Optional[list[str]]]


def compile(
    rule: TalonRuleTop,
    *,
    captures: typing.Optional[TalonCaptureLookup] = None,
    lists: typing.Optional[TalonListLookup] = None,
) -> re.Pattern[str]:
    captures = captures or (lambda capture_name: None)
    lists = lists or (lambda list_name: None)
    return re.compile(_pattern_str(rule, captures=captures, lists=lists))


def _get_only_child(
    children: typing.Sequence[typing.Union[TalonRuleTop, TalonComment]]
) -> TalonRuleTop:
    for i, child in enumerate(children):
        if not isinstance(child, TalonComment):
            assert all(isinstance(child, TalonComment) for child in children[i + 1 :])
            return child
    raise ValueError(children)


def _pattern_str(
    rule: TalonRuleTop, *, captures: TalonCaptureLookup, lists: TalonListLookup
) -> str:
    if isinstance(rule, TalonCapture):
        capture_name = rule.capture_name.text.strip()
        capture_rule = captures(capture_name)
        if capture_rule:
            return _pattern_str(capture_rule, captures=captures, lists=lists)
        else:
            return re.escape(rf"<{capture_name}>")
    elif isinstance(rule, TalonChoice):
        pattern_str = r"|".join(
            [
                _pattern_str(child, captures=captures, lists=lists)
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
        pattern_str = _pattern_str(child, captures=captures, lists=lists)
        return rf"({pattern_str})?"
    elif isinstance(rule, TalonParenthesizedRule):
        child = _get_only_child(rule.children)
        pattern_str = _pattern_str(child, captures=captures, lists=lists)
        return rf"({pattern_str})"
    elif isinstance(rule, TalonRepeat):
        child = _get_only_child(rule.children)
        pattern_str = _pattern_str(child, captures=captures, lists=lists)
        return rf"({pattern_str})*"
    elif isinstance(rule, TalonRepeat1):
        child = _get_only_child(rule.children)
        pattern_str = _pattern_str(child, captures=captures, lists=lists)
        return rf"({pattern_str})+"
    elif isinstance(rule, TalonRule):
        return r"\s+".join(
            [
                _pattern_str(child, captures=captures, lists=lists)
                for child in rule.children
                if not isinstance(child, TalonComment)
            ]
        )
    elif isinstance(rule, TalonSeq):
        return r"\s+".join(
            [
                _pattern_str(child, captures=captures, lists=lists)
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
