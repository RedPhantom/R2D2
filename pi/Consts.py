# Purpose: contain application constants.
import os

CONFIG_PATH: str = os.path.abspath("config.json")
"""
Path to the application configuration file.
``os.path.abspath`` is used so that files using this path will get it correctly no matter where they are,
as long as this file is at the same relative path as the configuration file.
E.g., if ``CONFIG_PATH`` is ``"config.json"``, then this file must be in the same directory as ``"config.json"``.
"""
