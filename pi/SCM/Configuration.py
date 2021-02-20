# Purpose: Provide a data model to represent the application configuration.


class AppConfig:
    """
    A data model to represent application-specific configuration.
    """


class LoggingConfig:
    """
    A data model to represent the logging configuration.
    """

    def __init__(self, log_path: str, message_format: str, level: int):
        """
        Initialize the logging configuration.
        :param log_path: path in which the log file will be saved.
        :param message_format: the format in which log messages will be formatted.
        :param level: the minimal message level to report to file.
        """

        self.log_path = log_path
        self.format = message_format
        self.level = level


class Config:
    """
    The complete configuration.
    """

    def __init__(self, app_config: AppConfig, logging_config: LoggingConfig):
        """
        Initialize the total configuration.
        :param app_config:
        :param logging_config:
        """

        self.app_config = app_config
        self.logging_config = logging_config
