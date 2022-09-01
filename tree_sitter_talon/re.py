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


def compile(
    rule: TalonRuleTop, *, captures: dict[str, str] = {}, lists: dict[str, str] = {}
) -> re.Pattern[str]:
    return re.compile(_compile_str(rule, captures=captures, lists=lists))


def _get_only_child(
    children: typing.Sequence[typing.Union[TalonRuleTop, TalonComment]]
) -> TalonRuleTop:
    for i, child in enumerate(children):
        if not isinstance(child, TalonComment):
            assert all(isinstance(child, TalonComment) for child in children[i + 1 :])
            return child
    raise ValueError(children)


def _compile_str(
    rule: TalonRuleTop, *, captures: dict[str, str], lists: dict[str, str]
) -> str:
    if isinstance(rule, TalonCapture):
        capture_name = rule.capture_name.text.strip()
        capture_text = re.escape(rf"<{capture_name}>")
        return captures.get(capture_name, capture_text)
    elif isinstance(rule, TalonChoice):
        rule_compile_str = r"|".join(
            [
                _compile_str(child, captures=captures, lists=lists)
                for child in rule.children
                if not isinstance(child, TalonComment)
            ]
        )
        return rf"({rule_compile_str})"
    elif isinstance(rule, TalonEndAnchor):
        return r"$"
    elif isinstance(rule, TalonList):
        list_name = rule.list_name.text.strip()
        list_text = re.escape(rf"<{list_name}>")
        return lists.get(list_name, list_text)
    elif isinstance(rule, TalonOptional):
        child = _get_only_child(rule.children)
        rule_compile_str = _compile_str(child, captures=captures, lists=lists)
        return rf"({rule_compile_str})?"
    elif isinstance(rule, TalonParenthesizedRule):
        child = _get_only_child(rule.children)
        rule_compile_str = _compile_str(child, captures=captures, lists=lists)
        return rf"({rule_compile_str})"
    elif isinstance(rule, TalonRepeat):
        child = _get_only_child(rule.children)
        rule_compile_str = _compile_str(child, captures=captures, lists=lists)
        return rf"({rule_compile_str})*"
    elif isinstance(rule, TalonRepeat1):
        child = _get_only_child(rule.children)
        rule_compile_str = _compile_str(child, captures=captures, lists=lists)
        return rf"({rule_compile_str})+"
    elif isinstance(rule, TalonRule):
        return r"\s+".join(
            [
                _compile_str(child, captures=captures, lists=lists)
                for child in rule.children
                if not isinstance(child, TalonComment)
            ]
        )
    elif isinstance(rule, TalonSeq):
        return r"\s+".join(
            [
                _compile_str(child, captures=captures, lists=lists)
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
