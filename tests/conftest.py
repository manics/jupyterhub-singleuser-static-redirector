import os
import socket
import sys
import time
from subprocess import Popen
from typing import Generator
from uuid import uuid4

import requests
from pytest import fixture


@fixture(scope="session")
def random_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


@fixture(scope="session")
def destination() -> str:
    return "https://jupyter.org"


@fixture(scope="session")
def jupyter_server(random_port: int, destination: str) -> Generator[str, None, None]:
    """Run jupyter-server"""

    token = str(uuid4())
    args = [
        sys.executable,
        "-m",
        "jupyter",
        "server",
        f"--port={random_port}",
        "--no-browser",
        f"--IdentityProvider.token={token}",
        # "--config=jupyter_server_config.py",
        # "--debug",
    ]
    env = os.environ.copy()
    env["STATIC_REDIRECTOR_DESTINATION"] = destination

    server_proc = Popen(args, env=env)

    url = f"http://localhost:{random_port}/"
    check_url = f"{url}api"

    exc = None
    for i in range(10):
        time.sleep(1)
        try:
            r = requests.get(check_url)
            if r.status_code == 200:
                break
            exc = None
        except requests.RequestException as e:
            exc = e
        print(".", end="", flush=True)
    else:
        if not exc:
            exc = RuntimeError(f"Failed to successfully request {check_url}")
        raise exc from None

    yield url, token

    # clean up after server is no longer needed
    server_proc.terminate()
