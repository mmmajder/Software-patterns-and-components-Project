import pkg_resources
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Core'
    graph = None
    loader_plugins = []
    visualiser_plugins = []

    def ready(self):
        self.loader_plugins = load_plugins("loader")
        self.visualiser_plugins = load_plugins("visualiser")


def load_plugins(oznaka):
    plugins = []
    for ep in pkg_resources.iter_entry_points(group=oznaka):
        p = ep.load()
        plugin = p()
        plugins.append(plugin)
        
    return plugins
