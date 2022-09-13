import functools
import typing

import parsec

from .dynamic import (
    TalonCapture,
    TalonChoice,
    TalonCommandDeclaration,
    TalonComment,
    TalonEndAnchor,
    TalonList,
    TalonOptional,
    TalonParenthesizedRule,
    TalonRepeat,
    TalonRepeat1,
    TalonRule,
    TalonSeq,
    TalonSourceFile,
    TalonStartAnchor,
    TalonWord,
)

AnyTalonRule = typing.Union[
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

AnyListValue = typing.Union[list[str], dict[str, typing.Any]]

################################################################################
# Generic 'to_parser' method
################################################################################


@typing.overload
def to_parser(
    rule: TalonSourceFile,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> parsec.Parser:
    ...


@typing.overload
def to_parser(
    rule: TalonCommandDeclaration,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> parsec.Parser:
    ...


@typing.overload
def to_parser(
    rule: AnyTalonRule,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> parsec.Parser:
    ...


def to_parser(
    rule: typing.Union[TalonSourceFile, TalonCommandDeclaration, AnyTalonRule],
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> parsec.Parser:
    to_parser = getattr(rule, "to_parser")
    return to_parser(fullmatch=fullmatch, get_capture=get_capture, get_list=get_list)


################################################################################
# Compile TalonSourceFile to parsec.Parser
################################################################################


def _TalonSourceFile_to_parser(
    self: TalonSourceFile,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    buffer: list[parsec.Parser] = []
    for declaration in self.children:
        if isinstance(declaration, TalonCommandDeclaration):
            buffer.append(
                to_parser(
                    declaration,
                    fullmatch=fullmatch,
                    get_capture=get_capture,
                    get_list=get_list,
                )
            )
    return functools.reduce(
        parsec.try_choice, buffer, parsec.fail_with(f"input does not match any command")
    )


setattr(TalonSourceFile, "to_parser", _TalonSourceFile_to_parser)

################################################################################
# Compile TalonCommandDeclaration to parsec.Parser
################################################################################


def _TalonCommandDeclaration_to_parser(
    self: TalonCommandDeclaration,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    return to_parser(
        self.rule, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
    ).result(self)


setattr(TalonCommandDeclaration, "to_parser", _TalonCommandDeclaration_to_parser)

################################################################################
# Compile TalonRule to parsec.Parser
################################################################################


def _pure(value) -> parsec.Parser:
    return parsec.Parser(fn=lambda text, index: parsec.Value.success(index, value))


def _token(token) -> parsec.Parser:
    def _token_parser(text, index: int) -> parsec.Value:
        if text[index] == token:
            return parsec.Value.success(index + 1, None)
        else:
            return parsec.Value.failure(index, str(token))

    return parsec.Parser(fn=_token_parser)


def _TalonCapture_to_parser(
    self: TalonCapture,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    capture_name = self.capture_name.text
    if get_capture:
        capture = get_capture(capture_name)
        if capture:
            return to_parser(capture, get_capture=get_capture, get_list=get_list)
    return _token(f"<{capture_name}>").result(None)


setattr(TalonCapture, "to_parser", _TalonCapture_to_parser)


def _TalonChoice_to_parser(
    self: TalonChoice,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    acc: typing.Optional[parsec.Parser] = None
    for rule in reversed(self.children):
        if not isinstance(rule, TalonComment):
            parser = to_parser(
                rule,
                fullmatch=fullmatch,
                get_capture=get_capture,
                get_list=get_list,
            )
            acc = parser ^ acc if acc else parser
    assert acc is not None
    return acc.result(None)


setattr(TalonChoice, "to_parser", _TalonChoice_to_parser)


def _TalonEndAnchor_to_parser(
    self: TalonEndAnchor,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    if fullmatch:
        return parsec.eof()
    else:
        return _pure(None)


setattr(TalonEndAnchor, "to_parser", _TalonEndAnchor_to_parser)


def _TalonList_to_parser(
    self: TalonList,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    list_name = self.list_name.text
    if get_list:
        list_value = get_list(list_name)
        if isinstance(list_value, dict):
            list_value = list(list_value.keys())
        if isinstance(list_value, list):
            return parsec.one_of([[item] for item in list_value])
    return _token(f"{{{list_name}}}").result(None)


setattr(TalonList, "to_parser", _TalonList_to_parser)


def _TalonOptional_to_parser(
    self: TalonOptional,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    return parsec.optional(
        to_parser(
            self.get_child(),
            fullmatch=fullmatch,
            get_capture=get_capture,
            get_list=get_list,
        )
    ).result(None)


setattr(TalonOptional, "to_parser", _TalonOptional_to_parser)


def _TalonParenthesizedRule_to_parser(
    self: TalonParenthesizedRule,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    return to_parser(
        self.get_child(),
        fullmatch=fullmatch,
        get_capture=get_capture,
        get_list=get_list,
    ).result(None)


setattr(TalonParenthesizedRule, "to_parser", _TalonParenthesizedRule_to_parser)


def _TalonRepeat_to_parser(
    self: TalonRepeat,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    return parsec.many(
        to_parser(
            self.get_child(),
            fullmatch=fullmatch,
            get_capture=get_capture,
            get_list=get_list,
        )
    ).result(None)


setattr(TalonRepeat, "to_parser", _TalonRepeat_to_parser)


def _TalonRepeat1_to_parser(
    self: TalonRepeat1,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    return parsec.many1(
        to_parser(
            self.get_child(),
            fullmatch=fullmatch,
            get_capture=get_capture,
            get_list=get_list,
        )
    ).result(None)


setattr(TalonRepeat1, "to_parser", _TalonRepeat1_to_parser)


def _TalonRule_to_parser(
    self: TalonRule,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    acc: typing.Optional[parsec.Parser] = None
    for rule in reversed(self.children):
        if not isinstance(rule, TalonComment):
            parser = to_parser(
                rule,
                fullmatch=fullmatch,
                get_capture=get_capture,
                get_list=get_list,
            )
            acc = (parser >> acc) if acc else parser
    assert acc is not None
    return acc.result(None)


setattr(TalonRule, "to_parser", _TalonRule_to_parser)


def _TalonSeq_to_parser(
    self: TalonSeq,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    acc: typing.Optional[parsec.Parser] = None
    for rule in reversed(self.children):
        if not isinstance(rule, TalonComment):
            parser = to_parser(
                rule,
                fullmatch=fullmatch,
                get_capture=get_capture,
                get_list=get_list,
            )
            acc = parser > acc if acc else parser
    assert acc is not None
    return acc.result(None)


setattr(TalonSeq, "to_parser", _TalonSeq_to_parser)


def _TalonStartAnchor_to_parser(
    self: TalonStartAnchor,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    if fullmatch:

        def start_anchor_parser(text: parsec.Text, index: int) -> parsec.Value:
            if index == 0:
                return parsec.Value.success(index, None)
            else:
                return parsec.Value.failure(index, "should be start of the input")

        return parsec.Parser(fn=start_anchor_parser)
    else:
        return _pure(None)


setattr(TalonStartAnchor, "to_parser", _TalonStartAnchor_to_parser)


def _TalonWord_to_parser(
    self: TalonWord,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> parsec.Parser:
    return _token(self.text).result(None)


setattr(TalonWord, "to_parser", _TalonWord_to_parser)
