#################################################################################
# Tests
#################################################################################

.PHONY: test
test:
	tox

#################################################################################
# Build Docs
#################################################################################

.PHONY: serve
serve:
	@.venv/bin/python -m http.server --directory ./example/docs/_build/html

.PHONY: docs
docs: .venv/bin/activate
	@bash -c "source .venv/bin/activate; pip install -q .[docs]; sphinx-build -M 'html' 'docs' 'docs/_build'"

.venv/bin/activate:
	@python -m venv .venv
