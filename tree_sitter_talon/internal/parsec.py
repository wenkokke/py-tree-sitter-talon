import collections.abc
import functools
import typing

import parsec

from .dynamic import (
    TalonCapture,
    TalonChoice,
    TalonCommandDeclaration,
    TalonComment,
    TalonDeclarations,
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
    parser = _to_parser(
        self, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
    )
    try:
        return parser.parse_strict(text)
    except parsec.ParseError:
        return None


setattr(TalonSourceFile, "find_command", find_command)


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
    parser = _to_parser(
        self, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
    )
    try:
        parser.parse_strict(text)
        return True
    except parsec.ParseError:
        return False


setattr(TalonCommandDeclaration, "match", match)
setattr(TalonCapture, "match", match)
setattr(TalonChoice, "match", match)
setattr(TalonEndAnchor, "match", match)
setattr(TalonList, "match", match)
setattr(TalonOptional, "match", match)
setattr(TalonParenthesizedRule, "match", match)
setattr(TalonRepeat, "match", match)
setattr(TalonRepeat1, "match", match)
setattr(TalonRule, "match", match)
setattr(TalonSeq, "match", match)
setattr(TalonStartAnchor, "match", match)
setattr(TalonWord, "match", match)

################################################################################
# Generic '_to_parser'
################################################################################


def _to_parser(
    node: typing.Union[
        TalonSourceFile, TalonDeclarations, TalonCommandDeclaration, AnyTalonRule
    ],
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        collections.abc.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> typing.Union[parsec.Parser, parsec.Parser]:
    if isinstance(node, TalonCapture):
        return _TalonCapture_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonChoice):
        return _TalonChoice_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonCommandDeclaration):
        return _TalonCommandDeclaration_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonDeclarations):
        return _TalonDeclarations_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonEndAnchor):
        return _TalonEndAnchor_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonList):
        return _TalonList_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonOptional):
        return _TalonOptional_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonParenthesizedRule):
        return _TalonParenthesizedRule_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonRepeat):
        return _TalonRepeat_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonRepeat1):
        return _TalonRepeat1_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonRule):
        return _TalonRule_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonSeq):
        return _TalonSeq_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonSourceFile):
        return _TalonSourceFile_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonStartAnchor):
        return _TalonStartAnchor_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonWord):
        return _TalonWord_to_parser(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )


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
    for declarations in self.children:
        if isinstance(declarations, TalonDeclarations):
            buffer.append(
                _to_parser(
                    declarations,
                    fullmatch=fullmatch,
                    get_capture=get_capture,
                    get_list=get_list,
                )
            )
    return functools.reduce(
        parsec.try_choice, buffer, parsec.fail_with(f"input does not match any command")
    )


################################################################################
# Compile TalonDeclarations to parsec.Parser
################################################################################


def _TalonDeclarations_to_parser(
    self: TalonDeclarations,
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
                _to_parser(
                    declaration,
                    fullmatch=fullmatch,
                    get_capture=get_capture,
                    get_list=get_list,
                )
            )
    return functools.reduce(
        parsec.try_choice, buffer, parsec.fail_with(f"input does not match any command")
    )


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
    return _to_parser(
        self.rule, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
    ).result(self)


################################################################################
# Implement AnyTalonRule._to_parser
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
            return _to_parser(capture, get_capture=get_capture, get_list=get_list)
    return _word(f"<{capture_name}>").result(None)


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
            parser = _to_parser(
                rule,
                fullmatch=fullmatch,
                get_capture=get_capture,
                get_list=get_list,
            )
            acc = parser ^ acc if acc else parser
    assert acc is not None
    return acc.result(None)


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
        _to_parser(
            self.get_child(),
            fullmatch=fullmatch,
            get_capture=get_capture,
            get_list=get_list,
        )
    ).result(None)


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
    return _to_parser(
        self.get_child(),
        fullmatch=fullmatch,
        get_capture=get_capture,
        get_list=get_list,
    ).result(None)


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
        _to_parser(
            self.get_child(),
            fullmatch=fullmatch,
            get_capture=get_capture,
            get_list=get_list,
        )
    ).result(None)


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
        _to_parser(
            self.get_child(),
            fullmatch=fullmatch,
            get_capture=get_capture,
            get_list=get_list,
        )
    ).result(None)


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
            parser = _to_parser(
                rule,
                fullmatch=fullmatch,
                get_capture=get_capture,
                get_list=get_list,
            )
            acc = (parser >> acc) if acc else parser
    assert acc is not None
    return acc.result(None)


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
            parser = _to_parser(
                rule,
                fullmatch=fullmatch,
                get_capture=get_capture,
                get_list=get_list,
            )
            acc = parser > acc if acc else parser
    assert acc is not None
    return acc.result(None)


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
