from jupyter_server.services.contents.manager import ContentsManager

c = get_config()  # noqa

# Abstract ContentsManager, should disable all contents
c.ServerApp.contents_manager_class = ContentsManager

c.ServerApp.allow_unauthenticated_access = False

c.ServerApp.terminals_enabled = False
