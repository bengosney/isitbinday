.PHONY: help clean test install init dev all cog coverage git-hooks upgrade
.DEFAULT_GOAL := dev
.PRECIOUS: requirements.%.txt
.FORCE:

REQS=$(shell python -c "import tomllib; print(' '.join(f'requirements.{k}.txt' for k in tomllib.load(open('pyproject.toml', 'rb')).get('project', {}).get('optional-dependencies', {}).keys()))")

PYTHON_VERSION:=$(shell cat .python-version)
UV_PATH:=~/.cargo/bin/uv
VENV_PATH:=.venv
VENV_LOCK:=$(VENV_PATH)/.install_lock
PYTHON_PATH:=$(VENV_PATH)/bin/python
PRE_COMMIT_PATH:=$(VENV_PATH)/bin/pre-commit

COGABLE:=$(shell git ls-files | xargs grep -l "\[\[\[cog")
MIGRATION_FILES:=$(shell ls -d -- **/migrations/*.py)

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.gitignore:
	curl -sS "https://www.toptal.com/developers/gitignore/api/visualstudiocode,python,direnv" > $@

.git: .gitignore
	git init

.pre-commit-config.yaml: | $(PRE_COMMIT_PATH) .git
	curl -sS https://gist.githubusercontent.com/bengosney/4b1f1ab7012380f7e9b9d1d668626143/raw/.pre-commit-config.yaml > $@
	$(PRE_COMMIT_PATH) autoupdate
	@touch $@

.git/hooks/%: .git $(PRE_COMMIT_PATH) .pre-commit-config.yaml
	$(PRE_COMMIT_PATH) install --hook-type $(notdir $@)

.git/hooks/prepare-commit-msg:
	wget -O $@ https://raw.githubusercontent.com/commitizen-tools/commitizen/master/hooks/$(notdir $@).py
	chmod +x $@

.git/hooks/post-commit:
	wget -O $@ https://raw.githubusercontent.com/commitizen-tools/commitizen/master/hooks/$(notdir $@).py
	chmod +x $@

git-hooks: .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/prepare-commit-msg .git/hooks/post-commit ## Install git hooks

pyproject.toml: | $(UV_PATH)
	curl -sS https://gist.githubusercontent.com/bengosney/f703f25921628136f78449c32d37fcb5/raw/pyproject.toml > $@
	@touch $@

requirements.%.txt: $(UV_PATH) pyproject.toml
	@echo "Building $@"
	$(UV_PATH) pip compile --generate-hashes -q --extra $* -o $@ $(filter-out $<,$^)

requirements.txt: $(UV_PATH) pyproject.toml
	@echo "Building $@"
	$(UV_PATH) pip compile --generate-hashes -q -o $@ $(filter-out $<,$^)

$(VENV_PATH): | $(UV_PATH) .envrc
	$(UV_PATH) venv --managed-python --python $(PYTHON_VERSION)
	@touch $@

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo 'if [ ! -d .venv ]; then' > $@
	@echo '    make .venv' >> $@
	@echo 'fi' >> $@
	@echo '' >> $@
	@echo 'PATH_add ".venv/bin"' >> $@
	@echo 'export VIRTUAL_ENV="$$PWD/.venv"' >> $@
	@echo 'export VIRTUAL_ENV_PROMPT="$$(basename $$PWD)"' >> $@
	@echo 'watch_file .venv' >> $@
	@touch -d '+1 minute' $@
	@false

$(UV_PATH):
	@echo "Error: uv is not installed. Install it from https://github.com/astral-sh/uv" && false

$(PRE_COMMIT_PATH): $(UV_PATH) $(VENV_PATH)
	$(UV_PATH) pip install pre-commit

$(VENV_LOCK): requirements.txt $(REQS) | $(VENV_PATH)
	@echo "Installing $(filter-out $<,$^)"
	$(UV_PATH) pip sync $(filter-out $<,$^)
	@touch $@

init: .envrc $(UV_PATH) requirements.txt $(REQS) $(VENV_LOCK) git-hooks ## Initialise an environment

install: $(VENV_LOCK) ## Install development requirements

all: install ## Install everything

clean: ## Remove all build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -f .testmondata
	rm -rf *.egg-info

cog: $(UV_PATH) $(COGABLE) ## Run cog
	$(UV_PATH) tool run --from cogapp cog -rc $(filter-out $<,$^)

db.sqlite3: $(VENV_LOCK) $(MIGRATION_FILES)
	$(PYTHON_PATH) manage.py migrate
	@touch $@

dev: $(VENV_LOCK) db.sqlite3 ## Set up the project ready for development

upgrade: $(UV_PATH) pyproject.toml $(PRE_COMMIT_PATH) ## Upgrade the project requirements and hooks
	$(UV_PATH) pip compile --generate-hashes -q --upgrade -o requirements.txt pyproject.toml
	$(UV_PATH) pip compile --generate-hashes -q --upgrade --extra dev -o requirements.dev.txt pyproject.toml
	$(PRE_COMMIT_PATH) autoupdate
	@$(MAKE) install

lcov.info: .FORCE $(VENV_LOCK)
	$(PYTHON_PATH) -m pytest --cov=. --cov-report=lcov:lcov.info --cov-report=term-missing

coverage: lcov.info ## Run the test suite and generate a coverage report

test: $(VENV_LOCK) ## Run the test suite
	$(PYTHON_PATH) -m pytest --ff --picked
