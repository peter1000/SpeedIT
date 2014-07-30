#!/bin/bash

PYTHON=/usr/bin/env python3

.PHONY: help cleanall clean tests tests_cover build install dist docs info check_setup pypi_all


help:
	@echo 'Please use: `make <target>` where <target> is one of'
	@echo '  cleanall             clean inclusive generated documentation and cython c files.'
	@echo '  clean                basic clean: keeps builds, docs and cython c and extensions (.so) files'
	@echo '  tests                test the project: BUT remove any cython extensions'
	@echo '  tests_cover          test with coverage report: html dir: `cover` BUT remove any cython extensions'
	@echo '  build                build the project'
	@echo '  install              install the package'
	@echo '  dist                 build a source distribution tar file'
	@echo '  docs                 build the docs for the project'
	@echo '  info                 build the general info'
	@echo '  check_setup          checks the setup.py file'
	@echo '  pypi_all             re-register/upload (inclusive docs) to pypi'


cleanall: clean
	@rm -rf build dist cover zipped_docs
	@rm -rf docs/SpeedIT-DOCUMENTATION
	@rm -rf info/GENERAL-INFO
	@rm -rf docs/source/SpeedIT.rst docs/source/modules.rst

clean:
	@find . -iname '__pycache__' |xargs rm -rf
	@find . -iname '*.egg-info' |xargs rm -rf
	@find . -iname '*.pyc' |xargs rm -rf
	@rm -rf MANIFEST .coverage

tests: clean
	${PYTHON} setup.py nosetests
	$(MAKE) clean
	@echo -e '\n=== finished tests'

tests_cover: clean
	@rm -rf cover
	${PYTHON} setup.py nosetests --cover-branches --with-coverage --cover-html --cover-erase --cover-package=SpeedIT
	$(MAKE) clean
	@echo -e '\n=== finished tests_cover'

build: clean
	rm -rf build
	${PYTHON} setup.py build
	$(MAKE) clean
	@echo -e '\n=== finished build'

dist: cleanall
	${PYTHON} setup.py sdist
	$(MAKE) clean
	@echo -e '\n=== finished dist'

install: clean
	rm -rf build
	${PYTHON} setup.py install
	$(MAKE) clean
	@echo -e '\n=== finished install'

docs:
	rm -rf docs/SpeedIT-DOCUMENTATION
	sphinx-apidoc --force --output-dir=docs/source SpeedIT
	cd docs && make html
	cd ..
	$(MAKE) clean
	@echo -e '\n=== finished docs'

info:
	rm -rf info/GENERAL-INFO
	cd info && make html
	cd ..
	$(MAKE) clean
	@echo -e '\n=== finished info'

check_setup: clean
	${PYTHON} setup.py check
	$(MAKE) clean
	@echo -e '\n=== finished check_setup'

pypi_all: clean
	${PYTHON} setup.py check register sdist upload
	$(MAKE) clean
	$(MAKE) docs
	${PYTHON} setup.py upload_docs
	$(MAKE) clean
	@echo -e '\n=== finished pypi_all'
