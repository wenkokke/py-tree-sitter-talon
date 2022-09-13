import collections.abc
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
# Generic 'to_parser'
################################################################################


def to_parser(
    node: typing.Union[TalonSourceFile, TalonCommandDeclaration, AnyTalonRule],
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> typing.Union[parsec.Parser, parsec.Parser]:
    to_parser = getattr(node, "to_parser")
    return to_parser(fullmatch=fullmatch, get_capture=get_capture, get_list=get_list)


################################################################################
# Implement 'match' and 'find_command'
################################################################################


def find_command(
    self: TalonSourceFile,
    text: collections.abc.Sequence[str],
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> typing.Optional[TalonCommandDeclaration]:
    parser = to_parser(
        self, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
    )
    try:
        return parser.parse_strict(text)
    except parsec.ParseError:
        return None


def match(
    self: typing.Union[TalonCommandDeclaration, AnyTalonRule],
    text: collections.abc.Sequence[str],
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> bool:
    parser = to_parser(
        self, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
    )
    try:
        parser.parse_strict(text)
        return True
    except parsec.ParseError:
        return False


################################################################################
# Compile TalonSourceFile to parsec.Parser
################################################################################


def _TalonSourceFile_to_parser(
    self: TalonSourceFile,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
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


setattr(TalonSourceFile, "find_command", find_command)
setattr(TalonSourceFile, "to_parser", _TalonSourceFile_to_parser)

################################################################################
# Compile TalonCommandDeclaration to parsec.Parser
################################################################################


def _TalonCommandDeclaration_to_parser(
    self: TalonCommandDeclaration,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
) -> parsec.Parser:
    return to_parser(
        self.rule, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
    ).result(self)


setattr(TalonCommandDeclaration, "match", match)
setattr(TalonCommandDeclaration, "to_parser", _TalonCommandDeclaration_to_parser)

################################################################################
# Implement AnyTalonRule.to_parser
################################################################################


def _always() -> parsec.Parser:
    def _always_parser(text: collections.abc.Sequence[str], index: int):
        return parsec.Value.success(index, None)

    return parsec.Parser(fn=_always_parser)


def _word(token: str) -> parsec.Parser:
    def _word_parser(text: collections.abc.Sequence[str], index: int):
        if text[index] == token:
            return parsec.Value.success(index + 1, None)
        else:
            return parsec.Value.failure(index, str(token))

    return parsec.Parser(fn=_word_parser)


def _TalonCapture_to_parser(
    self: TalonCapture,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
) -> parsec.Parser:
    capture_name = self.capture_name.text
    if get_capture:
        capture = get_capture(capture_name)
        if capture:
            return to_parser(capture, get_capture=get_capture, get_list=get_list)
    return _word(f"<{capture_name}>").result(None)


setattr(TalonCapture, "match", match)
setattr(TalonCapture, "to_parser", _TalonCapture_to_parser)


def _TalonChoice_to_parser(
    self: TalonChoice,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
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


setattr(TalonChoice, "match", match)
setattr(TalonChoice, "to_parser", _TalonChoice_to_parser)


def _TalonEndAnchor_to_parser(
    self: TalonEndAnchor,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
) -> parsec.Parser:
    if fullmatch:
        return parsec.eof()
    else:
        return _always()


setattr(TalonEndAnchor, "match", match)
setattr(TalonEndAnchor, "to_parser", _TalonEndAnchor_to_parser)


def _TalonList_to_parser(
    self: TalonList,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
) -> parsec.Parser:
    list_name = self.list_name.text
    if get_list:
        list_value = get_list(list_name)
        if isinstance(list_value, dict):
            list_value = list(list_value.keys())
        if isinstance(list_value, list):
            return parsec.one_of([item for item in list_value]).result(None)
    return _word(f"{{{list_name}}}").result(None)


setattr(TalonList, "match", match)
setattr(TalonList, "to_parser", _TalonList_to_parser)


def _TalonOptional_to_parser(
    self: TalonOptional,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
) -> parsec.Parser:
    return parsec.optional(
        to_parser(
            self.get_child(),
            fullmatch=fullmatch,
            get_capture=get_capture,
            get_list=get_list,
        )
    ).result(None)


setattr(TalonOptional, "match", match)
setattr(TalonOptional, "to_parser", _TalonOptional_to_parser)


def _TalonParenthesizedRule_to_parser(
    self: TalonParenthesizedRule,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
) -> parsec.Parser:
    return to_parser(
        self.get_child(),
        fullmatch=fullmatch,
        get_capture=get_capture,
        get_list=get_list,
    ).result(None)


setattr(TalonParenthesizedRule, "match", match)
setattr(TalonParenthesizedRule, "to_parser", _TalonParenthesizedRule_to_parser)


def _TalonRepeat_to_parser(
    self: TalonRepeat,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
) -> parsec.Parser:
    return parsec.many(
        to_parser(
            self.get_child(),
            fullmatch=fullmatch,
            get_capture=get_capture,
            get_list=get_list,
        )
    ).result(None)


setattr(TalonRepeat, "match", match)
setattr(TalonRepeat, "to_parser", _TalonRepeat_to_parser)


def _TalonRepeat1_to_parser(
    self: TalonRepeat1,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
) -> parsec.Parser:
    return parsec.many1(
        to_parser(
            self.get_child(),
            fullmatch=fullmatch,
            get_capture=get_capture,
            get_list=get_list,
        )
    ).result(None)


setattr(TalonRepeat1, "match", match)
setattr(TalonRepeat1, "to_parser", _TalonRepeat1_to_parser)


def _TalonRule_to_parser(
    self: TalonRule,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
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


setattr(TalonRule, "match", match)
setattr(TalonRule, "to_parser", _TalonRule_to_parser)


def _TalonSeq_to_parser(
    self: TalonSeq,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
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


setattr(TalonSeq, "match", match)
setattr(TalonSeq, "to_parser", _TalonSeq_to_parser)


def _TalonStartAnchor_to_parser(
    self: TalonStartAnchor,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
) -> parsec.Parser:
    if fullmatch:

        def start_anchor_parser(
            text: collections.abc.Sequence[str], index: int
        ) -> parsec.Parser:
            if index == 0:
                return parsec.Value.success(index, None)
            else:
                return parsec.Value.failure(index, "should be start of the input")

        return parsec.Parser(fn=start_anchor_parser)
    else:
        return _always()


setattr(TalonStartAnchor, "match", match)
setattr(TalonStartAnchor, "to_parser", _TalonStartAnchor_to_parser)


def _TalonWord_to_parser(
    self: TalonWord,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ],
) -> parsec.Parser:
    return _word(self.text).result(None)


setattr(TalonWord, "match", match)
setattr(TalonWord, "to_parser", _TalonWord_to_parser)
