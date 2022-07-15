tree_sitter_talon
=================

=====================
Tree-Sitter Instances
=====================

.. autodata:: tree_sitter_talon::language

.. autodata:: tree_sitter_talon::parser

=============================
Parsing and Converting to AST
=============================

.. autofunction:: tree_sitter_talon::parse

.. autofunction:: tree_sitter_talon::parse_file

.. autofunction:: tree_sitter_talon::from_tree_sitter

================================
Talon Abstract Syntax Tree Nodes
================================

Abstract type for all AST nodes.

.. autoclass:: tree_sitter_talon::Node

   Each node stores the text it corresponds to, as well as its node type.

   .. autoattribute:: text
   .. autoattribute:: type

   Nodes can be converted to and from JSON.

   .. automethod:: to_json
   .. automethod:: from_json

   Nodes can be converted to and from a Python dictionary.

   .. automethod:: to_dict
   .. automethod:: from_dict

   Nodes types are associated with a JSON schema, which can be used,
   amongst other things, to load multiple nodes from a file.

   .. code-block::

      source_files: List[SourceFile] = (
         SourceFile.schema().loads(json, many=True)
      )

   .. automethod:: schema



Concrete types for AST nodes.

.. autoclass:: tree_sitter_talon::ERROR
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Action
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::And
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::ArgumentList
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Assignment
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::BinaryOperator
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Block
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Capture
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Choice
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Command
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Comment
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Context
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Docstring
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::EndAnchor
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Expression
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Float
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Identifier
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::ImplicitString
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::IncludeTag
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Integer
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Interpolation
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::KeyAction
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::List
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Match
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Not
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Number
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Operator
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Optional
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Or
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::ParenthesizedExpression
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::ParenthesizedRule
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::RegexEscapeSequence
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Repeat
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Repeat1
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Rule
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Seq
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Settings
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::SleepAction
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::SourceFile
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::StartAnchor
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::String
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::StringContent
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::StringEscapeSequence
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Variable
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::Word
   :members:
   :undoc-members:

========================================
Abstract Visitor and Transformer Classes
========================================

.. autoclass:: tree_sitter_talon::NodeVisitor
   :members:
   :undoc-members:

.. autoclass:: tree_sitter_talon::NodeTransformer
   :members:
   :undoc-members:
