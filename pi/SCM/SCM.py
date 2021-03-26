# Module:  State and Configuration Manager
# Purpose: Manage droid application configuration.
from os import path

from Configuration.Configuration import Config
from Telemetry.Telemetry import AppExceptions


class ConfigurationManager:

    def __init__(self, config_path: str):
        """
        Retrieve global configuration from the specified file.
        :param config_path: path to the configuration file.
        :return: the imported configuration.
        """

        if not path.exists(config_path):
            raise AppExceptions.InvalidPathException(config_path)

        self._config_path = config_path

    def get_config(self) -> Config:
        raise NotImplementedError()

    def save_config(self):
        raise NotImplementedError()
