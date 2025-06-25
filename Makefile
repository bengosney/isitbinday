.PHONY: help clean test install all init dev css js cog coverage git-hooks watch-assets upgrade test
.DEFAULT_GOAL := dev
.PRECIOUS: requirements.%.in
.FORCE:

HOOKS=$(.git/hooks/pre-commit)
REQS=$(shell python -c 'import tomllib;[print(f"requirements.{k}.txt") for k in tomllib.load(open("pyproject.toml", "rb"))["project"]["optional-dependencies"].keys()]')

COG_FILE:=.cogfiles

TS_FILES:=$(wildcard assets/typescript/*.ts)
JS_FILES:=$(patsubst assets/typescript/%.ts,static/js/%.min.js,$(TS_FILES))

ALL_CSS_FILES:=$(shell find assets/css/ -mindepth 2 -name *.css 2>/dev/null)
CSS_FILES:=$(wildcard assets/css/*.css)
CSS_MIN_FILES:=$(patsubst assets/css/%.css,static/css/%.min.css,$(CSS_FILES))

PYTHON_VERSION:=$(shell python --version | cut -d " " -f 2)
BINPATH=$(shell which python | xargs dirname | xargs realpath --relative-to=".")
PIP_PATH:=$(BINPATH)/pip
WHEEL_PATH:=$(BINPATH)/wheel
PRE_COMMIT_PATH:=$(BINPATH)/pre-commit
UV_PATH:=$(BINPATH)/uv
COG_PATH:=$(BINPATH)/cog
COGABLE:=$(shell git ls-files | xargs grep -l "\[\[\[cog")
MIGRATION_FILES:=$(shell ls -d -- **/migrations/*.py)

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.gitignore:
	curl -q "https://www.toptal.com/developers/gitignore/api/visualstudiocode,python,direnv" > $@

.git: .gitignore
	git init

.pre-commit-config.yaml: $(PRE_COMMIT_PATH) .git
	curl https://gist.githubusercontent.com/bengosney/4b1f1ab7012380f7e9b9d1d668626143/raw/.pre-commit-config.yaml > $@
	pre-commit autoupdate
	@touch $@

.git/hooks/%: .git $(PRE_COMMIT_PATH)
	pre-commit install --hook-type $(notdir $@)

.git/hooks/prepare-commit-msg:
	wget -O $@ https://raw.githubusercontent.com/commitizen-tools/commitizen/master/hooks/$(notdir $@).py
	chmod +x $@

.git/hooks/post-commit:
	wget -O $@ https://raw.githubusercontent.com/commitizen-tools/commitizen/master/hooks/$(notdir $@).py
	chmod +x $@

git-hooks: .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/prepare-commit-msg .git/hooks/post-commit ## Install git hooks

pyproject.toml:
	curl https://gist.githubusercontent.com/bengosney/f703f25921628136f78449c32d37fcb5/raw/pyproject.toml > $@
	@touch $@

requirements.%.txt: $(UV_PATH) pyproject.toml
	@echo "Builing $@"
	python -m uv pip compile --generate-hashes --extra $* $(filter-out $<,$^) > $@

requirements.txt: $(UV_PATH) pyproject.toml
	@echo "Builing $@"
	python -m uv pip compile --generate-hashes $(filter-out $<,$^) > $@

.direnv: .envrc $(UV_PATH) requirements.txt $(REQS)
	@echo "Installing $(filter-out $<,$^)"
	python -m uv pip sync requirements.txt $(REQS)
	@touch $@

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo "layout python python3.12" > $@
	@touch -d '+1 minute' $@
	@false

$(PIP_PATH): .envrc
	@python -m ensurepip
	@python -m pip install --upgrade pip
	@touch $@

$(WHEEL_PATH): $(PIP_PATH)
	@python -m pip install wheel
	@touch $@

$(UV_PATH): $(PIP_PATH) $(WHEEL_PATH)
	@python -m pip install uv
	@touch $@

$(PRE_COMMIT_PATH): $(PIP_PATH) $(WHEEL_PATH)
	@python -m pip install pre-commit

init: .envrc $(UV_PATH) requirements.dev.txt .direnv git-hooks ## Initalise a enviroment
	@python -m pip install --upgrade pip

clean: ## Remove all build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -f .testmondata
	rm -rf *.egg-info

static/css/%.min.css: assets/css/%.css $(ALL_CSS_FILES)
	npx lightningcss-cli --minify --bundle --nesting --targets '>= 0.25%' $< -o $@
	@touch $@

css: $(CSS_MIN_FILES) ## Build the css

watch-assets: ## Watch and build the css and js
	@echo "Watching scss"
	$(MAKE) css js
	@while inotifywait -qr -e close_write assets/; do \
		$(MAKE) css js; \
	done

install: $(UV_PATH) requirements.txt $(REQS) ## Install development requirements (default)
	@echo "Installing $(filter-out $<,$^)"
	python -m uv pip sync $(filter-out $<,$^)

_upgrade: $(UV_PATH) requirements.txt
	@echo "Upgrading pip packages"
	@python -m pip install --upgrade pip
	@python -m uv pip compile -q --upgrade -o requirements.txt pyproject.toml

upgrade: _upgrade $(PRE_COMMIT_PATH) .direnv  ## Upgrade the project requirements
	python -m pre_commit autoupdate

static/js/%.min.js: assets/typescript/%.ts $(TS_FILES)
	npx esbuild $< --bundle --minify --sourcemap --outfile=$@
	@touch $@

js: $(JS_FILES) ## Fetch and build the js

cog: $(UV_PATH) $(COGABLE) ## Run cog
	@uvx --from cogapp cog -rc $(filter-out $<,$^)

db.sqlite3: .direnv $(MIGRATION_FILES)
	python manage.py migrate
	@touch $@

dev: .direnv db.sqlite3 css js ## Setup the project read for development

node_modules: package.json package-lock.json
	npm install
	@touch $@

lcov.info: .FORCE .direnv
	python -m pytest --cov=. --cov-report=lcov:lcov.info --cov-report=term-missing

coverage: lcov.info ## Run the test suite and generate a coverage report

test: .direnv ## Run the test suite
	python -m pytest --ff --picked
