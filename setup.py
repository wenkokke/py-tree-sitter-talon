import setuptools  # isort:skip
from setuptools.command.develop import develop  # isort:skip
from setuptools.command.install import install  # isort:skip
from setuptools.command.sdist import sdist  # isort:skip
import distutils.cmd
import distutils.extension
import pathlib
import subprocess
import sys

pkg_dir = pathlib.Path(__file__).parent


def _get_description() -> str:
    return (pkg_dir / "README.md").read_text()


def _get_version() -> str:
    sys.path.insert(0, str(pkg_dir.absolute()))
    import tree_sitter_talon.version as pkg

    return pkg.__version__


def _get_data_files() -> list[str]:
    pkg_path = pkg_dir / "tree_sitter_talon"
    return [
        str(data_file.relative_to(pkg_path))
        for data_file in pkg_path.glob("data/tree-sitter-talon/**/*")
    ]


def _git_submodule_update():
    if (pathlib.Path(__file__).parent / ".git").exists():
        subprocess.check_call(["git", "submodule", "update", "--init", "--recursive"])
        return True

    return False


class CustomDevelop(develop):
    def run(self):
        _git_submodule_update()
        develop.run(self)


class CustomInstall(install):
    def run(self):
        _git_submodule_update()
        install.run(self)


class CustomSDist(sdist):
    def run(self):
        _git_submodule_update()
        sdist.run(self)


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
    tests_require=[
        "mypy >=0.971, <1",
        "pytest >=7.1.2, <8",
        "pytest-golden >=0.2.2, <0.3",
    ],
    install_requires=[
        "tree_sitter ==0.20.0",
        "tree_sitter_type_provider ==2.1.7",
        "dataclasses-json >=0.5.7, <0.6",
    ],
    extras_require={
        "dev": [
            "build >=0.8.0, <0.9",
            "tox >=3.25.1, <4",
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
    ],
    package_data={
        "tree_sitter_talon": [
            "py.typed",
            "internal/binding.c",
            "internal/binding.pyi",
            "internal/dynamic.pyi",
            *_get_data_files(),
        ]
    },
    cmdclass={
        "develop": CustomDevelop,
        "install": CustomInstall,
        "sdist": CustomSDist,
    },
)
