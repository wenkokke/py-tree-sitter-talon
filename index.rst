-------------------------------------
Python bindings for Tree-Sitter Talon
-------------------------------------

.. module:: tree_sitter_talon

=====================
Tree-Sitter Instances
=====================

.. autodata:: language

.. autodata:: parser

=============================
Parsing and Converting to AST
=============================

.. autofunction:: parse

.. autofunction:: parse_file

.. autofunction:: from_tree_sitter

================================
Talon Abstract Syntax Tree Nodes
================================

All AST nodes inherit from the Node class.

.. autoclass:: Node

   .. _Node:

   Nodes store the following information the text and the start and end
   positions corresponding to this node in the source file, as well as the
   tree-sitter name for the node type:

   .. autoattribute:: text
   .. autoattribute:: start_position
   .. autoattribute:: end_position
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

Each explicit node in the tree-sitter grammar corresponds to a dataclass.

.. autoclass:: Action
   :members:

.. autoclass:: And
   :members:

.. autoclass:: ArgumentList
   :members:

.. autoclass:: Assignment
   :members:

.. autoclass:: BinaryOperator
   :members:

.. autoclass:: Block
   :members:

.. autoclass:: Capture
   :members:

.. autoclass:: Choice
   :members:

.. autoclass:: Command
   :members:

.. autoclass:: Comment
   :members:

.. autoclass:: Context
   :members:

.. autoclass:: Docstring
   :members:

.. autoclass:: EndAnchor
   :members:

.. autoclass:: Expression
   :members:

.. autoclass:: Float
   :members:

.. autoclass:: Identifier
   :members:

.. autoclass:: ImplicitString
   :members:

.. autoclass:: IncludeTag
   :members:

.. autoclass:: Integer
   :members:

.. autoclass:: Interpolation
   :members:

.. autoclass:: KeyAction
   :members:

.. autoclass:: List
   :members:

.. autoclass:: Match
   :members:

.. autoclass:: Not
   :members:

.. autoclass:: Number
   :members:

.. autoclass:: Operator
   :members:

.. autoclass:: Optional
   :members:

.. autoclass:: Or
   :members:

.. autoclass:: ParenthesizedExpression
   :members:

.. autoclass:: ParenthesizedRule
   :members:

.. autoclass:: RegexEscapeSequence
   :members:

.. autoclass:: Repeat
   :members:

.. autoclass:: Repeat1
   :members:

.. autoclass:: Rule
   :members:

.. autoclass:: Seq
   :members:

.. autoclass:: Settings
   :members:

.. autoclass:: SleepAction
   :members:

.. autoclass:: SourceFile
   :members:

.. autoclass:: StartAnchor
   :members:

.. autoclass:: String
   :members:

.. autoclass:: StringContent
   :members:

.. autoclass:: StringEscapeSequence
   :members:

.. autoclass:: Variable
   :members:

.. autoclass:: Word
   :members:

Finally, there is one additional dataclass for ERROR nodes.

.. autoclass:: ERROR
   :members:

=====================
Abstract Node Visitor
=====================

.. autoclass:: NodeVisitor
   :members:

=========================
Abstract Node Transformer
=========================

.. autotypevar:: Result
   :no-value:
   :no-type:

.. autoclass:: NodeTransformer
   :members:

========================================
Helper Classes
========================================

.. autoclass:: Point
