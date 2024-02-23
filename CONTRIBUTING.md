# Contribute

<!-- [[[cog
import cog
from textwrap import dedent
import subprocess

def print_command(command):
    cog.outl(dedent(f"""
```bash
$ {command}

{subprocess.getoutput(command)}
```
    """))

print_command("TERM='' make -s help")
]]] -->

```bash
$ TERM='' make -s help


Usage:
  make <target>

code
  verify                run all verifications
  test                  run tests
  format                run formatter
  lint                  run linter

artifact
  install               install package locally
  dist                  generate package artifacts
  docs                  generate documentation
  deploy                deploy Python package to PyPI

general
  deps                  install dependencies
  clean                 clean environment

```

<!-- [[[end]]] -->

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
poetry run mercado --help
```

### Install dist locally

```bash
make install

mercado --help
```

### Run GHA

I use [nektos/act](https://github.com/nektos/act) tool to run the Git Hub Action locally.

```bash
act -j <JOB>
```

In order to run a specific test, set the appropriate OS and environment variable

```bash
act -j test --env TEST_FUNC=k3d --matrix os:ubuntu-latest
```

When local execution does not help, we can enable a remote debug with [tmate](https://github.com/marketplace/actions/debugging-with-tmate)

```bash
gh workflow run Test --ref <branch_name> -f debug_enabled=true
```

## Generate docs

Generate the README with [cog](https://github.com/nedbat/cog)

1. Install dist locally
1. Run inside virtualenv

```bash
make docs
```

Record video with [asciinema](https://asciinema.org/)

```bash
asciinema rec docs/demo.cast

mercado is-latest kind
mercado install kind
mercado show kind
mercado list --label k8s --verbose --all

ctrl + d
```

Then use [gifcast](https://dstein64.github.io/gifcast/) to convert the `.cast` file to `.gif`
shave 10 rows from the bottom and 5 from the right.
