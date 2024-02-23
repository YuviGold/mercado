# Mercado
All-In-One Development CLI Tools Multi-platform Marketplace

<img src="docs/demo.gif" width="900"/>

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
│ k8sgpt     │
│ k9s        │
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
python3 -m pip install mercado
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
┏━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name       ┃ Installed ┃ Is Latest ┃ Version ┃ Path                                                ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ compose    │ ✅        │ 🔼        │ 2.20.3  │ /Users/yuvalgold/.docker/cli-plugins/docker-compose │
│ gh         │ ✅        │ ✅        │ 2.44.1  │ /Users/yuvalgold/.mercado/gh                        │
│ k3d        │ ✅        │ ✅        │ 5.6.0   │ /Users/yuvalgold/.mercado/k3d                       │
│ k8sgpt     │ ✅        │ ✅        │ 0.3.27  │ /Users/yuvalgold/.mercado/k8sgpt                    │
│ k9s        │ ✅        │ 🔼        │ 0.31.8  │ /Users/yuvalgold/.mercado/k9s                       │
│ kind       │ ✅        │ 🔼        │ 0.21.0  │ /Users/yuvalgold/.mercado/kind                      │
│ terragrunt │ ✅        │ 🔼        │ 0.50.3  │ /Users/yuvalgold/.mercado/terragrunt                │
├────────────┼───────────┼───────────┼─────────┼─────────────────────────────────────────────────────┤
│ terraform  │ ✅        │ 🔼        │ 1.7.3   │ /Users/yuvalgold/.mercado/terraform                 │
│ vagrant    │ ✅        │ 🔼        │ 2.3.7   │ /Users/yuvalgold/.mercado/vagrant                   │
│ vault      │ ✅        │ 🔼        │ 1.14.1  │ /Users/yuvalgold/.mercado/vault                     │
├────────────┼───────────┼───────────┼─────────┼─────────────────────────────────────────────────────┤
│ kubectl    │ ✅        │ 🔼        │ 1.28.2  │ /Users/yuvalgold/.mercado/kubectl                   │
├────────────┼───────────┼───────────┼─────────┼─────────────────────────────────────────────────────┤
│ aws        │ ✅        │ 🔼        │ 2.15.19 │ /Users/yuvalgold/.mercado/aws                       │
│ docker     │ ✅        │ ✅        │ 25.0.3  │ /Users/yuvalgold/.mercado/docker                    │
│ helm       │ ✅        │ 🔼        │ 3.14.0  │ /Users/yuvalgold/.mercado/helm                      │
└────────────┴───────────┴───────────┴─────────┴─────────────────────────────────────────────────────┘
```


```bash
$ mercado install gh

[02/22/24 18:07:35] Looking for the latest version of 'gh'                                                                                         
[02/22/24 18:07:36] Getting installer for tool 'gh' with version v2.44.1 for darwin and arm64                                                      
                    Installing 'gh'...                                                                                                             
[02/22/24 18:07:37] Downloading 'gh' to /var/folders/v5/mbdkcsy10c7b_g08jp498ww00000gn/T/gh_2.44.1_macOS_arm64.zip (size: 10.9 MB)                 
Downloading... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
[02/22/24 18:07:40] Unpacking /var/folders/v5/mbdkcsy10c7b_g08jp498ww00000gn/T/gh_2.44.1_macOS_arm64.zip to                                        
                    /var/folders/v5/mbdkcsy10c7b_g08jp498ww00000gn/T/gh_2.44.1_macOS_arm64                                                         
                    Copying /var/folders/v5/mbdkcsy10c7b_g08jp498ww00000gn/T/gh_2.44.1_macOS_arm64/gh_2.44.1_macOS_arm64/bin/gh to                 
                    /Users/yuvalgold/.mercado/gh                                                                                                   
👍      'gh' version v2.44.1 is installed
```


```bash
$ mercado is-latest docker

👍      You have the latest version of 'docker' (25.0.3)
```


```bash
$ mercado show minikube

Name: minikube
Status: ❌
Remote Version: 
```


```bash
$ mercado list --label k8s --with-labels --all

                   Mercado tools                   
┏━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name     ┃ Installed ┃ Labels                   ┃
┡━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ helm     │ ✅        │ k8s                      │
│ k3d      │ ✅        │ k8s,docker,orchestration │
│ k8sgpt   │ ✅        │ k8s                      │
│ k9s      │ ✅        │ k8s                      │
│ kind     │ ✅        │ k8s,docker,orchestration │
│ kubectl  │ ✅        │ k8s                      │
│ minikube │ ❌        │ k8s,orchestration        │
└──────────┴───────────┴──────────────────────────┘
```

<!-- [[[end]]] -->

## Contributing

Please see the [CONTRIBUTING guide](https://github.com/alexellis/arkade/blob/master/CONTRIBUTING.md).
