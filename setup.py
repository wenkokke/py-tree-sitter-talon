"""
Py-Tree-Sitter-Talon
"""

from os import path, system
from setuptools import setup
from setuptools.command.sdist import sdist


class custom_sdist(sdist):
    def run(self):
        system("git submodule update --init")
        sdist.run(self)


with open(path.join(path.dirname(__file__), "README.md")) as f:
    LONG_DESCRIPTION = f.read()


setup(
    name="tree_sitter_talon",
    version="0.1.0",
    maintainer="Wen Kokke",
    maintainer_email="me@wen.works",
    author="Wen Kokke",
    author_email="me@wen.works",
    url="https://github.com/wenkokke/py-tree-sitter-talon",
    license="MIT",
    platforms=["any"],
    python_requires=">=3.3",
    description="Parser for Talon files in Python",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Compilers",
        "Topic :: Text Processing :: Linguistic",
    ],
    packages=["tree_sitter_talon"],
    project_urls={"Source": "https://github.com/wenkokke/py-tree-sitter-talon"},
    install_requires=[
        "tree_sitter",
        "tree_sitter_type_provider @ git+ssh://git@github.com/wenkokke/py-tree-sitter-type-provider.git#egg=tree_sitter_type_provider",
    ],
    cmdclass={"sdist": custom_sdist},
    package_data={
        'tree_sitter_talon': [
            "tree_sitter_talon/data/tree-sitter-talon/Cargo.toml",
            "tree_sitter_talon/data/tree-sitter-talon/binding.gyp",
            "tree_sitter_talon/data/tree-sitter-talon/bindings/node/binding.cc",
            "tree_sitter_talon/data/tree-sitter-talon/bindings/node/index.js",
            "tree_sitter_talon/data/tree-sitter-talon/bindings/rust/build.rs",
            "tree_sitter_talon/data/tree-sitter-talon/bindings/rust/lib.rs",
            "tree_sitter_talon/data/tree-sitter-talon/grammar.js",
            "tree_sitter_talon/data/tree-sitter-talon/package.json",
            "tree_sitter_talon/data/tree-sitter-talon/src/grammar.json",
            "tree_sitter_talon/data/tree-sitter-talon/src/node-types.json",
            "tree_sitter_talon/data/tree-sitter-talon/src/parser.c",
            "tree_sitter_talon/data/tree-sitter-talon/src/scanner.cc",
            "tree_sitter_talon/data/tree-sitter-talon/src/tree_sitter/parser.h",
        ]
    },
)
