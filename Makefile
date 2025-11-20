uv.lock: pyproject.toml
	uv lock

update-requirements: uv.lock
	uv lock

sync-venv: uv.lock
	uv sync

# create virtual env and install deps
init:
	uv venv
	bash -c 'source .venv/bin/activate && \
	uv pip install keyring keyrings-google-artifactregistry-auth && \
	uv sync'
	.venv/bin/python -m pre_commit install --install-hooks --overwrite

lint:  # lint all source code
	@uvx ruff check --config=pyproject.toml

format:  # format all source code
	@uvx ruff check --fix --config=pyproject.toml

test:  # run all tests in project
	@.venv/bin/pytest -vv tests/ --cov=load_fcast --cov-report term-missing:skip-covered --cov-fail-under=80

clean:  # remove development files
	rm -rf .venv/
	find . -name __pycache__ | xargs rm -rf
	find . -name *.egg-info | xargs rm -rf
	find . -name .pytest_cache | xargs rm -rf
	find . -name .ruff_cache | xargs rm -rf
