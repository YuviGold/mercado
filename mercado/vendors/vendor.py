from dataclasses import dataclass


@dataclass
class Product:
    name: str
    # os: str
    # arch: str
    version: str
    url: str

# TODO: Support OS / Arch


class ToolVendor:
    def get_supported_products(self) -> list[str]:
        ...

    def get_latest_release(self, name: str) -> Product:
        ...

    def get_release_by_version(self, name: str, version: str) -> Product:
        ...
