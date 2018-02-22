# Makefile for development purpose

watch:
	ack -f --type python | entr -s "mypy --ignore-missing-imports app.py && mypy --ignore-missing-imports tests/ && PYTHONPATH=. pytest api/ tests/"

