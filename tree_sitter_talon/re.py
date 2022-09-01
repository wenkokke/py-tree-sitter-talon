import re
from functools import singledispatch
from typing import Union

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

TalonRuleTop = Union[
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


def compile(
    rule: TalonRuleTop, *, captures: dict[str, str] = {}, lists: dict[str, str]
) -> re.Pattern[str]:
    return re.compile(compile_str(rule, captures=captures, lists=lists))


@singledispatch
def compile_str(
    rule: TalonRuleTop, *, captures: dict[str, str] = {}, lists: dict[str, str]
) -> str:
    raise TypeError(type(rule))


@compile_str.register
def _(
    rule: TalonCapture, *, captures: dict[str, str] = {}, lists: dict[str, str]
) -> str:
    capture_name = rule.capture_name.text.strip()
    capture_text = re.escape(rf"<{capture_name}>")
    return captures.get(capture_name, capture_text)


@compile_str.register
def _(
    rule: TalonChoice, *, captures: dict[str, str] = {}, lists: dict[str, str]
) -> str:
    rule_compile_str = r"|".join(
        [
            compile_str(child, captures=captures, lists=lists)
            for child in rule.children
            if not isinstance(child, TalonComment)
        ]
    )
    return rf"({rule_compile_str})"


@compile_str.register
def _(
    rule: TalonEndAnchor, *, captures: dict[str, str] = {}, lists: dict[str, str]
) -> str:
    return r"$"


@compile_str.register
def _(rule: TalonList, *, captures: dict[str, str] = {}, lists: dict[str, str]) -> str:
    list_name = rule.list_name.text.strip()
    list_text = re.escape(rf"<{list_name}>")
    return lists.get(list_name, list_text)


@compile_str.register
def _(
    rule: TalonOptional, *, captures: dict[str, str] = {}, lists: dict[str, str]
) -> str:
    rule_compile_str = compile_str(rule, captures=captures, lists=lists)
    return rf"({rule_compile_str})?"


@compile_str.register
def _(
    rule: TalonParenthesizedRule,
    *,
    captures: dict[str, str] = {},
    lists: dict[str, str],
) -> str:
    rule_compile_str = compile_str(rule, captures=captures, lists=lists)
    return rf"({rule_compile_str})"


@compile_str.register
def _(
    rule: TalonRepeat, *, captures: dict[str, str] = {}, lists: dict[str, str]
) -> str:
    rule_compile_str = compile_str(rule, captures=captures, lists=lists)
    return rf"({rule_compile_str})*"


@compile_str.register
def _(
    rule: TalonRepeat1, *, captures: dict[str, str] = {}, lists: dict[str, str]
) -> str:
    rule_compile_str = compile_str(rule, captures=captures, lists=lists)
    return rf"({rule_compile_str})+"


@compile_str.register
def _(rule: TalonRule, *, captures: dict[str, str] = {}, lists: dict[str, str]) -> str:
    return r"\s+".join(
        [
            compile_str(child, captures=captures, lists=lists)
            for child in rule.children
            if not isinstance(child, TalonComment)
        ]
    )


@compile_str.register
def _(rule: TalonSeq, *, captures: dict[str, str] = {}, lists: dict[str, str]) -> str:
    return r"\s+".join(
        [
            compile_str(child, captures=captures, lists=lists)
            for child in rule.children
            if not isinstance(child, TalonComment)
        ]
    )


@compile_str.register
def _(
    rule: TalonStartAnchor, *, captures: dict[str, str] = {}, lists: dict[str, str]
) -> str:
    return r"^"


@compile_str.register
def _(rule: TalonWord, *, captures: dict[str, str] = {}, lists: dict[str, str]) -> str:
    return re.escape(rule.text.strip())
