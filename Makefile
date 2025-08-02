# Makefile for Large-Scale Ranking System

.PHONY: help install install-dev setup test clean lint type-check

help:
	@echo "Available commands:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  setup        Set up the project environment"
	@echo "  test         Run tests"
	@echo "  clean        Clean up generated files"
	@echo "  lint         Run linting"
	@echo "  type-check   Run type checking"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

setup:
	python scripts/setup_phase1.py
	python scripts/validate_data.py

test:
	pytest tests/ -v

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

lint:
	black src/ tests/
	flake8 src/ tests/

type-check:
	mypy src/

data-download:
	bash scripts/download_amazon_data.sh

notebook:
	jupyter lab notebooks/
