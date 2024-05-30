import importlib
import logging
import os
from pathlib import Path


class HandlerManager:
    def __init__(self, dp):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.project_root = Path(self.script_directory).parent
        self.dp = dp

    def import_routers(self):
        apps_directory = self.project_root / "apps"

        for app_dir in apps_directory.iterdir():
            handlers_dir = app_dir / "handlers"
            if app_dir.is_dir() and os.path.exists(handlers_dir):
                for handler in handlers_dir.iterdir():
                    if handler.is_file() and not handler.name.startswith("__init__"):
                        module_name = (
                            f"apps.{app_dir.name}.{handlers_dir.name}.{handler.stem}"
                        )
                        try:
                            module = importlib.import_module(module_name)
                            if hasattr(module, "router"):
                                self.dp.include_router(module.router)
                        except ImportError as e:
                            logging.error(f"Error importing module {module_name}: {e}")
