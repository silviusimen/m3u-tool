# M3U Playlist Filter Makefile
# This Makefile provides convenient commands for setting up and running the M3U filter script

# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
SCRIPT = filter_live_channels.py
# Default files (can be overridden)
INPUT_FILE ?= full_playlist.m3u
OUTPUT_FILE ?= live_channels.m3u

# Default target
.PHONY: help
help:
	@echo "M3U Playlist Filter - Available Commands:"
	@echo ""
	@echo "  make setup                              - Set up virtual environment and install dependencies"
	@echo "  make run                                - Run the M3U filter script with default files"
	@echo "  make filter                             - Alias for 'run'"
	@echo "  make run INPUT_FILE=input.m3u           - Run with custom input file"
	@echo "  make run OUTPUT_FILE=output.m3u         - Run with custom output file"
	@echo "  make run INPUT_FILE=in.m3u OUTPUT_FILE=out.m3u - Run with both custom files"
	@echo "  make clean                              - Remove generated files and virtual environment"
	@echo "  make reinstall                          - Clean and setup again"
	@echo "  make check                              - Check if input file exists and dependencies are installed"
	@echo "  make help                               - Show this help message"
	@echo ""
	@echo "Requirements:"
	@echo "  - Python 3.6 or higher"
	@echo "  - Default input file: $(INPUT_FILE)"
	@echo ""
	@echo "Examples:"
	@echo "  make run INPUT_FILE=playlist.m3u OUTPUT_FILE=filtered.m3u"
	@echo "  make filter INPUT_FILE=source.m3u"

# Set up virtual environment and install dependencies
.PHONY: setup
setup: $(VENV_DIR)/pyvenv.cfg
	@echo "✅ Virtual environment setup complete!"
	@echo "Dependencies installed: m3u_parser"

$(VENV_DIR)/pyvenv.cfg:
	@echo "🔧 Creating virtual environment..."
	python3 -m venv $(VENV_DIR)
	@echo "📦 Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install m3u_parser
	@echo "✅ Setup complete!"

# Check prerequisites
.PHONY: check
check:
	@echo "🔍 Checking prerequisites..."
	@if [ ! -f "$(INPUT_FILE)" ]; then \
		echo "❌ Input file '$(INPUT_FILE)' not found!"; \
		echo "   Please ensure $(INPUT_FILE) exists in the current directory."; \
		exit 1; \
	fi
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "❌ Virtual environment not found!"; \
		echo "   Run 'make setup' first to install dependencies."; \
		exit 1; \
	fi
	@if ! $(PIP) show m3u_parser > /dev/null 2>&1; then \
		echo "❌ m3u_parser library not installed!"; \
		echo "   Run 'make setup' to install dependencies."; \
		exit 1; \
	fi
	@echo "✅ All prerequisites met!"

# Run the filter script
.PHONY: run
run: check
	@echo "🎬 Running M3U playlist filter..."
	@echo "   Input:  $(INPUT_FILE)"
	@echo "   Output: $(OUTPUT_FILE)"
	$(PYTHON) $(SCRIPT) "$(INPUT_FILE)" "$(OUTPUT_FILE)"
	@if [ -f "$(OUTPUT_FILE)" ]; then \
		echo ""; \
		echo "📁 Files created:"; \
		echo "   📄 $(OUTPUT_FILE) (filtered live channels)"; \
		echo ""; \
		echo "📊 File sizes:"; \
		ls -lh "$(INPUT_FILE)" "$(OUTPUT_FILE)" | awk '{print "   " $$9 " - " $$5}'; \
	fi

# Alias for run
.PHONY: filter
filter: run

# Clean up generated files and virtual environment
.PHONY: clean
clean:
	@echo "🧹 Cleaning up..."
	@if [ -f "$(OUTPUT_FILE)" ]; then \
		rm -f $(OUTPUT_FILE); \
		echo "   🗑️  Removed $(OUTPUT_FILE)"; \
	fi
	@if [ -d "$(VENV_DIR)" ]; then \
		rm -rf $(VENV_DIR); \
		echo "   🗑️  Removed virtual environment ($(VENV_DIR)/)"; \
	fi
	@echo "✅ Cleanup complete!"

# Clean and setup again
.PHONY: reinstall
reinstall: clean setup
	@echo "✅ Reinstallation complete!"

# Quick development commands
.PHONY: dev-setup
dev-setup: setup
	@echo "🔧 Development environment ready!"
	@echo "   To activate manually: source $(VENV_DIR)/bin/activate"

# Show virtual environment status
.PHONY: status
status:
	@echo "📊 Environment Status:"
	@echo ""
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "   Virtual Environment: ✅ Installed"; \
		echo "   Location: $(VENV_DIR)/"; \
	else \
		echo "   Virtual Environment: ❌ Not found"; \
	fi
	@echo ""
	@if [ -f "$(INPUT_FILE)" ]; then \
		echo "   Input File: ✅ $(INPUT_FILE) ($(shell wc -l < $(INPUT_FILE) 2>/dev/null || echo '?') lines)"; \
	else \
		echo "   Input File: ❌ $(INPUT_FILE) not found"; \
	fi
	@echo ""
	@if [ -f "$(OUTPUT_FILE)" ]; then \
		echo "   Output File: ✅ $(OUTPUT_FILE) ($(shell wc -l < $(OUTPUT_FILE) 2>/dev/null || echo '?') lines)"; \
	else \
		echo "   Output File: ❌ $(OUTPUT_FILE) not found"; \
	fi
	@echo ""
	@if [ -d "$(VENV_DIR)" ] && $(PIP) show m3u_parser > /dev/null 2>&1; then \
		echo "   Dependencies: ✅ m3u_parser installed"; \
	else \
		echo "   Dependencies: ❌ m3u_parser not installed"; \
	fi

# Test the script with a dry run (if we add that feature)
.PHONY: test
test: check
	@echo "🧪 Testing script syntax..."
	$(PYTHON) -m py_compile $(SCRIPT)
	@echo "✅ Script syntax is valid!"

# Show available Python version
.PHONY: python-version
python-version:
	@echo "🐍 Python Information:"
	@python3 --version 2>/dev/null || echo "❌ Python 3 not found"
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Virtual Environment Python: $(shell $(PYTHON) --version 2>/dev/null)"; \
	fi

# Force targets (don't check for files)
.PHONY: help setup check run filter clean reinstall dev-setup status test python-version