.PHONY: help install install-dev install-all clean test lint format type-check run run-all docs

help:
	@echo "Crawler Agent - Available Commands"
	@echo "===================================="
	@echo "make install          - Install dependencies"
	@echo "make install-dev      - Install dev dependencies"
	@echo "make install-all      - Install all dependencies (dev + s3)"
	@echo "make clean            - Clean up cache and build files"
	@echo "make test             - Run tests"
	@echo "make test-cov         - Run tests with coverage report"
	@echo "make lint             - Run linter (flake8)"
	@echo "make format           - Format code (black, isort)"
	@echo "make type-check       - Type check (mypy)"
	@echo "make run              - Run crawler"
	@echo "make run-all          - Run crawler for all companies"
	@echo "make docs             - Generate documentation"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-all:
	pip install -e ".[all]"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".tox" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -name ".coverage" -delete
	find . -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned up cache and build files"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=crawlers --cov=agents --cov-report=html --cov-report=term

lint:
	flake8 crawlers agents main.py orchestrator.py config.py utils.py --max-line-length=100 --exclude=__pycache__

format:
	black crawlers agents main.py orchestrator.py config.py utils.py tests/
	isort crawlers agents main.py orchestrator.py config.py utils.py tests/

type-check:
	mypy crawlers agents main.py orchestrator.py config.py utils.py

run:
	python main.py --list

run-coupang:
	python main.py --company Coupang

run-naver:
	python main.py --company Naver

run-kakao:
	python main.py --company Kakao

run-all:
	python main.py --all

docs:
	@echo "Documentation can be found in README.md"

.DEFAULT_GOAL := help
