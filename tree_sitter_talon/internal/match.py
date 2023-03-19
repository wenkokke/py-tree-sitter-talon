import functools
import typing

import typing_extensions
from parsec import (
    ParseError,
    Parser,
    Value,
    eof,
    fail_with,
    many,
    many1,
    one_of,
    optional,
    try_choice,
)

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

AnyListValue = typing.Union[typing.List[str], typing.Dict[str, typing.Any]]


################################################################################
# Implement 'match' and 'find_command'
################################################################################


def find_command(
    self: TalonSourceFile,
    text: typing.Sequence[str],
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> typing.Optional[TalonCommandDeclaration]:
    parser = _to_parser(
        self, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
    )
    try:
        return parser.parse_strict(text)
    except ParseError:
        return None


setattr(TalonSourceFile, "find_command", find_command)


def match(
    self: typing.Union[TalonCommandDeclaration, AnyTalonRule],
    text: typing.Sequence[str],
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> bool:
    parser = _to_parser(
        self, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
    )
    try:
        parser.parse_strict(text)
        return True
    except ParseError:
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

if typing.TYPE_CHECKING:
    Matcher: typing_extensions.TypeAlias = Parser[None]
    Fetcher: typing_extensions.TypeAlias = Parser[TalonCommandDeclaration]
else:
    Matcher: typing_extensions.TypeAlias = Parser
    Fetcher: typing_extensions.TypeAlias = Parser


@typing.overload
def _to_parser(
    node: TalonSourceFile,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> Fetcher:
    ...


@typing.overload
def _to_parser(
    node: TalonDeclarations,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> Fetcher:
    ...


@typing.overload
def _to_parser(
    node: TalonCommandDeclaration,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> Fetcher:
    ...


@typing.overload
def _to_parser(
    node: AnyTalonRule,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> Matcher:
    ...


def _to_parser(
    node: typing.Union[
        TalonSourceFile, TalonDeclarations, TalonCommandDeclaration, AnyTalonRule
    ],
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyListValue]]
    ] = None,
) -> typing.Union[Matcher, Fetcher,]:
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
# Compile TalonSourceFile to Parser
################################################################################


def _TalonSourceFile_to_parser(
    self: TalonSourceFile,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Fetcher:
    buffer: typing.List[Parser] = []
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
        try_choice, buffer, fail_with(f"input does not match any command")
    )


################################################################################
# Compile TalonDeclarations to Parser
################################################################################


def _TalonDeclarations_to_parser(
    self: TalonDeclarations,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Fetcher:
    buffer: typing.List[Parser] = []
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
        try_choice, buffer, fail_with(f"input does not match any command")
    )


################################################################################
# Compile TalonCommandDeclaration to Parser
################################################################################


def _TalonCommandDeclaration_to_parser(
    self: TalonCommandDeclaration,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Fetcher:
    return _to_parser(
        self.rule, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
    ).result(self)


################################################################################
# Implement AnyTalonRule._to_parser
################################################################################


def _always() -> Matcher:
    def _always_parser(text: typing.Sequence[str], index: int) -> Value[None]:
        return Value.success(index, None)

    return Matcher(fn=_always_parser)


def _word(token: str) -> Matcher:
    def _word_parser(text: typing.Sequence[str], index: int) -> Value[None]:
        if text[index] == token:
            return Value.success(index + 1, None)
        else:
            # NOTE: `Value.failure` creates a value of type `Value[<nothing>]`
            return typing.cast(Value[None], Value.failure(index, str(token)))

    return Matcher(fn=_word_parser)


def _TalonCapture_to_parser(
    self: TalonCapture,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Matcher:
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Matcher:
    acc: typing.Optional[Parser] = None
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Matcher:
    if fullmatch:
        return eof()
    else:
        return _always()


def _TalonList_to_parser(
    self: TalonList,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Matcher:
    list_name = self.list_name.text
    if get_list:
        list_value = get_list(list_name)
        if isinstance(list_value, dict):
            list_value = list(list_value.keys())
        if isinstance(list_value, list):
            return one_of([item for item in list_value]).result(None)
    return _word(f"{{{list_name}}}").result(None)


def _TalonOptional_to_parser(
    self: TalonOptional,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Matcher:
    return optional(
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Matcher:
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Matcher:
    return many(
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Matcher:
    return many1(
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Matcher:
    acc: typing.Optional[Matcher] = None
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Matcher:
    acc: typing.Optional[Matcher] = None
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Matcher:
    if fullmatch:

        def start_anchor_parser(text: typing.Sequence[str], index: int) -> Value:
            if index == 0:
                return Value.success(index, None)
            else:
                return Value.failure(index, "should be start of the input")

        return Matcher(fn=start_anchor_parser)
    else:
        return _always()


def _TalonWord_to_parser(
    self: TalonWord,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> Matcher:
    return _word(self.text).result(None)
