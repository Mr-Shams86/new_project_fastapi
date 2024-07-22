# Makefile

.PHONY: help install run migrate test lint

help: 
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-15s %s\n", $$1, $$2}'

install: 
	@pip install -r requirements.txt

run: 
	@uvicorn main:app --reload

migrate: 
	@alembic upgrade head

makemigrations: 
	@alembic revision --autogenerate -m "New migration"

test: 
	@pytest

lint: 
	@flake8 .
