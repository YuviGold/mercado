COMPOSE = docker compose

all: verify dist

.PHONY: help
help:
	@awk -f ./hack/help.awk $(MAKEFILE_LIST)

##@ code

.PHONY: verify
verify: format lint test  ## run all verifications

.PHONY: test
test: ## run tests
	$(MAKE) -s _docker_$@

.PHONY: format
format: ## run formatter
	$(MAKE) -s _docker_$@

.PHONY: lint
lint: ## run linter
	$(MAKE) -s _docker_$@

##@ artifact

.PHONY: install
install: clean dist ## install package locally
	$(MAKE) -s _$@

.PHONY: dist
dist: ## generate package artifacts
	$(MAKE) -s _$@

.PHONY: docs
docs:  ## generate documentation
	$(MAKE) -s _$@

.PHONY: deploy
deploy: dist  ## deploy Python package to PyPI
	$(MAKE) -s _$@

##@ general

.PHONY: deps
deps:  ## install dependencies
	$(MAKE) -s _$@	

.PHONY: clean
clean:  ## clean environment
	-$(MAKE) -s _$@

_docker_%:
	${COMPOSE} build test && ${COMPOSE} run --rm test make _$*

_%:
	./hack/$*.sh
