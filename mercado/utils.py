import logging
import re
import stat
import subprocess
from functools import partial
from glob import glob
from http import HTTPStatus
from os.path import basename
from pathlib import Path
from shutil import copy, get_unpack_formats, unpack_archive, which
from tempfile import gettempdir

from humanize import naturalsize
from requests import Session
from requests.adapters import HTTPAdapter
from rich.progress import Progress
from urllib3 import Retry

MATRIX_X86_64 = ('x86_64', 'amd64')
CHUNK_SIZE = 1024
REQUEST_MAX_TIMEOUT = 10
STREAM_MAX_TIMEOUT = 300
SUPPORTED_ARCHIVE_FORMATS = sum([format[1] for format in get_unpack_formats()], [])


def is_valid_architecture(expected: str, actual: str) -> bool:
    '''
    Equalize architectures that their name does not necessarily match
    '''
    if expected in MATRIX_X86_64:
        for arch in MATRIX_X86_64:
            if arch in actual:
                return True

    return expected in actual


def get_local_version(name: str) -> tuple[str, str]:
    path = local_path(name)

    if not path.exists():
        path = which(name)
        if not path:
            raise ValueError(f'{name} could not be found')

    return get_tool_version(path), path


def get_tool_version(path: Path) -> str:
    if not which(path):
        raise FileNotFoundError(path)

    try:
        output = subprocess.check_output(f'{path} --version'.split(), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        output = subprocess.check_output(f'{path} version'.split(), stderr=subprocess.STDOUT)

    output = output.decode().strip()
    match = re.search(
        r'([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?', output)
    return match[0]


def local_path(name: str) -> Path:
    return Path.home() / ".mercado" / name


def is_tool_available_in_path(name: str) -> bool:
    try:
        subprocess.check_output(f'which {name}'.split())
        return True
    except subprocess.CalledProcessError:
        return False


def download(name: str, url: str):
    logging.debug(f'Download {url}')

    with create_session().get(url, stream=True, timeout=STREAM_MAX_TIMEOUT) as r:
        total_length = int(r.headers.get('content-length', 0))

        temp_file = Path(gettempdir()) / basename(url)

        logging.info(
            f"Downloading '{name}' to {temp_file} (size: {naturalsize(total_length)})")

        with temp_file.open('wb') as file, Progress() as progress:
            task = progress.add_task("Downloading...", total=total_length)
            for data in r.iter_content(chunk_size=CHUNK_SIZE):
                if data:
                    file.write(data)
                    progress.advance(task, CHUNK_SIZE)

        dest = local_path(name)
        dest.parent.mkdir(exist_ok=True)

        if is_archive(str(temp_file)):
            temp_file = extract_file_from_archive(temp_file, name)

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


def choose_url(urls: list[str]) -> str:
    DROP_NAMES = ('checksum', 'sha')

    urls = list(filter(lambda url: all(
        [substr not in url for substr in DROP_NAMES]), urls))

    # Priority #1 - without suffix
    for url in urls:
        if not Path(url).suffix:
            return url

    # Priority #2 - an archive if available
    for url in urls:
        if is_archive(url):
            return url

    assert len(urls) == 1, f"There are several valid urls: {urls}, taking the first one. Please file a bug"
    return urls[0]
