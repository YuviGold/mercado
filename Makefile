all: verify dist

verify: format lint test

test format lint:
	docker-compose build test && docker-compose run --rm test make _$@

_lint:
	python -m flake8 --max-line-length 120 mercado tests
	git diff --shortstat --exit-code

_format:
	find mercado -name '*.py' -exec autopep8 --max-line-length 120 -i {} \;

_test:
	python -m pytest --log-cli-level=$(or ${LOGLEVEL},info) -s --verbose $(or ${TEST},tests) -k $(or ${TEST_FUNC},'')

install: clean dist
	pip install --force-reinstall ./dist/mercado-*.whl

.PHONY: dist
dist:
	./setup.py bdist_wheel

deploy: dist
	python -m twine upload --verbose dist/*

clean:
	-rm -rf dist build *.egg-info
