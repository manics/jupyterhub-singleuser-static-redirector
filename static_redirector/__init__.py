"""The extension entry point."""

from typing import Any

from .application import Redirector


def _jupyter_server_extension_points() -> list[dict[str, Any]]:
    return [
        {"module": "static_redirector.application", "app": Redirector},
    ]


_jupyter_server_extension_paths = _jupyter_server_extension_points
