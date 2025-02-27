from os import environ
from pathlib import Path

from .utils import INSTALL_DIR, PACKAGES_DIR, fetch_url, is_arm64_arch, is_darwin_os, search_version
from .vendors.github import GitHub, GitHubTool
from .vendors.hashicorp import Hashicorp
from .vendors.shell import Shell, ShellTool
from .vendors.url_fetcher import URLFetcher, URLFetcherTool
from .vendors.vendor import Label, Tool, ToolVendor

TOOLS: dict[ToolVendor, list[Tool]] = {
    GitHub(): [
        GitHubTool("kind", labels=(Label.K8S, Label.DOCKER, Label.ORCHESTRATE), repository="kubernetes-sigs/kind"),
        GitHubTool("gh", labels=(Label.VCS,), repository="cli/cli"),
        GitHubTool("k3d", labels=(Label.K8S, Label.DOCKER, Label.ORCHESTRATE), repository="k3d-io/k3d"),
        GitHubTool("cosign", labels=(Label.SECURITY,), repository="sigstore/cosign"),
        GitHubTool("terragrunt", labels=(Label.IAC,), repository="gruntwork-io/terragrunt"),
        GitHubTool("trivy", labels=(Label.SECURITY,), repository="aquasecurity/trivy"),
        GitHubTool(
            "tfsec",
            labels=(Label.SECURITY,),
            repository="aquasecurity/tfsec",
            asset_template=lambda os, arch: f"tfsec-{os}-{arch}",
        ),
        GitHubTool("minikube", labels=(Label.K8S, Label.ORCHESTRATE), repository="kubernetes/minikube"),
        GitHubTool(
            "compose",
            labels=(Label.VIRT, Label.DOCKER, Label.ORCHESTRATE),
            repository="docker/compose",
            target=Path(environ.get("DOCKER_CONFIG", Path.home() / ".docker")) / "cli-plugins/docker-compose",
        ),
        GitHubTool("k9s", labels=(Label.K8S,), repository="derailed/k9s"),
        GitHubTool("k8sgpt", labels=(Label.K8S,), repository="k8sgpt-ai/k8sgpt"),
        GitHubTool("colima", labels=(Label.DOCKER,), repository="abiosoft/colima"),
        GitHubTool("task", labels=(Label.BUILD,), repository="go-task/task"),
        GitHubTool("sops", labels=(Label.SECURITY,), repository="getsops/sops"),
    ],
    Hashicorp(): [
        Tool("vagrant", labels=(Label.VIRT,)),
        Tool("vault", labels=(Label.SECURITY,)),
        Tool("terraform", labels=(Label.IAC,)),
        Tool("packer", labels=(Label.VIRT,)),
        Tool("waypoint", labels=(Label.CICD,)),
        Tool(
            "consul",
            labels=(
                Label.STORAGE,
                Label.NETWORK,
            ),
        ),
    ],
    URLFetcher(): [
        URLFetcherTool(
            "kubectl",
            labels=(Label.K8S,),
            get_latest_version_url="https://storage.googleapis.com/kubernetes-release/release/stable.txt",
            get_release_by_version_url=lambda os,
            arch,
            version: f"https://storage.googleapis.com/kubernetes-release/release/{version}/bin/{os}/{arch}/kubectl",
        ),
    ],
    Shell(): [
        ShellTool(
            "helm",
            labels=(Label.K8S,),
            env_vars={"USE_SUDO": "false", "HELM_INSTALL_DIR": str(INSTALL_DIR)},
            get_latest_version=lambda: GitHub().get_latest_version(GitHubTool("helm", repository="helm/helm")),
            download_script=lambda version, os, arch: f"""
                  curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
                  chmod 700 get_helm.sh
                  ./get_helm.sh --version {version}
                  """,
        ),
        ShellTool(
            "docker",
            labels=(Label.VIRT, Label.DOCKER),
            get_latest_version=lambda: GitHub().get_latest_version(GitHubTool("moby", repository="moby/moby")),
            download_script=lambda version, os, arch: f"""
                  curl -fsSL https://get.docker.com -o get-docker.sh
                  VERSION={version} sh get-docker.sh
                  """
            if not is_darwin_os(os)
            else f"""
                    arch={"aarch64" if is_arm64_arch(arch) else "x86_64"}
                    curl "https://download.docker.com/mac/static/stable/${{arch}}/docker-{version.lstrip("v")}.tgz" \\
                        -o docker.tgz
                    tar -xf docker.tgz
                    find . -type f -name docker -exec mv {{}} {INSTALL_DIR / "docker"!s} \\;
                  """,
        ),
        ShellTool(
            "aws",
            labels=(Label.CLOUD,),
            get_latest_version=lambda: search_version(
                fetch_url("https://awscli.amazonaws.com/latest/", raise_for_status=False),
            ),
            download_script=lambda version, os, arch: f"""
                  curl "https://awscli.amazonaws.com/awscli-exe-linux-{arch}-{version}.zip" -o "awscliv2.zip"
                  unzip -q awscliv2.zip
                  ./aws/install --bin-dir {INSTALL_DIR!s} --install-dir {INSTALL_DIR / "aws-cli"!s} --update
                  """
            if not is_darwin_os(os)
            else f"""
                    curl "https://awscli.amazonaws.com/AWSCLIV2-{version}.pkg" -o "AWSCLIV2.pkg"
                  tar -xf AWSCLIV2.pkg
                  pkg_dir={PACKAGES_DIR / "aws-cli"!s}
                  mkdir -p ${{pkg_dir}}
                  find . -type f -name Payload -exec tar -xf {{}} -C ${{pkg_dir}} \\;
                  ln -f -s `find ${{pkg_dir}} -type f -name aws` {INSTALL_DIR / "aws"!s}
                  """,
        ),
    ],
}
