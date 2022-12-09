# Mercado
All-In-One Development CLI Tools Multi-platform Marketplace

Stop remembering if that's `apt install` or `brew` that takes long whenever it has install recommendations only to get an outdated tool - and use `mercado` instead!

All the most used tools by developers like `docker`, `terraform`, and `kubectl`.

- Supports multi-platform multi-architectures installations
- Install the latest artifact or a specific version
- HTTP calls with retry mechanismand timeouts
- Unpacking archives
- Elaborated logs with timestamps of every step in the process
- Supports different types of installations
  - **GitHub releases**
  - **Hashicorp products**
  - **URL fetching**
  - **Customized shell scripts**
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

print_command("list --names-only")

]]] -->

```bash
$ mercado list --names-only

Mercado tools 
┏━━━━━━━━━━━━┓
┃ Name       ┃
┡━━━━━━━━━━━━┩
│ compose    │
│ cosign     │
│ gh         │
│ k3d        │
│ kind       │
│ minikube   │
│ terragrunt │
│ tfsec      │
│ trivy      │
│ consul     │
│ packer     │
│ terraform  │
│ vagrant    │
│ vault      │
│ waypoint   │
│ kubectl    │
│ docker     │
│ helm       │
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
$ mercado {command}

{subprocess.getoutput(f"./main.py {command}")}
```
    """))

print_command("install gh")

print_command("is-latest docker")

print_command("show minikube")

print_command("list --label k8s --with-labels")

print_command("list --installed-only --verbose")

]]] -->

```bash
$ mercado install gh

[12/10/22 00:09:44] Looking for the latest version of 'gh'                                                                                                       
[12/10/22 00:09:45] Getting installer for tool 'gh' with version v2.20.2 for linux and x86_64                                                                    
                    Installing 'gh'...                                                                                                                           
[12/10/22 00:09:46] Downloading 'gh' to /tmp/gh_2.20.2_linux_amd64.tar.gz (size: 9.6 MB)                                                                         
Downloading... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
[12/10/22 00:09:51] Unpacking /tmp/gh_2.20.2_linux_amd64.tar.gz to /tmp/gh_2.20.2_linux_amd64.tar                                                                
                    Copying /tmp/gh_2.20.2_linux_amd64.tar/gh_2.20.2_linux_amd64/bin/gh to /home/yuvalgold/.mercado/gh                                           
👍       'gh' version v2.20.2 is installed
```


```bash
$ mercado is-latest docker

👍       You have the latest version of 'docker' (20.10.21)
```


```bash
$ mercado show minikube

Name: minikube
Installed: ✅
Local Version: 1.27.1
Path: /home/yuvalgold/.mercado/minikube
Remote Version: v1.28.0
```


```bash
$ mercado list --label k8s --with-labels

                   Mercado tools                   
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Name     ┃ Labels                   ┃ Installed ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ k3d      │ k8s,docker,orchestration │ ❌        │
│ kind     │ k8s,docker,orchestration │ ✅        │
│ minikube │ k8s,orchestration        │ ✅        │
│ kubectl  │ k8s                      │ ✅        │
│ helm     │ k8s                      │ ❌        │
└──────────┴──────────────────────────┴───────────┘
```


```bash
$ mercado list --installed-only --verbose

                                       Mercado tools                                       
┏━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name      ┃ Vendor     ┃ Installed                                                      ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ compose   │ GitHub     │ ✅ (/home/yuvalgold/.docker/cli-plugins/docker-compose 2.13.0) │
│ gh        │ GitHub     │ ✅ (/home/yuvalgold/.mercado/gh 2.20.2)                        │
│ kind      │ GitHub     │ ✅ (/home/yuvalgold/.mercado/kind 0.17.0)                      │
│ minikube  │ GitHub     │ ✅ (/home/yuvalgold/.mercado/minikube 1.27.1)                  │
├───────────┼────────────┼────────────────────────────────────────────────────────────────┤
│ consul    │ Hashicorp  │ ✅ (/usr/local/bin/consul 1.13.1)                              │
│ terraform │ Hashicorp  │ ✅ (/home/yuvalgold/.mercado/terraform 1.3.3)                  │
│ vagrant   │ Hashicorp  │ ✅ (/home/yuvalgold/.mercado/vagrant 2.3.2)                    │
│ vault     │ Hashicorp  │ ✅ (/home/yuvalgold/.mercado/vault 1.12.1)                     │
├───────────┼────────────┼────────────────────────────────────────────────────────────────┤
│ kubectl   │ URLFetcher │ ✅ (/home/yuvalgold/.mercado/kubectl 1.25.3)                   │
├───────────┼────────────┼────────────────────────────────────────────────────────────────┤
│ docker    │ Shell      │ ✅ (/usr/bin/docker 20.10.21)                                  │
└───────────┴────────────┴────────────────────────────────────────────────────────────────┘
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

## Generate docs

1. Install dist locally
1. Run inside virtualenv

```bash
pip install cogapp
make docs
```
