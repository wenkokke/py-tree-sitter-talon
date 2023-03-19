import functools
import typing

import parsec
import typing_extensions

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
    except parsec.ParseError:
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

if typing.TYPE_CHECKING:
    SequenceMatcher: typing_extensions.TypeAlias = parsec.Parser[None]
    TalonCommandDeclarationMatcher: typing_extensions.TypeAlias = parsec.Parser[
        TalonCommandDeclaration
    ]
else:
    SequenceMatcher: typing_extensions.TypeAlias = parsec.Parser
    TalonCommandDeclarationMatcher: typing_extensions.TypeAlias = parsec.Parser


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
) -> TalonCommandDeclarationMatcher:
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
) -> TalonCommandDeclarationMatcher:
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
) -> TalonCommandDeclarationMatcher:
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
) -> SequenceMatcher:
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
) -> typing.Union[SequenceMatcher, TalonCommandDeclarationMatcher]:
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
) -> TalonCommandDeclarationMatcher:
    buffer: typing.List[parsec.Parser] = []
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
) -> TalonCommandDeclarationMatcher:
    buffer: typing.List[parsec.Parser] = []
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
) -> TalonCommandDeclarationMatcher:
    return _to_parser(
        self.rule, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
    ).result(self)


################################################################################
# Implement AnyTalonRule._to_parser
################################################################################


def _always() -> SequenceMatcher:
    def _always_parser(text: typing.Sequence[str], index: int):
        return parsec.Value.success(index, None)

    return SequenceMatcher(fn=_always_parser)


def _word(token: str) -> SequenceMatcher:
    def _word_parser(text: typing.Sequence[str], index: int):
        if text[index] == token:
            return parsec.Value.success(index + 1, None)
        else:
            # NOTE: `Value.failure` creates a value of type `Value[<nothing>]`
            return parsec.Value.failure(index, str(token))

    return SequenceMatcher(fn=_word_parser)


def _TalonCapture_to_parser(
    self: TalonCapture,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> SequenceMatcher:
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
) -> SequenceMatcher:
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> SequenceMatcher:
    if fullmatch:
        return parsec.eof()
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
) -> SequenceMatcher:
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> SequenceMatcher:
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> SequenceMatcher:
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
) -> SequenceMatcher:
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> SequenceMatcher:
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
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[AnyListValue]]],
) -> SequenceMatcher:
    acc: typing.Optional[SequenceMatcher] = None
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
) -> SequenceMatcher:
    acc: typing.Optional[SequenceMatcher] = None
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
) -> SequenceMatcher:
    if fullmatch:

        def start_anchor_parser(text: typing.Sequence[str], index: int):
            if index == 0:
                return parsec.Value.success(index, None)
            else:
                return parsec.Value.failure(index, "should be start of the input")

        return SequenceMatcher(fn=start_anchor_parser)
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
) -> SequenceMatcher:
    return _word(self.text).result(None)
