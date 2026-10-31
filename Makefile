# Usage: make [MODEL=example] <target>
MODEL ?= plate
RUN   := uv run python

.PHONY: all stl step setup view clean list help

all: build/$(MODEL).stl build/$(MODEL).step build/$(MODEL).svg ## Export STL + STEP + SVG for MODEL (default: plate)

stl: build/$(MODEL).stl ## Export STL only
step: build/$(MODEL).step ## Export STEP only

# Both files come from one run; rebuild when the model or exporter changes.
build/$(MODEL).stl build/$(MODEL).step build/$(MODEL).svg: models/$(MODEL).py scripts/export.py
	$(RUN) scripts/export.py $(MODEL)

setup: ## Install dependencies into .venv
	uv sync

view: ## Export and show in the OCP viewer (needs `python -m ocp_vscode` or the VS Code extension)
	$(RUN) scripts/export.py $(MODEL) --view

list: ## List available models
	@ls models/*.py | grep -v __init__ | xargs -n1 basename | sed 's/\.py$$//'

clean: ## Remove build outputs
	rm -rf build

help: ## Show targets
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/'
