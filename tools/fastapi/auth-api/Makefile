.PHONY: tests
tests:
	ruff .
	black --check .
	mypy --strict --ignore-missing-import .
	AUTH_API_SECRET_KEY=secret MAGIC_API_SECRET_KEY=secret pytest --cov-report=xml:cov.xml --cov=auth_api --cov-fail-under=100
