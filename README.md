# Mercado
All-In-One Development CLI Tools Multi-platform Marketplace

Stop memorizing whether that's `apt install` or `brew` or any other package manager that takes too long whenever only to get an outdated tool - and use `mercado` instead!

All the most used tools by developers like `docker`, `terraform`, and `kubectl`.

- Supports different types of installations
  - **GitHub releases**
  - **Hashicorp products**
  - **URL fetching**
  - **Customized shell scripts**
- **Multi-platform multi-architectures** installations
- Install the **latest artifact** or a specific version
- HTTP calls with retry mechanismand timeouts
- Archive unpacking
- Elaborated logs with timestamps of every step in the process
- CI first
  - Every artifact is verified on a daily basis
  - README is dynamically generated so docs can't get broken


## Supported Tools

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

print_command("list --names-only --all")

]]] -->

```bash
$ mercado list --names-only --all

Mercado tools 
┏━━━━━━━━━━━━┓
┃ Name       ┃
┡━━━━━━━━━━━━┩
│ compose    │
│ consul     │
│ cosign     │
│ docker     │
│ gh         │
│ helm       │
│ k3d        │
│ kind       │
│ kubectl    │
│ minikube   │
│ packer     │
│ terraform  │
│ terragrunt │
│ tfsec      │
│ trivy      │
│ vagrant    │
│ vault      │
│ waypoint   │
└────────────┘
```

<!-- [[[end]]] -->

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
$ {command}

{subprocess.getoutput(command)}
```
    """))

print_command("mercado list --verbose")

print_command("mercado install gh")

print_command("mercado is-latest docker")

print_command("mercado show minikube")

print_command("mercado list --label k8s --with-labels --all")

]]] -->

```bash
$ mercado list --verbose

                                       Mercado tools                                        
┏━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name       ┃ Vendor     ┃ Installed                                                      ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ compose    │ GitHub     │ ⏫ (/home/yuvalgold/.docker/cli-plugins/docker-compose 2.13.0) │
│ gh         │ GitHub     │ ✅ (/home/yuvalgold/.mercado/gh 2.25.1)                        │
│ kind       │ GitHub     │ ✅ (/home/yuvalgold/.mercado/kind 0.18.0)                      │
│ minikube   │ GitHub     │ ✅ (/home/yuvalgold/.mercado/minikube 1.29.0)                  │
│ terragrunt │ GitHub     │ ⏫ (/home/yuvalgold/.mercado/terragrunt 0.42.5)                │
├────────────┼────────────┼────────────────────────────────────────────────────────────────┤
│ consul     │ Hashicorp  │ ⏫ (/usr/local/bin/consul 1.13.1)                              │
│ terraform  │ Hashicorp  │ ✅ (/home/yuvalgold/.mercado/terraform 1.4.4)                  │
│ vagrant    │ Hashicorp  │ ⏫ (/home/yuvalgold/.mercado/vagrant 2.3.2)                    │
│ vault      │ Hashicorp  │ ✅ (/home/yuvalgold/.mercado/vault 1.13.1)                     │
├────────────┼────────────┼────────────────────────────────────────────────────────────────┤
│ kubectl    │ URLFetcher │ ⏫ (/home/yuvalgold/.mercado/kubectl 1.25.3)                   │
├────────────┼────────────┼────────────────────────────────────────────────────────────────┤
│ docker     │ Shell      │ ⏫ (/usr/bin/docker 23.0.1)                                    │
│ helm       │ Shell      │ ⏫ (/home/yuvalgold/.mercado/helm 3.11.0)                      │
└────────────┴────────────┴────────────────────────────────────────────────────────────────┘
```


```bash
$ mercado install gh

[03/31/23 17:18:48] Looking for the latest version of 'gh'                                                                                                                                                 
[03/31/23 17:18:49] Getting installer for tool 'gh' with version v2.25.1 for linux and x86_64                                                                                                              
                    Installing 'gh'...                                                                                                                                                                     
[03/31/23 17:18:50] Downloading 'gh' to /tmp/gh_2.25.1_linux_amd64.tar.gz (size: 10.1 MB)                                                                                                                  
Downloading... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
[03/31/23 17:18:51] Unpacking /tmp/gh_2.25.1_linux_amd64.tar.gz to /tmp/gh_2.25.1_linux_amd64.tar                                                                                                          
                    Copying /tmp/gh_2.25.1_linux_amd64.tar/gh_2.25.1_linux_amd64/bin/gh to /home/yuvalgold/.mercado/gh                                                                                     
👍       'gh' version v2.25.1 is installed
```


```bash
$ mercado is-latest docker

👎       'docker' version 'v23.0.2' is available! (current: 23.0.1)
```


```bash
$ mercado show minikube

Name: minikube
Status: ✅
Local Version: 1.29.0
Path: /home/yuvalgold/.mercado/minikube
Remote Version: v1.29.0
```


```bash
$ mercado list --label k8s --with-labels --all

                   Mercado tools                   
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Name     ┃ Labels                   ┃ Installed ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ helm     │ k8s                      │ ⏫        │
│ k3d      │ k8s,docker,orchestration │ ❌        │
│ kind     │ k8s,docker,orchestration │ ✅        │
│ kubectl  │ k8s                      │ ⏫        │
│ minikube │ k8s,orchestration        │ ✅        │
└──────────┴──────────────────────────┴───────────┘
```

<!-- [[[end]]] -->

## Contribute

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
By default, act runs on a slim container image, for docker-compose usage the base image is replaced.

```bash
act --platform=ubuntu-latest=lucasalt/act_base:latest -j <JOB>
```

## Generate docs

1. Install dist locally
1. Run inside virtualenv

```bash
make docs
```
