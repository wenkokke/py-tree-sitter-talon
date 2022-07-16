from dataclasses import dataclass
from pathlib import Path
from typing import Generic, Dict, Sequence, TypeVar
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
) -> Sequence[Node] | Node | None: ...

@dataclass
class ERROR(Node):

    children: Sequence[Sequence[Node] | Node | None] = ...

@dataclass
class Action(Node):

    action_name: "Identifier"
    arguments: "ArgumentList"

@dataclass
class And(Node):

    children: Sequence["And" | "Match" | "Not"]

@dataclass
class ArgumentList(Node):

    children: Sequence[
        "Action"
        | "BinaryOperator"
        | "Float"
        | "Integer"
        | "KeyAction"
        | "ParenthesizedExpression"
        | "SleepAction"
        | "String"
        | "Variable"
    ]

@dataclass
class Assignment(Node):

    left: "Identifier"
    right: "Action" | "BinaryOperator" | "Float" | "Integer" | "KeyAction" | "ParenthesizedExpression" | "SleepAction" | "String" | "Variable"

@dataclass
class BinaryOperator(Node):

    left: "Action" | "BinaryOperator" | "Float" | "Integer" | "KeyAction" | "ParenthesizedExpression" | "SleepAction" | "String" | "Variable"
    operator: "Operator"
    right: "Action" | "BinaryOperator" | "Float" | "Integer" | "KeyAction" | "ParenthesizedExpression" | "SleepAction" | "String" | "Variable"

@dataclass
class Block(Node):

    children: Sequence["Assignment" | "Docstring" | "Expression"]

@dataclass
class Capture(Node):

    capture_name: "Identifier"

@dataclass
class Choice(Node):

    children: Sequence[
        "Capture"
        | "EndAnchor"
        | "List"
        | "Optional"
        | "ParenthesizedRule"
        | "Repeat"
        | "Repeat1"
        | "Seq"
        | "StartAnchor"
        | "Word"
    ]

@dataclass
class Command(Node):

    rule: "Rule"
    script: "Block"

@dataclass
class Comment(Node):
    pass

@dataclass
class Context(Node):

    children: Sequence["And" | "Docstring" | "Match" | "Not" | "Or"]

@dataclass
class Docstring(Node):
    pass

@dataclass
class EndAnchor(Node):
    pass

@dataclass
class Expression(Node):

    expression: "Action" | "BinaryOperator" | "Float" | "Integer" | "KeyAction" | "ParenthesizedExpression" | "SleepAction" | "String" | "Variable"

@dataclass
class Float(Node):
    pass

@dataclass
class Identifier(Node):
    pass

@dataclass
class ImplicitString(Node):
    pass

@dataclass
class IncludeTag(Node):

    tag: "Identifier"

@dataclass
class Integer(Node):
    pass

@dataclass
class Interpolation(Node):

    children: "Action" | "BinaryOperator" | "Float" | "Integer" | "KeyAction" | "ParenthesizedExpression" | "SleepAction" | "String" | "Variable"

@dataclass
class KeyAction(Node):

    arguments: "ImplicitString"

@dataclass
class List(Node):

    list_name: "Identifier"

@dataclass
class Match(Node):

    key: "Identifier"
    pattern: "ImplicitString"

@dataclass
class Not(Node):

    children: "Match"

@dataclass
class Number(Node):

    children: "Float" | "Integer"

@dataclass
class Operator(Node):
    pass

@dataclass
class Optional(Node):

    children: Sequence[
        "Capture"
        | "Choice"
        | "EndAnchor"
        | "List"
        | "Optional"
        | "ParenthesizedRule"
        | "Repeat"
        | "Repeat1"
        | "Seq"
        | "StartAnchor"
        | "Word"
    ]

@dataclass
class Or(Node):

    children: Sequence["And" | "Match" | "Not"]

@dataclass
class ParenthesizedExpression(Node):

    children: "Action" | "BinaryOperator" | "Float" | "Integer" | "KeyAction" | "ParenthesizedExpression" | "SleepAction" | "String" | "Variable"

@dataclass
class ParenthesizedRule(Node):

    children: Sequence[
        "Choice"
        | "EndAnchor"
        | "List"
        | "Optional"
        | "ParenthesizedRule"
        | "Repeat"
        | "Repeat1"
        | "Seq"
        | "StartAnchor"
        | "Word"
    ]

@dataclass
class RegexEscapeSequence(Node):

    children: "RegexEscapeSequence" | None

@dataclass
class Repeat(Node):

    children: "Capture" | "List" | "Optional" | "ParenthesizedRule" | "Repeat" | "Repeat1" | "Word"

@dataclass
class Repeat1(Node):

    children: "Capture" | "List" | "Optional" | "ParenthesizedRule" | "Repeat" | "Repeat1" | "Word"

@dataclass
class Rule(Node):

    children: Sequence[
        "Capture"
        | "Choice"
        | "EndAnchor"
        | "List"
        | "Optional"
        | "ParenthesizedRule"
        | "Repeat"
        | "Repeat1"
        | "Seq"
        | "StartAnchor"
        | "Word"
    ]

@dataclass
class Seq(Node):

    children: Sequence[
        "Capture"
        | "List"
        | "Optional"
        | "ParenthesizedRule"
        | "Repeat"
        | "Repeat1"
        | "Word"
    ]

@dataclass
class Settings(Node):

    children: "Block"

@dataclass
class SleepAction(Node):

    arguments: "ImplicitString"

@dataclass
class SourceFile(Node):

    children: Sequence["Command" | "Context" | "IncludeTag" | "Settings"]

@dataclass
class StartAnchor(Node):
    pass

@dataclass
class String(Node):

    children: Sequence["Interpolation" | "StringContent" | "StringEscapeSequence"]

@dataclass
class StringContent(Node):
    pass

@dataclass
class StringEscapeSequence(Node):
    pass

@dataclass
class Variable(Node):
    variable_name: "Identifier"

@dataclass
class Word(Node):
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
    def generic_transform(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform(self, node: Node) -> Result: ...
    def transform_Action(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_And(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_ArgumentList(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Assignment(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_BinaryOperator(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Block(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Capture(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Choice(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Command(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Comment(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Context(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Docstring(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_ERROR(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_EndAnchor(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Expression(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Float(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Identifier(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_ImplicitString(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_IncludeTag(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Integer(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Interpolation(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_KeyAction(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_List(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Match(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Not(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Number(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Operator(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Optional(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Or(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_ParenthesizedExpression(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_ParenthesizedRule(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_RegexEscapeSequence(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Repeat(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Repeat1(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Rule(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Seq(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Settings(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_SleepAction(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_SourceFile(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_StartAnchor(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_String(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_StringContent(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_StringEscapeSequence(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Variable(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
    def transform_Word(
        self,
        *,
        text: str,
        type: str,
        children: Sequence[Result] = [],
        **kwargs: Dict[str, Result | Sequence[Node] | Node | None]
    ) -> Result: ...
