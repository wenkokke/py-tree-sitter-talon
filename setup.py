from setuptools import Extension, setup

ext_module = Extension(
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


def main():
    setup(
        ext_modules=[ext_module],
    )


if __name__ == "__main__":
    main()
