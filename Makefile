# Makefile

.PHONY: help install run migrate test lint

help: ## Показывает доступные команды
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-15s %s\n", $$1, $$2}'

install: ## Устанавливает зависимости
	@pip install -r requirements.txt

run: ## Запускает FastAPI сервер
	@uvicorn main:app --reload

migrate: ## Выполняет миграции Alembic
	@alembic upgrade head

makemigrations: ## Создает новые миграции Alembic
	@alembic revision --autogenerate -m "New migration"

test: ## Запускает тесты
	@pytest

lint: ## Проверяет код с помощью linters
	@flake8 .
