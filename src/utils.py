from pathlib import Path
import sys


def resource_path(relative_path):
    """Get absolute path to resource, works in dev and PyInstaller exe."""
    if getattr(sys, "_MEIPASS", False):
        return Path(sys._MEIPASS) / relative_path
    return Path(relative_path)
