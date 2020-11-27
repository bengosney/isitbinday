.PHONY: help install pull update lint pre-deploy deploy freeze deprecations clean test coverage

baselinefile = .baseline.json

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install all deps
	pip install -r requirements.txt
	npm install

pull:
	git pull

update: pull install ## Update the installed deps

installLint: ## Install the linting deps
	pip install autoflake autopep8 isort flake8 flake8-django bandit eradicate

lint: $(baselinefile)  ## Format, sort imports and lint python files
	pre-commit run --all-files
	eradicate -r --in-place .

test: ## Run the tests
	python manage.py test

pre-deploy:
	@echo "Checking for clean git branch"
	@git diff-index --quiet HEAD --
	git checkout master

deploy: pre-deploy update lint test ## Full lint and asset compile
	grunt compile
	git diff-index --quiet HEAD -- || git commit -am "Compile for build"
	git push

$(baselinefile):
	touch $(baselinefile)
	bandit -x "./node_modules" -f json -o $(baselinefile) -r .

freeze: ## Update requirements
	pip freeze | grep -v pkg-resources==0.0.0 > requirements.txt

deprecations: ## Run tests with deprecations excluding 3rd party packages
	python -Wd manage.py check 2>&1 #| grep -A 1 -v site-packages

clean: ## Clean all pyc files
	find . -name *.pyc -exec rm -f {} \;

coverage: ## Test with coverage
	coverage run --source='.' manage.py test $(APP)
	coverage html

.DEFAULT_GOAL := help
