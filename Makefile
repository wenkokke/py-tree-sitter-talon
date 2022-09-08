# Docs

docs:
	poetry install --extras "docs"
	poetry run sphinx-build -M "html" "docs" "docs/_build"

.PHONY: docs


# Versions

VERSION = $(shell poetry run python ./version.py)

minor:
	@poetry run bumpver update
	@$(MAKE) release

major:
	@poetry run bumpver update
	@$(MAKE) release

release:
	@git tag 'v$(VERSION)'
	@git push origin 'v$(VERSION)'

.PHONY: minor major release
