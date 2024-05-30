import importlib
import logging
import os
from pathlib import Path


class TaskManager:
    def __init__(self):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.project_root = Path(self.script_directory).parent

    def import_tasks(self):
        apps_directory = self.project_root / "apps"

        for app_dir in apps_directory.iterdir():
            if app_dir.is_dir():
                routers_file = app_dir / "tasks.py"
                if routers_file.exists():
                    module_name = f"apps.{app_dir.name}.tasks"
                    try:
                        importlib.import_module(module_name)
                    except ImportError as e:
                        logging.error(f"Error importing module {module_name}: {e}")
