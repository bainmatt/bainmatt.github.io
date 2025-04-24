CURRENT_FILE_EDITING =
# CURRENT_FILE_EDITING = posts/2024-03-15-writing-temp/cheatsheet.qmd

.PHONY: process-eq process-eq-r


# -- Dev ---------------------------------------------------------------------

# Forward substitution on math block labels ($$\n{#eq-*} -> $$ {#eq-*})
process-eq:
	@echo "Running process-eq..."
	@if [ -n "$(CURRENT_FILE_EDITING)" ]; then \
		python scripts/process_eq_labels.py $(CURRENT_FILE_EDITING); \
	else \
		echo "No CURRENT_FILE_EDITING provided. Skipping post-render step."; \
	fi


# Reverse substitution on math block labels ($$ {#eq-*} -> $$\n{#eq-*})
process-eq-r:
	@echo "Running process-eq-r..."
	@if [ -n "$(CURRENT_FILE_EDITING)" ]; then \
		python scripts/process_eq_labels.py $(CURRENT_FILE_EDITING) -r; \
	else \
		echo "No CURRENT_FILE_EDITING provided. Skipping pre-render step."; \
	fi


# -- CI ----------------------------------------------------------------------
