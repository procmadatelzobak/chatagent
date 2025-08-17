PYTHON ?= python3

.PHONY: lint format test

lint:
	cd backend && $(PYTHON) -m ruff check .
	cd backend && $(PYTHON) -m black --check .

format:
	cd backend && $(PYTHON) -m black .

test:
	cd backend && $(PYTHON) -m pytest
