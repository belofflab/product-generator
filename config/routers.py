import importlib
import logging
from fastapi import FastAPI
import os
from pathlib import Path


class RouterManager:
    """
    A utility class for managing FastAPI routers.

    This class detects and imports FastAPI routers from 'routers.py' files in
    the subdirectories of the 'apps' directory. It allows you to easily include
    routers in your FastAPI application.

    Attributes:
        None

    Methods:
        import_routers():
            Detects 'routers.py' files in subdirectories of the 'apps' directory
            and imports the 'router' variable from each file.

    Example Usage:
        router_manager = RouterManager()

        # Import routers from detected 'routers.py' files
        router_manager.import_routers()
    """

    def __init__(self, app: FastAPI):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.project_root = Path(self.script_directory).parent
        self.app = app

    def import_routers(self):
        apps_directory = self.project_root / "apps"

        for app_dir in apps_directory.iterdir():
            handlers_dir = app_dir / "routers"
            if app_dir.is_dir() and os.path.exists(handlers_dir):
                for handler in handlers_dir.iterdir():
                    if handler.is_file() and not handler.name.startswith("__init__"):
                        module_name = (
                            f"apps.{app_dir.name}.{handlers_dir.name}.{handler.stem}"
                        )
                        try:
                            module = importlib.import_module(module_name)
                            if hasattr(module, "router"):
                                self.app.router.include_router(module.router)
                        except ImportError as e:
                            logging.error(f"Error importing module {module_name}: {e}")