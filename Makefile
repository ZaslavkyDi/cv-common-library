.PHONY: ruff
ruff:
	poetry run ruff . --fix

.PHONY: black
black:
	poetry run black .

.PHONY: lint
lint:
	make ruff
	make black