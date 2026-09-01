import json
import sys
from pathlib import Path


def get_app_directory():
    if getattr(sys, "frozen", False):
        # Running as a PyInstaller executable
        return Path(sys.executable).parent

    # Running normally from Python
    return Path(__file__).resolve().parent


def load_config(filename="config.json"):
    config_path = get_app_directory() / filename

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)