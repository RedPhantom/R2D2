# Purpose: contain unit tests for the Audio module.
import unittest
import random

from Audio.Interface import AudioInterface
from Audio.Library import SpeechLibrary
from Configuration.Configuration import get_test_config


class BasicSanity(unittest.TestCase):
    def test_play(self):
        """
        Ensure a sound effect is played correctly by playing a random word.
        """

        config = get_test_config()
        speech_library = SpeechLibrary()
        interface = AudioInterface(config.audio_config)
        no_emotion_filters = []

        words = speech_library.get_words(emotions=no_emotion_filters)
        self.assertNotEqual(len(words), 0, "Expected populated words library, got empty words library.")

        random_word = random.choice(words)
        interface.play_sound(random_word.get_absolute_path(config.app_config))
