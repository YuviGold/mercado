# Mercado
Development CLIs open-sourced marketplace

## Install

```bash
python -m pip install mercado
```

## Test

The tests are running with pytest inside of a docker-compose container

```bash
make test

# Run a specific test file with TEST=</path/to/file>
TEST=./tests/test_github.py make test

# Run a tests matching an expression TEST_FUNC=<expression>
TEST_FUNC="invalid" make test

# Add more verbose logs
LOGLEVEL=debug make test
```

### Run locally

```bash
virtualenv .venv
source .venv/bin/activate
pip install -r dev-requirements.txt -r requirements.txt
./main.py --help
```

### Install dist locally

```bash
make install

mercado --help
```
