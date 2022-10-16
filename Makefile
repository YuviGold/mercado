all: verify dist

verify: fmt lint test

lint:
	python -m flake8 --max-line-length 120 mercado
	git diff --exit-code

fmt:
	find mercado -name '*.py' -exec autopep8 -i {} \;

test:
	echo 'test pytest'

install: clean dist
	pip install --force-reinstall ./dist/mercado-*.whl

.PHONY: dist
dist:
	./setup.py bdist_wheel

clean:
	-rm -rf dist build *.egg-info
