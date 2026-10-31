# Usage: make [MODEL=<name>] <target>
# With no MODEL, targets apply to every model in DEFAULT_MODELS.
DEFAULT_MODELS := power_switch_cover cable_tie_plate
MODELS := $(if $(MODEL),$(MODEL),$(DEFAULT_MODELS))
EXTS   := stl step obj png svg
RUN    := uv run python

slug = $(subst _,-,$(1))
out  = build/$(call slug,$(1))/$(call slug,$(1))

.PHONY: all $(EXTS) setup view clean list help

all: $(foreach e,$(EXTS),$(foreach m,$(MODELS),$(call out,$(m)).$(e))) ## Export STL + STEP + OBJ + isometric PNG + SVG for MODEL (default: all default models)

stl: $(foreach m,$(MODELS),$(call out,$(m)).stl) ## Export STL only
step: $(foreach m,$(MODELS),$(call out,$(m)).step) ## Export STEP only
obj: $(foreach m,$(MODELS),$(call out,$(m)).obj) ## Export OBJ only
png: $(foreach m,$(MODELS),$(call out,$(m)).png) ## Export isometric render only
svg: $(foreach m,$(MODELS),$(call out,$(m)).svg) ## Export underside outline only

# All outputs of a model come from one exporter run; rebuild when the model or exporter changes.
# The run is keyed on the STL; the other files ride along with it (portable to macOS make 3.81).
define model_rule
$(call out,$(1)).stl: models/$(1).py scripts/export.py scripts/render.py
	$(RUN) scripts/export.py $(1)
$(foreach e,$(filter-out stl,$(EXTS)),$(call out,$(1)).$(e)): $(call out,$(1)).stl ;
endef
$(foreach m,$(MODELS),$(eval $(call model_rule,$(m))))

setup: ## Install dependencies into .venv
	uv sync

view: ## Export and show MODEL in the OCP viewer (needs `python -m ocp_vscode` or the VS Code extension)
	$(RUN) scripts/export.py $(firstword $(MODELS)) --view

list: ## List available models
	@ls models/*.py | grep -v __init__ | xargs -n1 basename | sed 's/\.py$$//'

clean: ## Remove build outputs
	rm -rf build

help: ## Show targets
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/'
