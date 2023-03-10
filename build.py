import os
import shutil
from distutils.command.build_ext import build_ext
from distutils.core import Distribution, Extension

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


def build():
    distribution = Distribution(
        {"name": "tree-sitter-talon", "ext_modules": ext_modules}
    )
    distribution.package_dir = "tree_sitter_talon"

    cmd = build_ext(distribution)
    cmd.ensure_finalized()
    cmd.run()

    # Copy built extensions back to the project
    for output in cmd.get_outputs():
        relative_extension = os.path.relpath(output, cmd.build_lib)
        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)


if __name__ == "__main__":
    build()
