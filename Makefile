# Sphinx Docs

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = doc-source
BUILDDIR      = _build

html: Makefile
	@$(SPHINXBUILD) -M "html" "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Tests

test: pytest stubtest

pytest:
	@python setup.py pytest

stubtest:
	@stubtest --mypy-config-file pyproject.toml tree_sitter_talon

.PHONY: test pytest stubtest

# Bump versions

VERSION = $(shell python setup.py -V)

minor:
	@bumpver update --no-fetch --minor
	@git tag "$(VERSION)"
	@git push origin "$(VERSION)"

major:
	@bumpver update --no-fetch --major
	@git tag "$(VERSION)"
	@git push origin "$(VERSION)"

.PHONY: minor major

# Publish to PyPi

run/dist:
	python -m build
	twine check dist/*

run/testpypi: run/dist
	twine upload --skip-existing -r testpypi dist/*

run/pypi: run/dist
	twine upload --skip-existing -r pypi dist/*

.PHONY: run/dist run/testpypi run/pypi
