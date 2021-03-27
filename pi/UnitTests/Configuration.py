# Purpose: contain unit tests for the Configuration module.

import os
import unittest

from Configuration.Configuration import Config


class BasicSanity(unittest.TestCase):
    def test_create(self):
        """
        Ensure configuration object are created and have default values.
        """

        c1 = Config()

        # Note: make sure these asserts don't apply on configurations keys that are None by default.
        self.assertIsNotNone(c1.app_config.data_dir)
        self.assertIsNotNone(c1.audio_config.frequency)
        self.assertIsNotNone(c1.logging_config.log_path)

    def test_save_load(self):
        """
        Ensure default configuration is saved and loaded correctly.
        """

        c1 = Config()
        c2 = Config()

        self.assertIsNotNone(c1)
        self.assertIsNotNone(c2)

        # Create a temporary file to save c2.
        temp_file_name = "temp_config.json"

        # Save and load configuration.
        c2.save(temp_file_name)
        c2.load(temp_file_name)

        self.assertDictEqual(c1.app_config.__dict__, c2.app_config.__dict__)
        self.assertDictEqual(c1.audio_config.__dict__, c2.audio_config.__dict__)
        self.assertDictEqual(c1.logging_config.__dict__, c2.logging_config.__dict__)

        os.remove(temp_file_name)

    def test_save_load_modified(self):
        """
        This test ensures modified configuration is saved and loaded correctly.
        It also ensures no by-reference issues occur when modifying configuration objects.
        For example, the following code, having a backend bug, could cause c2 to be the same as c1:

        >>> config1 = Config()
        >>> config2 = Config()
        >>>
        >>> config1.app_config.data_dir = "C:\"
        >>> print config2.app_config.data_dir # This would print "C:\" instead of the default value.
        """

        c1 = Config()
        c2 = Config()

        c1.app_config.data_dir = "C:\\"
        c1.audio_config.frequency = 48000
        c1.logging_config.log_path = "C:\\log\\"

        # Create a temporary file to save c2.
        temp_file_name = "temp_config.json"

        # Save and load configuration.
        c1.save(temp_file_name)

        # Make sure the two configurations are different.
        self.assertNotEqual(c1.app_config.__dict__, c2.app_config.__dict__)
        self.assertNotEqual(c1.audio_config.__dict__, c2.audio_config.__dict__)
        self.assertNotEqual(c1.logging_config.__dict__, c2.logging_config.__dict__)

        # Delete the temporary configuration.
        os.remove(temp_file_name)


if __name__ == '__main__':
    unittest.main()
