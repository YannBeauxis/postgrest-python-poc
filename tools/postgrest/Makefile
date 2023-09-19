.PHONY: tests
tests:
	ruff .
	black --check .
	mypy --strict --ignore-missing-import .
	pytest --cov-report=xml:cov.xml --cov=models --cov-fail-under=100
