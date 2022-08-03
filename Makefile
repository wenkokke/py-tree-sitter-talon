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
	mkdir -p run && touch run/dist

run/testpypi: run/dist
	twine upload --skip-existing -r testpypi dist/*
	mkdir -p run && touch run/testpypi

run/pypi: run/dist
	twine upload --skip-existing -r pypi dist/*
	mkdir -p run && touch run/pypi

.PHONY: run/dist run/testpypi run/pypi
