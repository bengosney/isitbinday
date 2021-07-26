.PHONY := install, install-dev, help
.DEFAULT_GOAL := install-dev

INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

requirements.%.txt: requirements.%.in
	@echo "Builing $@"
	@pip-compile -q -o $@ $^

requirements.txt: requirements.in
	@echo "Builing $@"
	@pip-compile -q $^

install: requirements.txt ## Install production requirements
	@echo "Installing $^"
	@pip-sync $^

install-dev: requirements.txt $(REQS) ## Install development requirements (default)
	@echo "Installing $^"
	@pip-sync $^

_init:
	pip install wheel pip-tools

init: _init install-dev