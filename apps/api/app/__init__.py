"""
Food Safety Platform API - App Package

This module initializes the app package and sets up the Python path
to allow imports from the shared packages directory.
"""
import sys
from pathlib import Path

# Add packages directory to Python path for shared modules (scrapers, etc.)
# This needs to happen BEFORE any imports that depend on the scrapers package
PACKAGES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "packages"
if str(PACKAGES_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGES_DIR))
