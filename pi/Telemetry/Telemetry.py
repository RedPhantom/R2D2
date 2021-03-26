# Module:  Telemetry and Logging Module
# Purpose: Perform logging and telemetry reporting.

import logging
from os import path

from Configuration.Configuration import LoggingConfig


class ApplicationExceptions:
    def __init__(self):
        pass

    class InvalidPathException(Exception):
        def __init__(self, invalid_path, message="The specified path does not exist: %s"):
            self._path = invalid_path
            self._message = message

            super().__init__(self._message % (self._path,))

    class SerialException(Exception):
        pass

class Logging:
    def __init__(self, logging_config: LoggingConfig):
        """
        Initialize a new logging object.
        :param logging_config: the logging configuration to use.
        """

        if not path.exists(logging_config.log_path):
            raise ApplicationExceptions.InvalidPathException(logging_config.log_path)

        logging.basicConfig(
            filename=logging_config.log_path,
            format=logging_config.format,
            level=logging_config.level
        )

    @staticmethod
    def get_logger(module_name: str) -> logging.Logger:
        """
        Retrieve a module-specific logger.
        :param module_name: name of the module to report as.
        """

        return logging.getLogger(module_name)
