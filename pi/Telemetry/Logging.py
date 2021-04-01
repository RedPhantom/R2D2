# Purpose: perform logging and telemetry reporting.

import logging
from os import path

from Configuration.Configuration import LoggingConfig
from Telemetry.Exceptions import AppExceptions


class Logging:
    def __init__(self, logging_config: LoggingConfig):
        """
        Initialize a new logging object.

        :param logging_config: logging configuration to use.
        """

        if not path.exists(logging_config.log_path):
            raise AppExceptions.InvalidPathException(logging_config.log_path)

        logging.basicConfig(
            filename=logging_config.log_path,
            format=logging_config.message_format,
            level=logging_config.level
        )

    @staticmethod
    def get_logger(module_name: str) -> logging.Logger:
        """
        Retrieve a module-specific logger.

        :param module_name: name of the module to report as.
        """

        return logging.getLogger(module_name)
