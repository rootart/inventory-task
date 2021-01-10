SHELL=/bin/bash

all:
	make help

run: #red Execute runserver_plus
	python -W ignore manage.py runserver_plus 127.0.0.1:8000 --nopin

reqs: #red Compile requirements with pip-tools
	cd .. && pip-compile && pip-compile requirements-dev.in -o requirements-dev.txt

check: #red Run Flake8 and other checkers
	flake8

coverage:
	pytest --cov=. --cov-report=html


.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?#pink .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?#pink "}; {printf "\033[36m%-50s\033[95m %s\n", $$1, $$2}' ## pink
	@grep -E '^[a-zA-Z_-]+:.*?#yellow .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?#yellow "}; {printf "\033[36m%-50s\033[93m %s\n", $$1, $$2}' ## yellow
	@grep -E '^[a-zA-Z_-]+:.*?#blue .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?#blue "}; {printf "\033[36m%-50s\033[96m %s\n", $$1, $$2}' ## blue
	@grep -E '^[a-zA-Z_-]+:.*?#red .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?#red "}; {printf "\033[36m%-50s\033[91m %s\n", $$1, $$2}' ## red
	@grep -E '^[a-zA-Z_-]+:.*?#white .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?#white "}; {printf "\033[36m%-50s\033[97m %s\n", $$1, $$2}' ## white
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-50s\033[0m %s\n", $$1, $$2}' ## default
