.PHONY: tests
tests:
	@cd herbaltea-classifier && poetry run make tests
	@cd tools/postgrest && poetry run make tests
	@cd tools/fastapi/auth-api && poetry run make tests

.PHONY: install-dev
install-dev:
	@cd herbaltea-classifier && poetry env use python3.11 && poetry install
	@cd tools/postgrest && poetry env use python3.11 && poetry install
	@cd tools/fastapi/auth-api && poetry env use python3.10 && poetry install
