VERSION = $(shell poetry version -s)

build:
	poetry build

build-doc:
	poetry run sphinx-build -M "html" "docs" "docs/_build"

serve:
	@(cd docs/_build/html && npx browser-sync -ss)

test:
	tox --skip-missing-interpreters

bump-version:
	@poetry run bumpver update
	@$(MAKE) release

release-version:
	@git tag 'v$(VERSION)'
	@git push origin 'v$(VERSION)'

.PHONY: build build-doc serve test bump-version release-version
