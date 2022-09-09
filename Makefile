VERSION = $(shell poetry run python ./version.py)

build:
	poetry build

build-doc:
	poetry install -E docs
	poetry run sphinx-build -M "html" "docs" "docs/_build"

test:
	tox --skip-missing-interpreters true

bump-minor:
	@poetry run bumpver update
	@$(MAKE) release

bump-major:
	@poetry run bumpver update
	@$(MAKE) release

tag-release:
	@git tag 'v$(VERSION)'
	@git push origin 'v$(VERSION)'

.PHONY: build build-doc test bump-minor bump-major tag-release
