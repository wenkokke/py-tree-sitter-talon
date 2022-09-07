import setuptools  # isort:skip
import distutils.cmd
import distutils.extension
import os
import pathlib
import sys


def _get_description() -> str:
    with open(os.path.join(os.path.dirname(__file__), "README.md")) as fh:
        return fh.read()


def _get_version() -> str:
    sys.path.insert(0, os.path.abspath("."))
    import tree_sitter_talon.version as pkg

    return pkg.__version__


def _get_data_files() -> list[str]:
    pkg_path = pathlib.Path(__file__).parent / "tree_sitter_talon"
    return [
        str(data_file.relative_to(pkg_path))
        for data_file in pkg_path.glob("data/tree-sitter-talon/**/*")
    ]


setuptools.setup(
    name="tree_sitter_talon",
    version=_get_version(),
    description="Parser for Talon files in Python",
    long_description=_get_description(),
    long_description_content_type="text/markdown",
    author="Wen Kokke",
    url="https://github.com/wenkokke/py-tree-sitter-talon",
    project_urls={
        "Documentation": "https://wenkokke.github.io/py-tree-sitter-talon/",
        "Source": "https://github.com/tree-sitter/py-tree-sitter",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Compilers",
    ],
    license="MIT",
    keywords=["talon", "parser"],
    platforms=["any"],
    python_requires=">=3.9",
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=[
        "pytest >=7.1.2, <8",
        "pytest-golden >=0.2.2, <0.3",
    ],
    install_requires=[
        "tree_sitter ==0.20.1",
        "tree_sitter_type_provider ==2.1.7",
        "dataclasses-json >=0.5.7, <0.6",
    ],
    extras_require={
        "dev": [
            "build >=0.8.0, <0.9",
            "twine >=4.0.1, <5",
        ],
        "docs": [
            "Sphinx >=5.1.1, <6",
            "sphinx-bootstrap-theme >=0.8.1, <0.9",
        ],
        "test": [
            "mypy >=0.971, <1",
            "pytest >=7.1.2, <8",
            "pytest-golden >=0.2.2, <0.3",
        ],
    },
    ext_modules=[
        distutils.extension.Extension(
            name="tree_sitter_talon.binding",
            sources=[
                "tree_sitter_talon/binding.c",
                "tree_sitter_talon/data/tree-sitter-talon/src/parser.c",
                "tree_sitter_talon/data/tree-sitter-talon/src/scanner.cc",
            ],
            include_dirs=[
                "tree_sitter_talon/data/tree-sitter-talon/src",
            ],
        )
    ],
    package_data={
        "tree_sitter_talon": [
            "py.typed",
            "binding.c",
            "binding.pyi",
            "dynamic.pyi",
            *_get_data_files(),
        ]
    },
)
