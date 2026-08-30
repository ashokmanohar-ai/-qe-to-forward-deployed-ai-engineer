.PHONY: install check test docs serve run docker validate

install:
	python -m pip install -e ".[dev]"

check:
	ruff check .
	ruff format --check .
	mypy src/qe_fde
	python scripts/validate_repo.py

test:
	pytest

docs:
	mkdocs build --strict

serve:
	mkdocs serve

run:
	uvicorn qe_fde.ai_service.api:create_app --factory --host 0.0.0.0 --port 8000 --reload

docker:
	docker compose up --build

validate:
	python scripts/validate_repo.py
