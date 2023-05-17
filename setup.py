from setuptools import Extension, setup

ext_module = Extension(
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


def main():
    setup(
        ext_modules=[ext_module],
    )


if __name__ == "__main__":
    main()
