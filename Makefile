# Sphinx Docs

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = doc-source
BUILDDIR      = _build

html: Makefile
	@$(SPHINXBUILD) -M "html" "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Bump versions

patch:
	bumpver update --patch

minor:
	bumpver update --minor

major:
	bumpver update --major

.PHONY: patch minor major

# Publish to PyPi

run/dist:
	python -m build
	twine check dist/*

run/testpypi: run/dist
	twine upload --skip-existing -r testpypi dist/*

run/pypi: run/dist
	twine upload --skip-existing -r pypi dist/*

.PHONY: run/dist run/testpypi run/pypi
