-------------------------------------
   .. autoclass:: Python bindings for Tree-Sitter Talon
      :members:

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
   .. autoclass:: Talon Abstract Syntax Tree Nodes
      :members:

================================

All AST nodes inherit from the Node class.

.. autoclass:: Node

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

There are two subclasses of `Node`:

.. autoclass:: Leaf

   Leaf nodes have no fields other than those inherited from Node.

.. autoclass:: Branch

   Branch nodes are guaranteed to have a field `children`, as well as other fields corresponding to the named fields in the tree-sitter grammar.

   Each subclass provides a more specific typing for `children`, including `None` if the subclass only has named fields.

   .. autoattribute:: children

Each explicit node in the tree-sitter grammar corresponds to a dataclass.

   .. autoclass:: TalonSourceFile
      :members:

   .. autoclass:: TalonComment
      :members:

   .. autoclass:: TalonError
      :members:

   .. autoclass:: TalonMatches
      :members:

   .. autoclass:: TalonMatch
      :members:

   .. autoclass:: TalonMatchModifier
      :members:

   .. autoclass:: TalonDeclaration
      :members:

   .. autoclass:: TalonCommandDeclaration
      :members:

   .. autoclass:: TalonKeyBindingDeclaration
      :members:

   .. autoclass:: TalonSettingsDeclaration
      :members:

   .. autoclass:: TalonTagImportDeclaration
      :members:

   .. autoclass:: TalonCapture
      :members:

   .. autoclass:: TalonChoice
      :members:

   .. autoclass:: TalonEndAnchor
      :members:

   .. autoclass:: TalonList
      :members:

   .. autoclass:: TalonOptional
      :members:

   .. autoclass:: TalonParenthesizedRule
      :members:

   .. autoclass:: TalonRepeat
      :members:

   .. autoclass:: TalonRepeat1
      :members:

   .. autoclass:: TalonRule
      :members:

   .. autoclass:: TalonSeq
      :members:

   .. autoclass:: TalonStartAnchor
      :members:

   .. autoclass:: TalonWord
      :members:

   .. autoclass:: TalonStatement
      :members:

   .. autoclass:: TalonAssignmentStatement
      :members:

   .. autoclass:: TalonExpressionStatement
      :members:

   .. autoclass:: TalonBlock
      :members:

   .. autoclass:: TalonExpression
      :members:

   .. autoclass:: TalonAction
      :members:

   .. autoclass:: TalonArgumentList
      :members:

   .. autoclass:: TalonBinaryOperator
      :members:

   .. autoclass:: TalonKeyAction
      :members:

   .. autoclass:: TalonParenthesizedExpression
      :members:

   .. autoclass:: TalonSleepAction
      :members:

   .. autoclass:: TalonVariable
      :members:

   .. autoclass:: TalonIdentifier
      :members:

   .. autoclass:: TalonOperator
      :members:

   .. autoclass:: TalonImplicitString
      :members:

   .. autoclass:: TalonInterpolation
      :members:

   .. autoclass:: TalonString
      :members:

   .. autoclass:: TalonStringContent
      :members:

   .. autoclass:: TalonStringEscapeSequence
      :members:

   .. autoclass:: TalonFloat
      :members:

   .. autoclass:: TalonInteger
      :members:

   .. autoclass:: TalonNumber
      :members:


========================================
Helper Classes
========================================

.. autoclass:: Point
