from _typeshed import Incomplete
from tree_sitter.binding import Node as Node
from tree_sitter.binding import Parser as Parser
from tree_sitter.binding import Tree as Tree
from tree_sitter.binding import TreeCursor as TreeCursor

class Language:
    @staticmethod
    def build_library(output_path, repo_paths): ...
    name: Incomplete
    lib: Incomplete
    language_id: Incomplete
    def __init__(self, library_path, name) -> None: ...
    def field_id_for_name(self, name): ...
    def query(self, source): ...
