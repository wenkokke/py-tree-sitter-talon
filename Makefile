VERSION = $(shell poetry version -s)

build:
	poetry build

build-doc:
	poetry install -E docs
	poetry run sphinx-build -M "html" "docs" "docs/_build"

test:
	tox --skip-missing-interpreters true

bump-version:
	@poetry run bumpver update
	@$(MAKE) release

release-version:
	@git tag 'v$(VERSION)'
	@git push origin 'v$(VERSION)'

.PHONY: build build-doc test bump-version release-version
