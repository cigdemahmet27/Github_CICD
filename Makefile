# Run the SAME steps the pipeline runs, but on your machine.
.PHONY: install lint test build all

install:
	python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt

lint:
	.venv/bin/ruff check .

test:
	.venv/bin/pytest --cov=app --cov-report=term

build:
	.venv/bin/python -m app.build_site

all: lint test build
