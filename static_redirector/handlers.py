"""API handlers for the Jupyter Server example."""

import logging

from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.extension.handler import (
    ExtensionHandlerJinjaMixin,
    ExtensionHandlerMixin,
)
from tornado import web


class BaseTemplateHandler(
    ExtensionHandlerJinjaMixin, ExtensionHandlerMixin, JupyterHandler
):
    """A base template handler."""


class IndexHandler(BaseTemplateHandler):
    """The root API handler."""

    @web.authenticated
    def get(self) -> None:
        """Get the root response."""
        if self.config.autoredirect:
            self.redirect(self.config.destination)
        else:
            self.write(
                self.render_template("index.html", destination=self.config.destination)
            )


class ErrorHandler(BaseTemplateHandler):
    """An error handler."""

    def get(self, path: str) -> None:
        """Handle the error."""
        self.write_error(400)
