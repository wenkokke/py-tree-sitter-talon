from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            name="tree_sitter_talon._internal.binding",
            sources=[
                "src/tree_sitter_talon/_internal/binding.c",
                "src/tree_sitter_talon/_tree_sitter_talon/src/parser.c",
                "src/tree_sitter_talon/_tree_sitter_talon/src/scanner.cc",
            ],
            include_dirs=[
                "src/tree_sitter_talon/_tree_sitter_talon/src",
            ],
        )
    ],
)
