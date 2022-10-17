import logging
import re
import stat
import subprocess
from shutil import which
from pathlib import Path

import requests
from humanize import naturalsize
from rich.progress import Progress

MATRIX_X86_64 = ('x86_64', 'amd64')
CHUNK_SIZE = 1024


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

    output = subprocess.check_output(
        f'{path} --version'.split()).decode().strip()
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

    with requests.get(url, stream=True) as r:
        total_length = int(r.headers.get('content-length', 0))

        dest = local_path(name)
        dest.parent.mkdir(exist_ok=True)

        logging.info(
            f"Downloading '{name}' to {dest} (size: {naturalsize(total_length)})")
        # TODO: Handle archives
        with dest.open('wb') as file, Progress() as progress:
            task = progress.add_task("Downloading...", total=total_length)
            for data in r.iter_content(chunk_size=CHUNK_SIZE):
                if data:
                    file.write(data)
                    progress.advance(task, CHUNK_SIZE)
        dest.chmod(dest.stat().st_mode | stat.S_IEXEC)
