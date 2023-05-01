import logging
import platform
import re
import stat
import subprocess
from functools import cache, partial
from glob import glob
from http import HTTPStatus
from os.path import basename
from pathlib import Path
from shutil import copy, get_unpack_formats, unpack_archive, which
from tempfile import gettempdir
from typing import Callable

from humanize import naturalsize
from requests import Session
from requests.adapters import HTTPAdapter
from rich.progress import Progress
from urllib3 import Retry

from .vendors.vendor import Tool

MATRIX_X86_64 = ('amd64', 'x86_64', '64bit')
INSTALL_DIR = Path.home() / ".mercado"
CHUNK_SIZE = 1024
REQUEST_MAX_TIMEOUT = 10
STREAM_MAX_TIMEOUT = 300
SUBPROCSES_TIMEOUT = 30
SUPPORTED_ARCHIVE_FORMATS: list[str] = sum([format[1] for format in get_unpack_formats()], [])


def get_architecture_variations(arch: str) -> list[str]:
    if arch in MATRIX_X86_64:
        return MATRIX_X86_64
    return [arch]


def is_valid_architecture(expected: str, actual: str) -> bool:
    '''
    Equalize architectures that their name does not necessarily match
    '''
    for arch in get_architecture_variations(expected):
        if re.search(arch, actual, re.IGNORECASE):
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


def get_tool_version(path: Path) -> str:
    if not which(path):
        raise FileNotFoundError(path)

    commands = [f'{path} --version', f'{path} version']
    for command in commands:
        try:
            return get_command_version(command)
        except RuntimeError as ex:
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

        if is_archive(str(temp_file)):
            temp_file = extract_file_from_archive(temp_file, name)

        logging.info(f"Copying {temp_file} to {dest}")
        dest.parent.mkdir(exist_ok=True, parents=True)
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
    return matches[0]


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
