import functools
import typing

import parsec
import typing_extensions

typing_extensions.TypeAlias

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

################################################################################
# Export typing.List
################################################################################

__all__: typing.List[str] = [
    "AnyTalonRule",
    "ListValue",
    "find_command",
    "match",
]


################################################################################
# Definitions
################################################################################

AnyTalonRule: typing_extensions.TypeAlias = typing.Union[
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

ListValue = typing.Union[typing.List[str], typing.Dict[str, typing.Any]]


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
        typing.Callable[[str], typing.Optional[ListValue]]
    ] = None,
) -> typing.Optional[TalonCommandDeclaration]:
    parser = _TalonSourceFile_to_TalonCommandDeclarationMatcher(
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
        typing.Callable[[str], typing.Optional[ListValue]]
    ] = None,
) -> bool:
    try:
        matcher = _to_SequenceMatcher(
            self, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
        matcher.parse_strict(text)
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
# Generic '_to_SequenceMatcher'
################################################################################

# NOTE: The parsec library defines the types parsec.Parser and parsec.Value to
#       be generic _in the interface files_, but the runtime types don't extend
#       the Generic class, so we only supply the arguments when type checking.
if typing.TYPE_CHECKING:
    SequenceMatcher: typing_extensions.TypeAlias = parsec.Parser[
        typing.Optional[typing.NoReturn]
    ]
    SequenceMatcherValue: typing_extensions.TypeAlias = parsec.Value[
        typing.Optional[typing.NoReturn]
    ]
    TalonCommandDeclarationMatcher: typing_extensions.TypeAlias = parsec.Parser[
        TalonCommandDeclaration
    ]
    TalonCommandDeclarationMatcherValue: typing_extensions.TypeAlias = parsec.Value[
        TalonCommandDeclaration
    ]
else:
    SequenceMatcher: typing_extensions.TypeAlias = parsec.Parser
    SequenceMatcherValue: typing_extensions.TypeAlias = parsec.Value
    TalonCommandDeclarationMatcher: typing_extensions.TypeAlias = parsec.Parser
    TalonCommandDeclarationMatcherValue: typing_extensions.TypeAlias = parsec.Value


def _to_SequenceMatcher(
    node: typing.Union[TalonCommandDeclaration, AnyTalonRule],
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[
        typing.Callable[[str], typing.Optional[ListValue]]
    ] = None,
) -> SequenceMatcher:
    if isinstance(node, TalonCapture):
        return _TalonCapture_to_SequenceMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonCommandDeclaration):
        return _TalonCommandDeclaration_to_TalonCommandDeclarationMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        ).result(None)
    elif isinstance(node, TalonChoice):
        return _TalonChoice_to_SequenceMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonEndAnchor):
        return _TalonEndAnchor_to_SequenceMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonList):
        return _TalonList_to_SequenceMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonOptional):
        return _TalonOptional_to_SequenceMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonParenthesizedRule):
        return _TalonParenthesizedRule_to_SequenceMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonRepeat):
        return _TalonRepeat_to_SequenceMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonRepeat1):
        return _TalonRepeat1_to_SequenceMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonRule):
        return _TalonRule_to_SequenceMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonSeq):
        return _TalonSeq_to_SequenceMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonStartAnchor):
        return _TalonStartAnchor_to_SequenceMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )
    elif isinstance(node, TalonWord):
        return _TalonWord_to_SequenceMatcher(
            node, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
        )


################################################################################
# Compile TalonSourceFile to Parser
################################################################################


def _TalonSourceFile_to_TalonCommandDeclarationMatcher(
    self: TalonSourceFile,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> TalonCommandDeclarationMatcher:
    buffer: typing.List[TalonCommandDeclarationMatcher] = []
    for declarations in self.children:
        if isinstance(declarations, TalonDeclarations):
            buffer.append(
                _TalonDeclarations_to_TalonCommandDeclarationMatcher(
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


def _TalonDeclarations_to_TalonCommandDeclarationMatcher(
    self: TalonDeclarations,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> TalonCommandDeclarationMatcher:
    buffer: typing.List[TalonCommandDeclarationMatcher] = []
    for declaration in self.children:
        if isinstance(declaration, TalonCommandDeclaration):
            buffer.append(
                _TalonCommandDeclaration_to_TalonCommandDeclarationMatcher(
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


def _TalonCommandDeclaration_to_TalonCommandDeclarationMatcher(
    self: TalonCommandDeclaration,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> TalonCommandDeclarationMatcher:
    return _to_SequenceMatcher(
        self.rule, fullmatch=fullmatch, get_capture=get_capture, get_list=get_list
    ).result(self)


################################################################################
# Implement AnyTalonRule._to_SequenceMatcher
################################################################################


def _always() -> SequenceMatcher:
    def _always_parser(text: typing.Sequence[str], index: int) -> SequenceMatcherValue:
        return parsec.Value.success(index, None)

    return parsec.Parser(fn=_always_parser)


def _word(token: str) -> SequenceMatcher:
    def _word_parser(text: typing.Sequence[str], index: int) -> SequenceMatcherValue:
        try:
            if text[index] == token:
                return parsec.Value.success(index + 1, None)
        except IndexError:
            pass
        # NOTE: `Value.failure` creates a value of type `Value[<nothing>]`
        return typing.cast(
            SequenceMatcherValue, parsec.Value.failure(index, str(token))
        )

    return parsec.Parser(fn=_word_parser)


def _TalonCapture_to_SequenceMatcher(
    self: TalonCapture,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> SequenceMatcher:
    capture_name = self.capture_name.text
    if get_capture:
        capture = get_capture(capture_name)
        if capture:
            return _to_SequenceMatcher(
                capture, get_capture=get_capture, get_list=get_list
            )
    return _word(f"<{capture_name}>").result(None)


def _TalonChoice_to_SequenceMatcher(
    self: TalonChoice,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> SequenceMatcher:
    acc: typing.Optional[SequenceMatcher] = None
    for rule in reversed(self.children):
        if not isinstance(rule, TalonComment):
            parser = _to_SequenceMatcher(
                rule,
                fullmatch=fullmatch,
                get_capture=get_capture,
                get_list=get_list,
            )
            acc = parser ^ acc if acc else parser
    assert acc is not None
    return acc.result(None)


def _TalonEndAnchor_to_SequenceMatcher(
    self: TalonEndAnchor,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> SequenceMatcher:
    if fullmatch:
        return parsec.eof()
    else:
        return _always()


def _TalonList_to_SequenceMatcher(
    self: TalonList,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> SequenceMatcher:
    list_name = self.list_name.text
    if get_list:
        list_value = get_list(list_name)
        if isinstance(list_value, dict):
            list_value = list(list_value.keys())
        if isinstance(list_value, list):
            return parsec.one_of([item for item in list_value]).result(None)
    return _word(f"{{{list_name}}}").result(None)


def _TalonOptional_to_SequenceMatcher(
    self: TalonOptional,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> SequenceMatcher:
    return parsec.optional(
        _to_SequenceMatcher(
            self.get_child(),
            fullmatch=fullmatch,
            get_capture=get_capture,
            get_list=get_list,
        )
    ).result(None)


def _TalonParenthesizedRule_to_SequenceMatcher(
    self: TalonParenthesizedRule,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> SequenceMatcher:
    return _to_SequenceMatcher(
        self.get_child(),
        fullmatch=fullmatch,
        get_capture=get_capture,
        get_list=get_list,
    ).result(None)


def _TalonRepeat_to_SequenceMatcher(
    self: TalonRepeat,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> SequenceMatcher:
    return parsec.many(
        _to_SequenceMatcher(
            self.get_child(),
            fullmatch=fullmatch,
            get_capture=get_capture,
            get_list=get_list,
        )
    ).result(None)


def _TalonRepeat1_to_SequenceMatcher(
    self: TalonRepeat1,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> SequenceMatcher:
    return parsec.many1(
        _to_SequenceMatcher(
            self.get_child(),
            fullmatch=fullmatch,
            get_capture=get_capture,
            get_list=get_list,
        )
    ).result(None)


def _TalonRule_to_SequenceMatcher(
    self: TalonRule,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> SequenceMatcher:
    acc: typing.Optional[SequenceMatcher] = None
    for rule in reversed(self.children):
        if not isinstance(rule, TalonComment):
            parser = _to_SequenceMatcher(
                rule,
                fullmatch=fullmatch,
                get_capture=get_capture,
                get_list=get_list,
            )
            acc = (parser >> acc) if acc else parser
    assert acc is not None
    return acc.result(None)


def _TalonSeq_to_SequenceMatcher(
    self: TalonSeq,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> SequenceMatcher:
    acc: typing.Optional[SequenceMatcher] = None
    for rule in reversed(self.children):
        if not isinstance(rule, TalonComment):
            parser = _to_SequenceMatcher(
                rule,
                fullmatch=fullmatch,
                get_capture=get_capture,
                get_list=get_list,
            )
            acc = parser > acc if acc else parser
    assert acc is not None
    return acc.result(None)


def _TalonStartAnchor_to_SequenceMatcher(
    self: TalonStartAnchor,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> SequenceMatcher:
    if fullmatch:

        def start_anchor_parser(
            text: typing.Sequence[str], index: int
        ) -> SequenceMatcherValue:
            if index == 0:
                return parsec.Value.success(index, None)
            else:
                return typing.cast(
                    SequenceMatcherValue,
                    parsec.Value.failure(index, "should be start of the input"),
                )

        return SequenceMatcher(fn=start_anchor_parser)
    else:
        return _always()


def _TalonWord_to_SequenceMatcher(
    self: TalonWord,
    *,
    fullmatch: bool = False,
    get_capture: typing.Optional[
        typing.Callable[[str], typing.Optional[AnyTalonRule]]
    ] = None,
    get_list: typing.Optional[typing.Callable[[str], typing.Optional[ListValue]]],
) -> SequenceMatcher:
    return _word(self.text).result(None)
