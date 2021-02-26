from SCM.Configuration import Config, AudioConfig, AppConfig, LoggingConfig


def config_test():
    app_config = AppConfig()
    audio_config = AudioConfig()
    logging_config = LoggingConfig()

    saved_config = Config(app_config, audio_config, logging_config)
    saved_config.save("config.json")

    loaded_config = Config.load("config.json")

    assert loaded_config.app_config.data_dir == saved_config.app_config.data_dir
    assert loaded_config.logging_config.level == saved_config.logging_config.level

    print("Test passed")


if __name__ == '__main__':
    config_test()
