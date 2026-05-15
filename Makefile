.PHONY: demo lint docker-build install help

PYTHON := python

help:
	@echo "Available targets:"
	@echo "  make install       Install demo dependencies"
	@echo "  make demo          Run all demo examples"
	@echo "  make lint          Run ruff linter on demo scripts"
	@echo "  make docker-build  Build Docker image"

install:
	pip install pandas numpy

demo:
	$(PYTHON) demo/examples/01_basic_query.py
	$(PYTHON) demo/examples/02_multi_table_analysis.py

lint:
	pip install ruff --quiet
	ruff check demo/ --ignore E501

docker-build:
	docker build -t conversaetl:latest .
