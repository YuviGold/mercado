import logging
import platform
import re
import stat
import subprocess
from contextlib import suppress
from functools import cache, partial
from glob import glob
from http import HTTPStatus
from os.path import basename
from pathlib import Path
from shutil import copy, get_unpack_formats, unpack_archive, which
from tempfile import gettempdir
from typing import Callable, Sequence

from humanize import naturalsize
from requests import Session
from requests.adapters import HTTPAdapter
from rich.progress import Progress
from urllib3 import Retry

from .vendors.vendor import Tool

MATRIX_X86_64 = ('amd64', 'x86_64', '64bit')
MATRIX_ARM64 = ('arm64', 'aarch64')
MATRIX_MAC = ('darwin', 'macos')
INSTALL_DIR = Path.home() / ".mercado"
PACKAGES_DIR = INSTALL_DIR / "packages"
PKG_PAYLOAD_FILE = 'Payload'
CHUNK_SIZE = 1024
REQUEST_MAX_TIMEOUT = 10
STREAM_MAX_TIMEOUT = 300
SUBPROCSES_TIMEOUT = 30
SUPPORTED_ARCHIVE_FORMATS: list[str] = sum([format[1] for format in get_unpack_formats()], [])


def get_architecture_variations(arch: str) -> Sequence[str]:
    if arch in MATRIX_X86_64:
        return MATRIX_X86_64
    if arch in MATRIX_ARM64:
        return MATRIX_ARM64
    return [arch]


def get_operating_system_variations(os: str) -> Sequence[str]:
    if os in MATRIX_MAC:
        return MATRIX_MAC
    return [os]


def is_valid_architecture(expected: str, actual: str) -> bool:
    """
    Equalize architectures that their name does not necessarily match
    """
    return contains_ignore_case(actual, get_architecture_variations(expected))


def is_valid_os(expected: str, actual: str) -> bool:
    """
    Equalize operating system that their name does not necessarily match
    """
    return contains_ignore_case(actual, get_operating_system_variations(expected))


def is_amd64_arch(arch: str) -> bool:
    return is_valid_architecture('amd64', arch)


def is_arm64_arch(arch: str) -> bool:
    return is_valid_architecture('arm64', arch)


def is_darwin_os(os: str) -> bool:
    return is_valid_os('darwin', os)


def contains_ignore_case(item: str, lst: Sequence[str]):
    for element in lst:
        if re.search(element, item, re.IGNORECASE):
            return True

    return False


def get_local_version(tool: Tool) -> tuple[str, Path]:
    if tool.target:
        path = tool.target
    else:
        path = default_install_path(tool.name)

    if not path.exists():
        path = which(Path(tool.name))
        if not path:
            raise ValueError(f'{tool.name} could not be found')

    return get_tool_version(path), path


def get_command_version(command: str) -> str:
    res = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=SUBPROCSES_TIMEOUT)
    output = res.stdout.decode().strip()
    try:
        return search_version(output)
    except ValueError:
        raise RuntimeError(f'Could not find a valid version for {command}')


def search_version(text: str) -> str:
    match = re.search(
        r'([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?', text)
    if match:
        return match[0]
    raise ValueError('version could not been found in {text}')


def get_tool_version(path: Path, silent: bool = False) -> str:
    if not which(path):
        raise FileNotFoundError(path)

    commands = [f'{path} --version', f'{path} version']
    for command in commands:
        try:
            return get_command_version(command)
        except RuntimeError as ex:
            if not silent:
                logging.debug(ex)
    raise ValueError(path)


def default_install_path(name: str) -> Path:
    return INSTALL_DIR / name


def is_tool_available(tool: Tool) -> bool:
    if tool.target:
        return tool.target.exists()
    return is_tool_available_in_path(tool.name)


def is_tool_available_in_path(name: str) -> bool:
    return which(name) is not None


def download_url(name: str, url: str, dest: Path):
    dest.parent.mkdir(exist_ok=True, parents=True)

    logging.debug(f'Download {url}')

    with create_session().get(url, stream=True, timeout=STREAM_MAX_TIMEOUT) as r:
        total_length = int(r.headers.get('content-length', 0))

        temp_file = Path(gettempdir()) / basename(url)

        logging.info(f"Downloading '{name}' to {temp_file} (size: {naturalsize(total_length)})")

        with temp_file.open('wb') as file, Progress() as progress:
            task = progress.add_task("Downloading...", total=total_length)
            for data in r.iter_content(chunk_size=CHUNK_SIZE):
                if data:
                    file.write(data)
                progress.advance(task, CHUNK_SIZE)

        should_link = False
        if is_archive(str(temp_file)):
            temp_file = extract_file_from_archive(temp_file, name)

        if is_dmg(str(temp_file)):
            temp_file, should_link = extract_file_from_dmg(temp_file, name)

        if should_link:
            logging.info(f"Linking {temp_file} to {dest}")
            dest.unlink(missing_ok=True)
            dest.symlink_to(temp_file)
        else:
            logging.info(f"Copying {temp_file} to {dest}")
            copy(temp_file, dest)

        dest.chmod(dest.stat().st_mode | stat.S_IEXEC)


def is_archive(path: str) -> bool:
    return any(path.endswith(suffix) for suffix in SUPPORTED_ARCHIVE_FORMATS)


def extract_file_from_archive(path: Path, file_name: str) -> Path:
    unpack_dest = path.with_suffix('')
    unpack_dest.mkdir(exist_ok=True)
    logging.info(f"Unpacking {path} to {unpack_dest}")
    unpack_archive(path, extract_dir=unpack_dest)
    matches = glob(f"{unpack_dest}/**/{file_name}", recursive=True)
    assert len(matches) == 1, f"There should be one file in the archive with the name {file_name}"
    return Path(matches[0])


def is_dmg(path: str) -> bool:
    return path.endswith('.dmg')


def extract_file_from_dmg(path: Path, file_name: str) -> (Path, bool):
    unpack_dest = path.with_suffix('')
    unpack_dest.mkdir(exist_ok=True)
    logging.info(f"Unpacking {path} to {unpack_dest}")

    # Mount the DMG
    subprocess.check_call(f"hdiutil attach {path} -mountpoint {unpack_dest} -quiet", shell=True)

    try:
        app_files = glob(f"{unpack_dest}/**/{file_name}.app", recursive=True)
        pkg_files = glob(f"{unpack_dest}/**/{file_name}.pkg", recursive=True)

        if app_files:
            assert len(app_files) == 1, f"There should be one .app file in the dmg with the name {file_name}"
            return Path(app_files[0]), False

        elif pkg_files:
            assert len(pkg_files) == 1, f"There should be one .pkg file in the dmg with the name {file_name}"
            return extract_file_from_pkg(Path(pkg_files[0]), file_name), True
        else:
            raise Exception("No .app or .pkg files found in the DMG!")

    finally:
        # Unmount the DMG
        subprocess.check_call(["hdiutil", "detach", unpack_dest])


def extract_file_from_pkg(path: Path, file_name: str) -> Path:
    temp_dir = Path(gettempdir()) / basename(path)
    temp_dir.mkdir(exist_ok=True)
    logging.info(f"Unpacking {path} to {temp_dir}")

    # Unpack pkg file
    subprocess.check_call(f"tar -xf {path} -C {temp_dir}", shell=True)
    payload_file = glob(f"{temp_dir}/**/{PKG_PAYLOAD_FILE}", recursive=True)
    assert len(payload_file) == 1, f"There should be one {PKG_PAYLOAD_FILE} file extracted from the pkg file {path}"

    # Unpack Payload file
    unpack_dest = PACKAGES_DIR / file_name
    unpack_dest.mkdir(exist_ok=True, parents=True)
    logging.info(f"Unpacking {payload_file[0]} to {unpack_dest}")

    subprocess.check_call(f"tar -xf {payload_file[0]} -C {unpack_dest}", shell=True)

    matches = glob(f"{unpack_dest}/**/{file_name}", recursive=True)
    binaries = []
    for match in matches:
        with suppress(FileNotFoundError, ValueError, RuntimeError):
            _ = get_tool_version(Path(match), silent=True)
            binaries.append(match)

    # TODO: Find a workaround for the fact that the pkg file contains multiple binaries
    # assert len(binaries) == 1, f"There should be one binary in the archive with the name {file_name}"
    return Path(binaries[0])


def create_session():
    session = Session()
    retries = Retry(total=5,
                    backoff_factor=1,
                    status_forcelist=[
                        HTTPStatus.TOO_MANY_REQUESTS.value,
                        HTTPStatus.INTERNAL_SERVER_ERROR.value,
                        HTTPStatus.BAD_GATEWAY.value,
                        HTTPStatus.SERVICE_UNAVAILABLE.value,
                        HTTPStatus.GATEWAY_TIMEOUT.value,
                    ])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.request = partial(session.request, timeout=REQUEST_MAX_TIMEOUT)
    return session


def filter_artifacts(names: list[str]) -> list[str]:
    DROP_NAMES = ('checksum', 'sha', '.sig', '.pem', '.sbom', 'key')
    return list(filter(lambda name: all([substr not in name for substr in DROP_NAMES]), names))


def choose_url(urls: list[str]) -> str:
    urls = filter_artifacts(urls)

    # Priority #1 - without suffix
    if url := _search_url(urls, no_suffix):
        return url

    # Priority #2 - an archive if available
    if url := _search_url(urls, is_archive):
        return url

    # search url if dmg file
    if url := _search_url(urls, is_dmg):
        return url

    raise ValueError(f"Could not find a valid URL inside {urls}. Please file a bug")


def no_suffix(item: str) -> bool:
    return not Path(item).suffix


def _search_url(urls: list[str], func: Callable[[str], bool]) -> str:
    ls = []

    for url in urls:
        if func(url):
            ls.append(url)
    if len(ls) > 1:
        raise ValueError(f"There are several valid urls: {ls} for matcher {func.__name__}, Please file a bug")
    if len(ls) == 1:
        return ls[0]

    return ''


@cache
def fetch_url(url: str, raise_for_status: bool = True) -> str:
    logging.debug(f"Fetching {url}")
    res = create_session().get(url)
    if raise_for_status:
        res.raise_for_status()
    return res.text


def get_host_operating_system() -> str:
    return platform.system().lower()


def get_host_architecture() -> str:
    return platform.machine()
