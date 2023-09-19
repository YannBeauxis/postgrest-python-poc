.PHONY: tests
tests:
	ruff .
	black --check .
	mypy --strict --ignore-missing-import .
# TODO: 100% coverage
	pytest -x --cov-report=xml:cov.xml --cov=herbaltea_classifier --cov-fail-under=88 tests
