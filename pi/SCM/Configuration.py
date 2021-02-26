# Purpose: Provide a data model to represent the application configuration.
import logging
import json


class AppConfig:
    """
    A data model to represent application-specific configuration.
    """

    class Defaults:
        DATA_DIR: str = "D:\\Development\\R2D2\\pi\\data"

    def __init__(self,
                 data_dir: str = Defaults.DATA_DIR):
        """
        Initialize the application configuration.
        :param data_dir: absolute path of the directory of data files (assets).
        """

        self.data_dir = data_dir


class AudioConfig:
    """
    A data model to represent audio and sound configuration.
    """

    class Defaults:
        FREQUENCY: int = 44100
        DEVICE_NAME: str = None

    def __init__(self,
                 frequency: int = Defaults.FREQUENCY,
                 device_name: str = Defaults.DEVICE_NAME):
        """
        Initialize the audio configuration.
        :param frequency: the sample frequency in which sounds would be played at.
        :param device_name: name of the audio device through which sound would be played.
        """

        self.frequency = frequency
        self.device_name = device_name


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
        self.message_format = message_format
        self.level = level


class Config:
    """
    Holds system configuration.
    """

    def __init__(self,
                 app_config: AppConfig,
                 audio_config: AudioConfig,
                 logging_config: LoggingConfig):
        """
        Initialize the total configuration.
        :param app_config: object containing the values of the application configuration.
        :param audio_config: object containing the values of the audio configuration.
        :param logging_config: object containing the values of the logging configuration.
        """

        self.app_config = app_config
        self.audio_config = audio_config
        self.logging_config = logging_config

    def save(self, configuration_path):
        """
        Save the configuration to `configuration_path`.

        :param configuration_path: path to the configuration file.
        """

        try:
            with open(configuration_path, "wt") as config_file:
                json_data = json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=4)
                config_file.write(json_data)

        except IOError as io_err:
            print("ERROR: Failed to save configuration file to %s: %s" % (configuration_path, io_err))

    @staticmethod
    def load(configuration_path):
        try:
            with open(configuration_path, "rt") as config_file:
                json_data = json.loads(config_file.read())

                app_config = AppConfig(**json_data["app_config"])
                audio_config = AudioConfig(**json_data["audio_config"])
                logging_config = LoggingConfig(**json_data["logging_config"])

                return Config(app_config, audio_config, logging_config)

        except IOError as io_err:
            print("ERROR: Failed to load configuration from file %s: %s" % (configuration_path, io_err))
