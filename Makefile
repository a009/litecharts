.PHONY: lint

lint:
	uv run ruff format src/
	uv run ruff check src/ --fix
	uv run mypy src/ --strict
