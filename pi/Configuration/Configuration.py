# Purpose: Provide a data model to represent the application configuration.
import logging
import json
import copy

import Consts


class ConfigModelBase:
    """
    Provide core functionalities for configuration models, such as formatted (str) printout.
    """

    def __str__(self) -> str:
        """
        Retrieve the formatted representation of the configuration class.

        :return: a "key: value" combination per line.
        """

        key_value_pairs = []
        for config_key, config_value in self.__dict__:
            key_value_pairs.append(
                "{config_key}: {config_value}".format(config_key=config_key, config_value=config_value))

        return "\n".join(key_value_pairs)


class AppConfig(ConfigModelBase):
    """
    A data model to represent application-specific configuration.
    """

    class Defaults:
        DATA_DIR: str = "C:\\Development\\R2D2\\pi\\data"

    def __init__(self,
                 data_dir: str = Defaults.DATA_DIR):
        """
        Initialize the application configuration.

        :param data_dir: absolute path of the directory of data files (assets).
        """

        self.data_dir = data_dir


class AudioConfig(ConfigModelBase):
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

        :param frequency: sample frequency (rate) in which sounds would be played at.
        :param device_name: name of the audio device through which sound would be played.
        """

        self.frequency = frequency
        self.device_name = device_name


class LoggingConfig(ConfigModelBase):
    """
    A data model to represent the logging configuration.
    """

    class Defaults:
        LOG_PATH: str = "r2d2.log"
        MESSAGE_FORMAT: str = "%(asctime)s    %(levelname)10s    %(message)s"
        LEVEL: int = logging.DEBUG

    def __init__(self,
                 log_path: str = Defaults.LOG_PATH,
                 message_format: str = Defaults.MESSAGE_FORMAT,
                 level: int = Defaults.LEVEL):
        """
        Initialize the logging configuration.

        :param log_path: path in which the log file will be saved.
        :param message_format: format in which log messages will be formatted.
        :param level: minimal message level to report to file.
        """

        self.log_path = log_path
        self.message_format = message_format
        self.level = level


class Config:
    """
    Holds system configuration.
    """

    def __init__(self,
                 app_config: AppConfig = AppConfig(),
                 audio_config: AudioConfig = AudioConfig(),
                 logging_config: LoggingConfig = LoggingConfig()):
        """
        Initialize the total configuration. Omitting configuration object parameters
        will set them to have default values.

        :param app_config: object containing the values of the application configuration.
        :param audio_config: object containing the values of the audio configuration.
        :param logging_config: object containing the values of the logging configuration.
        """

        self.app_config = copy.deepcopy(app_config)
        self.audio_config = copy.deepcopy(audio_config)
        self.logging_config = copy.deepcopy(logging_config)

    def save(self, configuration_path):
        """
        Save the configuration to the specified path.

        :param configuration_path: path to the configuration file.
        """

        try:
            with open(configuration_path, "wt") as config_file:
                json_data = json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=4)
                config_file.write(json_data)

        except IOError as io_err:
            print(f"ERROR: Failed to save configuration file to {configuration_path}: {io_err}.")

    def load(self, configuration_path):
        """
        Load the specified configuration file into the configuration object.
        *Note*: missing configuration keys will be set to default values.

        :param configuration_path: path to configuration file.
        """

        try:
            with open(configuration_path, "rt") as config_file:
                json_data = json.loads(config_file.read())

                self.app_config = AppConfig(**json_data["app_config"])
                self.audio_config = AudioConfig(**json_data["audio_config"])
                self.logging_config = LoggingConfig(**json_data["logging_config"])

        except IOError as io_err:
            print(f"ERROR: Failed to load configuration from file {configuration_path}: {io_err}.")


def get_test_config() -> Config:
    """
    Get a configuration adapted for testing (i.e. preferring the local config.json,
    although the default is available as well).
    :return: a prepared configuration object.
    """

    config = Config()

    try:
        config.load(Consts.CONFIG_PATH)
    finally:
        return config
