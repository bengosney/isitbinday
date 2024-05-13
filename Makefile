.PHONY: help clean test install all init dev dist, emails
.DEFAULT_GOAL := install
.PRECIOUS: requirements.%.in

HOOKS=$(.git/hooks/pre-commit)
INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

EMAIL_TEMPLATES=$(subst .mjml,.html,$(wildcard templates/emails/*.mjml))

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.gitignore:
	curl -q "https://www.toptal.com/developers/gitignore/api/visualstudiocode,python,direnv" > $@

.git: .gitignore
	git init

.pre-commit-config.yaml:
	curl https://gist.githubusercontent.com/bengosney/4b1f1ab7012380f7e9b9d1d668626143/raw/060fd68f4c7dec75e8481e5f5a4232296282779d/.pre-commit-config.yaml > $@
	python -m pip install pre-commit
	pre-commit autoupdate

requirements.%.in:
	echo "-c requirements.txt" > $@

requirements.%.txt: requirements.%.in
	@echo "Builing $@"
	@python -m piptools compile -q -o $@ $^

requirements.txt: requirements.in
	@echo "Builing $@"
	@python -m piptools compile -q requirements.in

.direnv: .envrc
	python -m pip install --upgrade pip
	python -m pip install wheel pip-tools
	@touch $@ $^

.git/hooks/pre-commit: .pre-commit-config.yaml
	python -m pip install pre-commit
	pre-commit install

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo "layout python python3.10" > $@
	@touch -d '+1 minute' $@
	@false

piptools:
	python -m pip install pip-tools

init: .direnv .git .git/hooks/pre-commit piptools requirements.dev.txt ## Initalise a enviroment

clean: ## Remove all build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -f .testmondata

install: requirements.txt $(REQS) ## Install development requirements (default)
	@echo "Installing $^"
	@python -m piptools sync $^

templates/emails/%.html: templates/emails/%.mjml
	npx mjml $< --config.minify -o $@

emails: $(EMAIL_TEMPLATES) ## Compile the email templates to django templates

dev: init install ## Start work
	code .

pytest:
	pytest

dist:
	python setup.py sdist

upgrade: pyproject.toml
	@echo "Upgrading pip packages"
	@python -m piptools compile -q --upgrade pyproject.toml
