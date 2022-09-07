# Docs

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = docs/_build

html: Makefile
	@$(SPHINXBUILD) -M "html" "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: html


# Tests

test: pytest stubtest

pytest:
	@pytest

stubtest:
	@PYTHONPATH=. stubtest --mypy-config-file pyproject.toml tree_sitter_talon

.PHONY: test pytest stubtest


# Bump versions

VERSION = $(shell python setup.py -V)

minor:
	@bumpver update --no-fetch --minor
	@$(MAKE) tag

major:
	@bumpver update --no-fetch --major
	@$(MAKE) tag

release:
	@git tag "v$(VERSION)"
	@git push origin "v$(VERSION)"

.PHONY: minor major release
