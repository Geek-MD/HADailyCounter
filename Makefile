# Makefile for HA Daily Counter CI tasks

.PHONY: lint typecheck hassfest release clean ci

# Variables
PACKAGE=custom_components/ha_daily_counter

## -----------------------------------
## 🧹 Lint with Ruff
lint:
	@echo "🔍 Running Ruff Linter..."
	ruff check $(PACKAGE)

## -----------------------------------
## 🩺 Type checking with Mypy
typecheck:
	@echo "🔍 Running Mypy Type Checking..."
	mypy --config-file mypy.ini $(PACKAGE)

## -----------------------------------
## 🔍 Validate manifest & structure with Hassfest
hassfest:
	@echo "🔍 Running Hassfest validation..."
	@if [ ! -d "hassfest-core" ]; then \
		echo "📥 Downloading Home Assistant core repo..."; \
		git clone --depth 1 --single-branch --branch dev https://github.com/home-assistant/core hassfest-core; \
	fi
	python3 hassfest-core/script/hassfest --integration $(PACKAGE)
	@echo "🧹 Cleaning up hassfest-core..."
	rm -rf hassfest-core

## -----------------------------------
## 🚀 Create GitHub Release from Tag
release:
ifndef VERSION
	$(error VERSION is not set. Usage: make release VERSION=v1.0.5)
endif
	@echo "🚀 Creating GitHub release $(VERSION)..."
	gh release create $(VERSION) --generate-notes --title "$(VERSION)" || true

## -----------------------------------
## 🗑️ Clean hassfest-core manually
clean:
	@echo "🧹 Cleaning hassfest-core folder (if exists)..."
	rm -rf hassfest-core

## -----------------------------------
## 🧪 CI pipeline: lint + typecheck + hassfest
ci: lint typecheck hassfest
	@echo "✅ CI pipeline completed successfully."
