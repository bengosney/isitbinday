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
	autoflake --expand-star-imports --exclude "migrations" --exclude "node_modules" -i -r --remove-unused-variables --remove-all-unused-imports .
	autopep8 -a -a -a --exclude "migrations,node_modules" --in-place --recursive .
	isort "." --skip "stef/wsgi.py" --skip-glob "**/migrations/*" --skip-glob "*/node_modules/*"
	flake8 --exclude migrations,node_modules .
	bandit -x "./node_modules" -b $(baselinefile) -r .
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
