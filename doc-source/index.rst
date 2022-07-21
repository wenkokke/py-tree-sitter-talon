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
   .. autoattribute:: type_name

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

.. autoclass:: TalonAction
   :members:

.. autoclass:: TalonAnd
   :members:

.. autoclass:: TalonArgumentList
   :members:

.. autoclass:: TalonAssignment
   :members:

.. autoclass:: TalonBinaryOperator
   :members:

.. autoclass:: TalonBlock
   :members:

.. autoclass:: TalonCapture
   :members:

.. autoclass:: TalonChoice
   :members:

.. autoclass:: TalonCommand
   :members:

.. autoclass:: TalonComment
   :members:

.. autoclass:: TalonContext
   :members:

.. autoclass:: TalonDocstring
   :members:

.. autoclass:: TalonEndAnchor
   :members:

.. autoclass:: TalonExpression
   :members:

.. autoclass:: TalonFloat
   :members:

.. autoclass:: TalonIdentifier
   :members:

.. autoclass:: TalonImplicitString
   :members:

.. autoclass:: TalonIncludeTag
   :members:

.. autoclass:: TalonInteger
   :members:

.. autoclass:: TalonInterpolation
   :members:

.. autoclass:: TalonKeyAction
   :members:

.. autoclass:: TalonList
   :members:

.. autoclass:: TalonMatch
   :members:

.. autoclass:: TalonNot
   :members:

.. autoclass:: TalonNumber
   :members:

.. autoclass:: TalonOperator
   :members:

.. autoclass:: TalonOptional
   :members:

.. autoclass:: TalonOr
   :members:

.. autoclass:: TalonParenthesizedExpression
   :members:

.. autoclass:: TalonParenthesizedRule
   :members:

.. autoclass:: TalonRegexEscapeSequence
   :members:

.. autoclass:: TalonRepeat
   :members:

.. autoclass:: TalonRepeat1
   :members:

.. autoclass:: TalonRule
   :members:

.. autoclass:: TalonSeq
   :members:

.. autoclass:: TalonSettings
   :members:

.. autoclass:: TalonSleepAction
   :members:

.. autoclass:: TalonSourceFile
   :members:

.. autoclass:: TalonStartAnchor
   :members:

.. autoclass:: TalonString
   :members:

.. autoclass:: TalonStringContent
   :members:

.. autoclass:: TalonStringEscapeSequence
   :members:

.. autoclass:: TalonVariable
   :members:

.. autoclass:: TalonWord
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
