from dataclasses import dataclass
from pathlib import Path
from typing import Generic, TypeVar
from tree_sitter_type_provider import Node as Node, Point as Point

import tree_sitter as ts  # type: ignore

parser: ts.Parser

language: ts.Language

def parse(
    contents: str | bytes,
    has_header: bool | None = None,
    encoding: str = "utf-8",
) -> Node: ...
def parse_file(
    path: str | Path,
    has_header: bool | None = None,
    encoding: str = "utf-8",
) -> Node: ...
def parse_as_tree_sitter(
    contents: str | bytes,
    has_header: bool | None = None,
    encoding: str = "utf-8",
) -> ts.Tree: ...
def parse_file_as_tree_sitter(
    path: str | Path,
    has_header: bool | None = None,
    encoding: str = "utf-8",
) -> ts.Tree: ...
def from_tree_sitter(
    tsnode: ts.Node, encoding: str = "utf-8"
) -> list[Node] | Node | None: ...
@dataclass
class TalonAction(Node):

    action_name: "TalonIdentifier"
    arguments: "TalonArgumentList"

@dataclass
class TalonAnd(Node):

    children: list["TalonAnd" | "TalonMatch" | "TalonNot"]

@dataclass
class TalonArgumentList(Node):

    children: list[
        "TalonAction"
        | "TalonBinaryOperator"
        | "TalonFloat"
        | "TalonInteger"
        | "TalonKeyAction"
        | "TalonParenthesizedExpression"
        | "TalonSleepAction"
        | "TalonString"
        | "TalonVariable"
    ]

@dataclass
class TalonAssignment(Node):

    left: "TalonIdentifier"
    right: "TalonAction" | "TalonBinaryOperator" | "TalonFloat" | "TalonInteger" | "TalonKeyAction" | "TalonParenthesizedExpression" | "TalonSleepAction" | "TalonString" | "TalonVariable"

@dataclass
class TalonBinaryOperator(Node):

    left: "TalonAction" | "TalonBinaryOperator" | "TalonFloat" | "TalonInteger" | "TalonKeyAction" | "TalonParenthesizedExpression" | "TalonSleepAction" | "TalonString" | "TalonVariable"
    operator: "TalonOperator"
    right: "TalonAction" | "TalonBinaryOperator" | "TalonFloat" | "TalonInteger" | "TalonKeyAction" | "TalonParenthesizedExpression" | "TalonSleepAction" | "TalonString" | "TalonVariable"

@dataclass
class TalonBlock(Node):

    children: list["TalonAssignment" | "TalonDocstring" | "TalonExpression"]

@dataclass
class TalonCapture(Node):

    capture_name: "TalonIdentifier"

@dataclass
class TalonChoice(Node):

    children: list[
        "TalonCapture"
        | "TalonEndAnchor"
        | "TalonList"
        | "TalonOptional"
        | "TalonParenthesizedRule"
        | "TalonRepeat"
        | "TalonRepeat1"
        | "TalonSeq"
        | "TalonStartAnchor"
        | "TalonWord"
    ]

@dataclass
class TalonCommand(Node):

    rule: "TalonRule"
    script: "TalonBlock"

@dataclass
class TalonComment(Node):
    pass

@dataclass
class TalonContext(Node):

    children: list[
        "TalonAnd" | "TalonDocstring" | "TalonMatch" | "TalonNot" | "TalonOr"
    ]

@dataclass
class TalonDocstring(Node):
    pass

@dataclass
class ERROR(Node):

    children: list[list[Node] | Node | None] = ...

@dataclass
class TalonEndAnchor(Node):
    pass

@dataclass
class TalonExpression(Node):

    expression: "TalonAction" | "TalonBinaryOperator" | "TalonFloat" | "TalonInteger" | "TalonKeyAction" | "TalonParenthesizedExpression" | "TalonSleepAction" | "TalonString" | "TalonVariable"

@dataclass
class TalonFloat(Node):
    pass

@dataclass
class TalonIdentifier(Node):
    pass

@dataclass
class TalonImplicitString(Node):
    pass

@dataclass
class TalonIncludeTag(Node):

    tag: "TalonIdentifier"

@dataclass
class TalonInteger(Node):
    pass

@dataclass
class TalonInterpolation(Node):

    children: "TalonAction" | "TalonBinaryOperator" | "TalonFloat" | "TalonInteger" | "TalonKeyAction" | "TalonParenthesizedExpression" | "TalonSleepAction" | "TalonString" | "TalonVariable"

@dataclass
class TalonKeyAction(Node):

    arguments: "TalonImplicitString"

@dataclass
class TalonList(Node):

    list_name: "TalonIdentifier"

@dataclass
class TalonMatch(Node):

    key: "TalonIdentifier"
    pattern: "TalonImplicitString"

@dataclass
class TalonNot(Node):

    children: "TalonMatch"

@dataclass
class TalonNumber(Node):

    children: "TalonFloat" | "TalonInteger"

@dataclass
class TalonOperator(Node):
    pass

@dataclass
class TalonOptional(Node):

    children: list[
        "TalonCapture"
        | "TalonChoice"
        | "TalonEndAnchor"
        | "TalonList"
        | "TalonOptional"
        | "TalonParenthesizedRule"
        | "TalonRepeat"
        | "TalonRepeat1"
        | "TalonSeq"
        | "TalonStartAnchor"
        | "TalonWord"
    ]

@dataclass
class TalonOr(Node):

    children: list["TalonAnd" | "TalonMatch" | "TalonNot"]

@dataclass
class TalonParenthesizedExpression(Node):

    children: "TalonAction" | "TalonBinaryOperator" | "TalonFloat" | "TalonInteger" | "TalonKeyAction" | "TalonParenthesizedExpression" | "TalonSleepAction" | "TalonString" | "TalonVariable"

@dataclass
class TalonParenthesizedRule(Node):

    children: list[
        "TalonChoice"
        | "TalonEndAnchor"
        | "TalonList"
        | "TalonOptional"
        | "TalonParenthesizedRule"
        | "TalonRepeat"
        | "TalonRepeat1"
        | "TalonSeq"
        | "TalonStartAnchor"
        | "TalonWord"
    ]

@dataclass
class TalonRegexEscapeSequence(Node):

    children: "TalonRegexEscapeSequence" | None

@dataclass
class TalonRepeat(Node):

    children: "TalonCapture" | "TalonList" | "TalonOptional" | "TalonParenthesizedRule" | "TalonRepeat" | "TalonRepeat1" | "TalonWord"

@dataclass
class TalonRepeat1(Node):

    children: "TalonCapture" | "TalonList" | "TalonOptional" | "TalonParenthesizedRule" | "TalonRepeat" | "TalonRepeat1" | "TalonWord"

@dataclass
class TalonRule(Node):

    children: list[
        "TalonCapture"
        | "TalonChoice"
        | "TalonEndAnchor"
        | "TalonList"
        | "TalonOptional"
        | "TalonParenthesizedRule"
        | "TalonRepeat"
        | "TalonRepeat1"
        | "TalonSeq"
        | "TalonStartAnchor"
        | "TalonWord"
    ]

@dataclass
class TalonSeq(Node):

    children: list[
        "TalonCapture"
        | "TalonList"
        | "TalonOptional"
        | "TalonParenthesizedRule"
        | "TalonRepeat"
        | "TalonRepeat1"
        | "TalonWord"
    ]

@dataclass
class TalonSettings(Node):

    children: "TalonBlock"

@dataclass
class TalonSleepAction(Node):

    arguments: "TalonImplicitString"

@dataclass
class TalonSourceFile(Node):

    children: list[
        "TalonCommand" | "TalonContext" | "TalonIncludeTag" | "TalonSettings"
    ]

@dataclass
class TalonStartAnchor(Node):
    pass

@dataclass
class TalonString(Node):

    children: list[
        "TalonInterpolation" | "TalonStringContent" | "TalonStringEscapeSequence"
    ]

@dataclass
class TalonStringContent(Node):
    pass

@dataclass
class TalonStringEscapeSequence(Node):
    pass

@dataclass
class TalonVariable(Node):
    variable_name: "TalonIdentifier"

@dataclass
class TalonWord(Node):
    pass

class NodeVisitor(object):
    def generic_visit(self, node: Node) -> None: ...
    def visit(self, node: Node) -> None: ...
    def visit_Action(self, node: Node) -> None: ...
    def visit_And(self, node: Node) -> None: ...
    def visit_ArgumentList(self, node: Node) -> None: ...
    def visit_Assignment(self, node: Node) -> None: ...
    def visit_BinaryOperator(self, node: Node) -> None: ...
    def visit_Block(self, node: Node) -> None: ...
    def visit_Capture(self, node: Node) -> None: ...
    def visit_Choice(self, node: Node) -> None: ...
    def visit_Command(self, node: Node) -> None: ...
    def visit_Comment(self, node: Node) -> None: ...
    def visit_Context(self, node: Node) -> None: ...
    def visit_Docstring(self, node: Node) -> None: ...
    def visit_ERROR(self, node: Node) -> None: ...
    def visit_EndAnchor(self, node: Node) -> None: ...
    def visit_Expression(self, node: Node) -> None: ...
    def visit_Float(self, node: Node) -> None: ...
    def visit_Identifier(self, node: Node) -> None: ...
    def visit_ImplicitString(self, node: Node) -> None: ...
    def visit_IncludeTag(self, node: Node) -> None: ...
    def visit_Integer(self, node: Node) -> None: ...
    def visit_Interpolation(self, node: Node) -> None: ...
    def visit_KeyAction(self, node: Node) -> None: ...
    def visit_List(self, node: Node) -> None: ...
    def visit_Match(self, node: Node) -> None: ...
    def visit_Not(self, node: Node) -> None: ...
    def visit_Number(self, node: Node) -> None: ...
    def visit_Operator(self, node: Node) -> None: ...
    def visit_Optional(self, node: Node) -> None: ...
    def visit_Or(self, node: Node) -> None: ...
    def visit_ParenthesizedExpression(self, node: Node) -> None: ...
    def visit_ParenthesizedRule(self, node: Node) -> None: ...
    def visit_RegexEscapeSequence(self, node: Node) -> None: ...
    def visit_Repeat(self, node: Node) -> None: ...
    def visit_Repeat1(self, node: Node) -> None: ...
    def visit_Rule(self, node: Node) -> None: ...
    def visit_Seq(self, node: Node) -> None: ...
    def visit_Settings(self, node: Node) -> None: ...
    def visit_SleepAction(self, node: Node) -> None: ...
    def visit_SourceFile(self, node: Node) -> None: ...
    def visit_StartAnchor(self, node: Node) -> None: ...
    def visit_String(self, node: Node) -> None: ...
    def visit_StringContent(self, node: Node) -> None: ...
    def visit_StringEscapeSequence(self, node: Node) -> None: ...
    def visit_Variable(self, node: Node) -> None: ...
    def visit_Word(self, node: Node) -> None: ...

Result = TypeVar("Result")

class NodeTransformer(Generic[Result]):
    def transform(self, node: Node) -> Result: ...
    def transform_Action(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        action_name: Result,
        arguments: Result,
        action_name_hist: "TalonIdentifier",
        arguments_hist: "TalonArgumentList",
    ) -> Result: ...
    def transform_And(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list["TalonAnd" | "TalonMatch" | "TalonNot"],
    ) -> Result: ...
    def transform_ArgumentList(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list[
            "TalonAction"
            | "TalonBinaryOperator"
            | "TalonFloat"
            | "TalonInteger"
            | "TalonKeyAction"
            | "TalonParenthesizedExpression"
            | "TalonSleepAction"
            | "TalonString"
            | "TalonVariable"
        ],
    ) -> Result: ...
    def transform_Assignment(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        left: Result,
        right: Result,
        left_hist: "TalonIdentifier",
        right_hist: "TalonAction"
        | "TalonBinaryOperator"
        | "TalonFloat"
        | "TalonInteger"
        | "TalonKeyAction"
        | "TalonParenthesizedExpression"
        | "TalonSleepAction"
        | "TalonString"
        | "TalonVariable",
    ) -> Result: ...
    def transform_BinaryOperator(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        left: Result,
        operator: Result,
        right: Result,
        left_hist: "TalonAction"
        | "TalonBinaryOperator"
        | "TalonFloat"
        | "TalonInteger"
        | "TalonKeyAction"
        | "TalonParenthesizedExpression"
        | "TalonSleepAction"
        | "TalonString"
        | "TalonVariable",
        operator_hist: "TalonOperator",
        right_hist: "TalonAction"
        | "TalonBinaryOperator"
        | "TalonFloat"
        | "TalonInteger"
        | "TalonKeyAction"
        | "TalonParenthesizedExpression"
        | "TalonSleepAction"
        | "TalonString"
        | "TalonVariable",
    ) -> Result: ...
    def transform_Block(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list["TalonAssignment" | "TalonDocstring" | "TalonExpression"],
    ) -> Result: ...
    def transform_Capture(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        capture_name: Result,
        capture_name_hist: "TalonIdentifier",
    ) -> Result: ...
    def transform_Choice(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list[
            "TalonCapture"
            | "TalonEndAnchor"
            | "TalonList"
            | "TalonOptional"
            | "TalonParenthesizedRule"
            | "TalonRepeat"
            | "TalonRepeat1"
            | "TalonSeq"
            | "TalonStartAnchor"
            | "TalonWord"
        ],
    ) -> Result: ...
    def transform_Command(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        rule: Result,
        script: Result,
        rule_hist: "TalonRule",
        script_hist: "TalonBlock",
    ) -> Result: ...
    def transform_Comment(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
    ) -> Result: ...
    def transform_Context(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list[
            "TalonAnd" | "TalonDocstring" | "TalonMatch" | "TalonNot" | "TalonOr"
        ],
    ) -> Result: ...
    def transform_Docstring(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
    ) -> Result: ...
    def transform_ERROR(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list[list[Node] | Node | None],
    ) -> Result: ...
    def transform_EndAnchor(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
    ) -> Result: ...
    def transform_Expression(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        expression: Result,
        expression_hist: "TalonAction"
        | "TalonBinaryOperator"
        | "TalonFloat"
        | "TalonInteger"
        | "TalonKeyAction"
        | "TalonParenthesizedExpression"
        | "TalonSleepAction"
        | "TalonString"
        | "TalonVariable",
    ) -> Result: ...
    def transform_Float(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
    ) -> Result: ...
    def transform_Identifier(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
    ) -> Result: ...
    def transform_ImplicitString(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
    ) -> Result: ...
    def transform_IncludeTag(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        tag: Result,
        tag_hist: "TalonIdentifier",
    ) -> Result: ...
    def transform_Integer(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
    ) -> Result: ...
    def transform_Interpolation(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: Result,
        children_hist: "TalonAction"
        | "TalonBinaryOperator"
        | "TalonFloat"
        | "TalonInteger"
        | "TalonKeyAction"
        | "TalonParenthesizedExpression"
        | "TalonSleepAction"
        | "TalonString"
        | "TalonVariable",
    ) -> Result: ...
    def transform_KeyAction(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        arguments: Result,
        arguments_hist: "TalonImplicitString",
    ) -> Result: ...
    def transform_List(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        list_name: Result,
        list_name_hist: "TalonIdentifier",
    ) -> Result: ...
    def transform_Match(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        key: Result,
        pattern: Result,
        key_hist: "TalonIdentifier",
        pattern_hist: "TalonImplicitString",
    ) -> Result: ...
    def transform_Not(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: Result,
        children_hist: "TalonMatch",
    ) -> Result: ...
    def transform_Number(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: Result,
        children_hist: "TalonFloat" | "TalonInteger",
    ) -> Result: ...
    def transform_Operator(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
    ) -> Result: ...
    def transform_Optional(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list[
            "TalonCapture"
            | "TalonChoice"
            | "TalonEndAnchor"
            | "TalonList"
            | "TalonOptional"
            | "TalonParenthesizedRule"
            | "TalonRepeat"
            | "TalonRepeat1"
            | "TalonSeq"
            | "TalonStartAnchor"
            | "TalonWord"
        ],
    ) -> Result: ...
    def transform_Or(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list["TalonAnd" | "TalonMatch" | "TalonNot"],
    ) -> Result: ...
    def transform_ParenthesizedExpression(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: Result,
        children_hist: "TalonAction"
        | "TalonBinaryOperator"
        | "TalonFloat"
        | "TalonInteger"
        | "TalonKeyAction"
        | "TalonParenthesizedExpression"
        | "TalonSleepAction"
        | "TalonString"
        | "TalonVariable",
    ) -> Result: ...
    def transform_ParenthesizedRule(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list[
            "TalonChoice"
            | "TalonEndAnchor"
            | "TalonList"
            | "TalonOptional"
            | "TalonParenthesizedRule"
            | "TalonRepeat"
            | "TalonRepeat1"
            | "TalonSeq"
            | "TalonStartAnchor"
            | "TalonWord"
        ],
    ) -> Result: ...
    def transform_RegexEscapeSequence(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: Result,
        children_hist: "TalonRegexEscapeSequence" | None,
    ) -> Result: ...
    def transform_Repeat(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: Result,
        children_hist: "TalonCapture"
        | "TalonList"
        | "TalonOptional"
        | "TalonParenthesizedRule"
        | "TalonRepeat"
        | "TalonRepeat1"
        | "TalonWord",
    ) -> Result: ...
    def transform_Repeat1(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: Result,
        children_hist: "TalonCapture"
        | "TalonList"
        | "TalonOptional"
        | "TalonParenthesizedRule"
        | "TalonRepeat"
        | "TalonRepeat1"
        | "TalonWord",
    ) -> Result: ...
    def transform_Rule(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list[
            "TalonCapture"
            | "TalonChoice"
            | "TalonEndAnchor"
            | "TalonList"
            | "TalonOptional"
            | "TalonParenthesizedRule"
            | "TalonRepeat"
            | "TalonRepeat1"
            | "TalonSeq"
            | "TalonStartAnchor"
            | "TalonWord"
        ],
    ) -> Result: ...
    def transform_Seq(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list[
            "TalonCapture"
            | "TalonList"
            | "TalonOptional"
            | "TalonParenthesizedRule"
            | "TalonRepeat"
            | "TalonRepeat1"
            | "TalonWord"
        ],
    ) -> Result: ...
    def transform_Settings(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: Result,
        children_hist: "TalonBlock",
    ) -> Result: ...
    def transform_SleepAction(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        arguments: Result,
        arguments_hist: "TalonImplicitString",
    ) -> Result: ...
    def transform_SourceFile(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list[
            "TalonCommand" | "TalonContext" | "TalonIncludeTag" | "TalonSettings"
        ],
    ) -> Result: ...
    def transform_StartAnchor(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
    ) -> Result: ...
    def transform_String(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        children: list[Result],
        children_hist: list[
            "TalonInterpolation" | "TalonStringContent" | "TalonStringEscapeSequence"
        ],
    ) -> Result: ...
    def transform_StringContent(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
    ) -> Result: ...
    def transform_StringEscapeSequence(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
    ) -> Result: ...
    def transform_Variable(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
        variable_name: Result,
        variable_name_hist: "TalonIdentifier",
    ) -> Result: ...
    def transform_Word(
        self,
        *,
        text: str,
        type_name: str,
        start_position: Point,
        end_position: Point,
    ) -> Result: ...
