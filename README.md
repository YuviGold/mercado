# Mercado
Development CLIs open-sourced marketplace

## Install

```bash
python -m pip install mercado
```

## How to use

<!-- [[[cog
import cog
from textwrap import dedent
import subprocess

def print_command(command):
    cog.outl(dedent(f"""
```bash
$ mercado {command}

{subprocess.getoutput(f"./main.py {command}")}
```
    """))

print_command("install gh")

print_command("is-latest docker")

print_command("show minikube")
]]] -->

```bash
$ mercado install gh

[11/01/22 15:16:01] Looking for the latest version of 'gh'                                                                                                
                    Getting installer for tool 'gh' with version v2.18.1 for linux and x86_64                                                             
[11/01/22 15:16:02] Installing 'gh'...                                                                                                                    
[11/01/22 15:16:03] Downloading 'gh' to /tmp/gh_2.18.1_linux_amd64.tar.gz (size: 9.2 MB)                                                                  
Downloading... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
[11/01/22 15:16:04] Unpacking /tmp/gh_2.18.1_linux_amd64.tar.gz to /tmp/gh_2.18.1_linux_amd64.tar                                                         
                    Copying /tmp/gh_2.18.1_linux_amd64.tar/gh_2.18.1_linux_amd64/bin/gh to /home/yuvalgold/.mercado/gh                                    
👍       'gh' version v2.18.1 is installed
```


```bash
$ mercado is-latest docker

👎       'docker' version 'v20.10.21' is available! (current: 20.10.18)
```


```bash
$ mercado show gh

Name: gh
Installed: ✅
Local Version: 2.18.1
Path: /home/yuvalgold/.mercado/gh
Remote Version: v2.18.1
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

### Run GHA

I use [nektos/act](https://github.com/nektos/act) tool to run the Git Hub Action locally.
By default, act runs on a slim container image, for docker-compose usage the base image is replaced.

```bash
act --platform=ubuntu-latest=lucasalt/act_base:latest
```
