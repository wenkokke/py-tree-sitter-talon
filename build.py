from distutils.extension import Extension

ext_modules = [
    Extension(
        name="tree_sitter_talon.internal.binding",
        sources=[
            "tree_sitter_talon/internal/binding.c",
            "tree_sitter_talon/data/tree-sitter-talon/src/parser.c",
            "tree_sitter_talon/data/tree-sitter-talon/src/scanner.cc",
        ],
        include_dirs=[
            "tree_sitter_talon/data/tree-sitter-talon/src",
        ],
    )
]


def build(kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    kwargs.update({"ext_modules": ext_modules})
