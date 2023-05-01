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
$ {command}

{subprocess.getoutput(command)}
```
    """))

print_command("mercado list --names-only --all")

]]] -->

```bash
$ mercado list --names-only --all

Mercado tools 
┏━━━━━━━━━━━━┓
┃ Name       ┃
┡━━━━━━━━━━━━┩
│ aws        │
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
┏━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name       ┃ Vendor     ┃ Installed                                                   ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ compose    │ GitHub     │ ✅ (/home/yuvalg/.docker/cli-plugins/docker-compose 2.17.3) │
│ gh         │ GitHub     │ ✅ (/home/yuvalg/.mercado/gh 2.28.0)                        │
│ kind       │ GitHub     │ ✅ (/home/yuvalg/.mercado/kind 0.18.0)                      │
│ minikube   │ GitHub     │ ✅ (/home/yuvalg/.mercado/minikube 1.30.1)                  │
│ terragrunt │ GitHub     │ ⏫ (/home/yuvalg/.mercado/terragrunt 0.42.5)                │
│ trivy      │ GitHub     │ ⏫ (/home/yuvalg/.mercado/trivy 0.32.1)                     │
├────────────┼────────────┼─────────────────────────────────────────────────────────────┤
│ consul     │ Hashicorp  │ ⏫ (/home/yuvalg/.mercado/consul 1.13.1)                    │
│ terraform  │ Hashicorp  │ ✅ (/home/yuvalg/.mercado/terraform 1.4.6)                  │
│ vagrant    │ Hashicorp  │ ⏫ (/home/yuvalg/.mercado/vagrant 2.3.2)                    │
│ vault      │ Hashicorp  │ ✅ (/home/yuvalg/.mercado/vault 1.13.2)                     │
├────────────┼────────────┼─────────────────────────────────────────────────────────────┤
│ kubectl    │ URLFetcher │ ⏫ (/usr/local/bin/kubectl 1.18.3)                          │
├────────────┼────────────┼─────────────────────────────────────────────────────────────┤
│ aws        │ Shell      │ ✅ (/home/yuvalg/.mercado/aws 2.11.16)                      │
│ docker     │ Shell      │ ⏫ (/usr/bin/docker 20.10.12)                               │
│ helm       │ Shell      │ ⏫ (/home/yuvalg/.mercado/helm 3.11.0)                      │
└────────────┴────────────┴─────────────────────────────────────────────────────────────┘
```


```bash
$ mercado install gh

[05/01/23 19:19:10] Looking for the latest version of 'gh'                                                                                                                                                 
                    Getting installer for tool 'gh' with version v2.28.0 for linux and x86_64                                                                                                              
[05/01/23 19:19:11] Installing 'gh'...                                                                                                                                                                     
[05/01/23 19:19:12] Downloading 'gh' to /tmp/gh_2.28.0_linux_amd64.tar.gz (size: 10.1 MB)                                                                                                                  
Downloading... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
[05/01/23 19:19:13] Unpacking /tmp/gh_2.28.0_linux_amd64.tar.gz to /tmp/gh_2.28.0_linux_amd64.tar                                                                                                          
[05/01/23 19:19:14] Copying /tmp/gh_2.28.0_linux_amd64.tar/gh_2.28.0_linux_amd64/bin/gh to /home/yuvalg/.mercado/gh                                                                                        
👍       'gh' version v2.28.0 is installed
```


```bash
$ mercado is-latest docker

👎       'docker' version 'v23.0.5' is available! (current: 20.10.12)
```


```bash
$ mercado show minikube

Name: minikube
Status: ✅
Local Version: 1.30.1
Path: /home/yuvalg/.mercado/minikube
Remote Version: v1.30.1
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
