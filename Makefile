PROJECT_NAME ?= $(shell python3 setup.py --name)
VERSION = $(shell python3 setup.py --version | tr '+' '-')


all:
	@echo "make devenv     - Configure the development environment"
	@echo "make clean      - Remove files created by distutils"
	@echo "make codestyle  - Reformat code with gray linter"
	@exit 0

$(PROJECT_NAME)/version.py:
	python3 bump.py $(PROJECT_NAME)/version.py

bump: clean $(PROJECT_NAME)/version.py

sdist: bump
	python3 setup.py sdist

clean:
	rm -fr *.egg-info .tox dist $(PROJECT_NAME)/version.py

clean-pyc:
	find . -iname '*.pyc' -delete

devenv: clean
	rm -fr env
	python3.10 -m venv env
	env/bin/pip install -U pip
	env/bin/pip install -Ue '.[dev]'
	env/bin/pip check

lint:
	twine check --strict dist/*

codestyle:
	gray *.py lxd tests
