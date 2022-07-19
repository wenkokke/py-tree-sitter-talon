"""
Py-Tree-Sitter-Talon
"""

import os
import shutil
from setuptools import setup
from setuptools.command.sdist import sdist


class custom_sdist(sdist):
    def run(self):

        # Get data/tree-sitter-talon
        if shutil.which("git") is not None:
            os.system("git submodule update --init")
        else:
            print("Building tree_sitter_talon requires git")
            exit(1)

        # Run sdist
        sdist.run(self)


with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    LONG_DESCRIPTION = f.read()


setup(
    name="tree_sitter_talon",
    version="1.1.1",
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
        "tree_sitter_type_provider @ git+https://github.com/wenkokke/py-tree-sitter-type-provider.git@v1.0.4#egg=tree_sitter_type_provider",
        "sphinx",
        "sphinx-toolbox >=3.1.2",
        "sphinx_bootstrap_theme",
        "pytest",
        "pytest-golden",
    ],
    cmdclass={"sdist": custom_sdist},
    package_data={
        "tree_sitter_talon": [
            "py.typed",
            "__init__.pyi",
            "data/tree-sitter-talon/binding.gyp",
            "data/tree-sitter-talon/bindings/node/binding.cc",
            "data/tree-sitter-talon/bindings/node/index.js",
            "data/tree-sitter-talon/bindings/rust/build.rs",
            "data/tree-sitter-talon/bindings/rust/lib.rs",
            "data/tree-sitter-talon/grammar.js",
            "data/tree-sitter-talon/package.json",
            "data/tree-sitter-talon/src/grammar.json",
            "data/tree-sitter-talon/src/node-types.json",
            "data/tree-sitter-talon/src/parser.c",
            "data/tree-sitter-talon/src/scanner.cc",
            "data/tree-sitter-talon/src/tree_sitter/parser.h",
        ]
    },
)
