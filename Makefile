.PHONY := install, help
.DEFAULT_GOAL := install

INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.envrc: runtime.txt
	@echo layout python $(shell cat $^ | tr -d "-" | egrep -o "python[0-9]\.[0-9]+") > $@
	@false

requirements.%.txt: requirements.%.in requirements.txt
	@echo "Builing $@"
	@pip-compile --generate-hashes -q -o $@ $<
	@touch $@

requirements.txt: requirements.in
	@echo "Builing $@"
	@pip-compile --generate-hashes -q $^

install: requirements.txt $(REQS) ## Install development requirements
	@echo "Installing $^"
	@pip-sync $^

$(HOOKS):
	pre-commit install

pre-init:
	python -m ensurepip
	python -m pip install --upgrade pip
	python -m pip install wheel pip-tools

init: .envrc pre-init install $(HOOKS) ## Initalise a dev enviroment
	@which direnv > /dev/null || echo "direnv not found but recommended"
	@echo "Read to dev"
