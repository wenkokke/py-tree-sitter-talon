"""
Py-Tree-Sitter-Talon
"""

import os
import pathlib
import sys

import setuptools


def build_library() -> tuple[str, ...]:
    try:
        package_root = pathlib.Path(__file__).parent.absolute()
        sys.path.insert(0, str(package_root))
        import tree_sitter_talon

        library_path = pathlib.Path(tree_sitter_talon.library_path)  # type: ignore
        library_path = library_path.relative_to(package_root)
        return (str(library_path),)
    except (ImportError, RuntimeError):
        return ()


library_path: tuple[str, ...]
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package
            self.root_is_pure = False

        def get_tag(self):
            _, _, plat = _bdist_wheel.get_tag(self)
            python, abi = "py3", "none"
            # Pretend to be manylinux:
            plat = plat.replace("linux", "manylinux1")
            return python, abi, plat

    library_path = build_library()

except ImportError:
    bdist_wheel = None  # type: ignore
    library_path = ()


with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="tree_sitter_talon",
    version="1.5.18",
    description="Parser for Talon files in Python",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Wen Kokke",
    url="https://github.com/wenkokke/py-tree-sitter-talon",
    project_urls={
        "Documentation": "https://wenkokke.github.io/py-tree-sitter-talon/",
        "Source": "https://github.com/tree-sitter/py-tree-sitter",
    },
    packages=["tree_sitter_talon"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Compilers",
    ],
    license="MIT",
    keywords=["talon", "parser"],
    platforms=["any"],
    python_requires=">=3.9",
    install_requires=[
        "tree_sitter",
        "tree_sitter_type_provider >=1.4.7",
        "dataclasses-json",
    ],
    extras_require={
        "sphinx": [
            "sphinx",
            "sphinx_bootstrap_theme",
        ],
        "test": [
            "pytest",
            "pytest-golden",
            "mypy",
        ],
        "publish": [
            "bumpver",
            "build",
            "twine",
            "auditwheel;platform_system=='Linux'",
        ],
    },
    package_data={
        "tree_sitter_talon": [
            "py.typed",
            "__init__.pyi",
            *library_path,
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
    cmdclass={
        "bdist_wheel": bdist_wheel,
    },
)
