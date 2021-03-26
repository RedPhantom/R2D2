# Purpose: Provide a data model to represent the application configuration.
import logging


class AppConfig:
    """
    A data model to represent application-specific configuration.
    """

    data_dir: str = "D:\\Development\\R2D2\\pi\\data"


class AudioConfig:
    """
    A data model to represent audio and sound configuration.
    """

    frequency: int = 44100
    device_name: str = None


class LoggingConfig:
    """
    A data model to represent the logging configuration.
    """

    class Defaults:
        LOG_PATH = "r2d2.log"
        MESSAGE_FORMAT = "%(asctime)s    %(levelname)10s    %(message)s"
        LEVEL = logging.DEBUG

    def __init__(self,
                 log_path: str = Defaults.LOG_PATH,
                 message_format: str = Defaults.MESSAGE_FORMAT,
                 level: int = Defaults.LEVEL):
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

    def __init__(self, app_config: AppConfig, audio_config: AudioConfig, logging_config: LoggingConfig):
        """
        Initialize the total configuration.
        :param app_config:
        :param logging_config:
        """

        self.app_config = app_config
        self.audio_config = audio_config
        self.logging_config = logging_config
