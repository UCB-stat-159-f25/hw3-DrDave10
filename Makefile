# Makefile for project management
.PHONY: env html clean help

# env: create or update Conda environment from environment.yml
env:
	@echo "[ENV] Creating or updating Conda env from environment.yml..."
	if conda env list | grep -q 'myenv'; then \
	   conda env update -f environment.yml -n myenv; \
	else \
	   conda env create -f environment.yml; \
	fi

# html: build MyST site as HTML
html:
	@echo "[HTML] Building MyST site as HTML..."
	myst build --html

# clean: Remove figures, audio, and _build folders
clean:
	@echo "[CLEAN] Removing figures, audio, and _build directories..."
	rm -rf figures audio _build

# help: List available targets
help:
	@echo "\nTARGETS:"
	@grep -E '^[a-zA-Z_-]+:' Makefile | awk -F: '{print "  "$1}'
