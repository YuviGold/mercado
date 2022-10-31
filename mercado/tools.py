
from .utils import INSTALL_DIR

from .vendors.github import GitHub, GitHubTool
from .vendors.hashicorp import Hashicorp
from .vendors.shell import Shell, ShellTool
from .vendors.url_fetcher import URLFetcher, URLFetcherTool
from .vendors.vendor import Label, Tool, ToolVendor

TOOLS: dict[ToolVendor, list[Tool]] = {
    GitHub(): [
        GitHubTool('kind', labels=(Label.K8S,), repository='kubernetes-sigs/kind'),
        GitHubTool('gh', labels=(Label.VCS,), repository='cli/cli'),
        GitHubTool('k3d', labels=(Label.K8S,), repository='k3d-io/k3d'),
        GitHubTool('cosign', labels=(Label.SECURITY,), repository='sigstore/cosign'),
        GitHubTool('terragrunt', labels=(Label.IAC,), repository='gruntwork-io/terragrunt'),
        GitHubTool('trivy', labels=(Label.SECURITY,), repository='aquasecurity/trivy'),
        GitHubTool('tfsec', labels=(Label.SECURITY,), repository='aquasecurity/tfsec',
                   asset_template=lambda os, arch: f'tfsec-{os}-{arch}'),
        GitHubTool('minikube', labels=(Label.SECURITY,), repository='kubernetes/minikube'),
    ],

    Hashicorp(): [
        Tool('vagrant', labels=(Label.VIRT,)),
        Tool('vault', labels=(Label.SECURITY,)),
        Tool('terraform', labels=(Label.IAC,)),
        Tool('packer', labels=(Label.VIRT,)),
        Tool('waypoint', labels=(Label.CICD,)),
    ],

    URLFetcher(): [
        URLFetcherTool('kubectl', labels=(Label.K8S,),
                       get_latest_version_url='https://storage.googleapis.com/kubernetes-release/release/stable.txt',
                       get_release_by_version_url=lambda os, arch, version:
                       f"https://storage.googleapis.com/kubernetes-release/release/{version}/bin/{os}/{arch}/kubectl",
                       ),
    ],

    Shell(): [
        ShellTool("helm", labels=(Label.K8S,),
                  env_vars={"USE_SUDO": "false", "HELM_INSTALL_DIR": INSTALL_DIR},
                  get_latest_version=lambda: GitHub().get_latest_version(GitHubTool('helm', repository='helm/helm')),
                  download_script=lambda version: f"""
                  curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
                  chmod 700 get_helm.sh
                  ./get_helm.sh --version {version}
                  """
                  ),
    ]
}
