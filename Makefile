.PHONY: help venv build

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  venv           => to create a virtualenv"
	@echo "  deps           => to install Python packages"
	@echo "  prepare        => to execute venv deps"

venv:
	@virtualenv -p python3 venv
	@venv/bin/pip install -U -r requirements.txt

build:
	@docker-compose build -t "url_shorter:latest" .
