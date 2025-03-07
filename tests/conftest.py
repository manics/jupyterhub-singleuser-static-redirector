import os
import socket
import sys
import time
from subprocess import Popen
from typing import Generator
from uuid import uuid4

import requests
from pytest import fixture


@fixture(scope="function")
def random_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


@fixture(scope="function")
def token() -> str:
    return str(uuid4())


@fixture(scope="function")
def destination() -> str:
    return f"https://example.org/?{uuid4()}"


@fixture(scope="function")
def autoredirect() -> str | None:
    return None


@fixture(scope="function")
def jupyter_server(
    random_port, token, destination, autoredirect
) -> Generator[str, None, None]:
    """Run jupyter-server"""

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

    env = {}
    env["STATIC_REDIRECTOR_DESTINATION"] = destination
    if autoredirect is not None:
        env["STATIC_REDIRECTOR_AUTOREDIRECT"] = autoredirect

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

    yield url

    # clean up after server is no longer needed
    server_proc.terminate()
