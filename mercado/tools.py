
from .vendors.github import GitHub, GitHubTool
from .vendors.hashicorp import Hashicorp
from .vendors.url_fetcher import URLFetcher, URLFetcherTool
from .vendors.vendor import Label, Tool, ToolVendor

TOOLS: dict[ToolVendor, list[Tool]] = {
    GitHub(): [
        GitHubTool('kind', labels=[Label.K8S], repository='kubernetes-sigs/kind'),
        GitHubTool('gh', labels=[Label.VCS], repository='cli/cli'),
        GitHubTool('k3d', labels=[Label.K8S], repository='k3d-io/k3d'),
        GitHubTool('cosign', labels=[Label.SECURITY], repository='sigstore/cosign'),
        GitHubTool('terragrunt', labels=[Label.IAC], repository='gruntwork-io/terragrunt'),
        GitHubTool('trivy', labels=[Label.SECURITY], repository='aquasecurity/trivy'),
        GitHubTool('tfsec', labels=[Label.SECURITY], repository='aquasecurity/tfsec',
                   asset_template=lambda os, arch: f'tfsec-{os}-{arch}'),
    ],

    Hashicorp(): [
        Tool('vagrant', labels=[Label.VIRT]),
        Tool('vault', labels=[Label.SECURITY]),
        Tool('terraform', labels=[Label.IAC]),
        Tool('packer', labels=[Label.VIRT]),
        Tool('waypoint', labels=[Label.CICD]),
    ],

    URLFetcher(): [
        URLFetcherTool('kubectl', labels=[Label.K8S],
                       get_latest_version_url='https://storage.googleapis.com/kubernetes-release/release/stable.txt',
                       get_release_by_version_url=lambda os, arch, version:
                       f"https://storage.googleapis.com/kubernetes-release/release/{version}/bin/{os}/{arch}/kubectl",
                       ),
    ],
}
