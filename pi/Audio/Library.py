import os
from enum import Enum
from os import path
from typing import List, AnyStr

import Audio.Interface
from Configuration.Configuration import AppConfig


class SpeechLibrary:
    AUDIO_DIR = "audio"

    class Emotions(Enum):
        NEUTRAL = 0
        HAPPY = 1
        SCREAMING = 2
        SCARED = 3
        CONFUSED = 4

    class EmotionFilters(Enum):
        # The specified emotions must be embodied in the word.
        INCLUDING = 0

        # The specified emotions must be the only emotions embodied in the word.
        EXCLUSIVE = 1

        # At least one of the specified emotions must be embodied in the word.
        AT_LEAST_ONE = 2

    class Word:
        def __init__(self, file_path: AnyStr, emotions: List, interface: Audio.Interface.AudioInterface = None):
            """
            Initialize a new word sound effect.

            :param file_path: path of the sound file relative to the data directory.
            :param emotions: filter emotions embodied in this sound effect.
            :param interface: audio interface to play the sound through.
            """

            if not isinstance(emotions, list):
                raise TypeError("Expected type 'list' for 'emotions'.")

            self.file_path = file_path
            self.emotions = emotions

            if interface and isinstance(interface, Audio.Interface.AudioInterface):
                self.interface = interface

        def get_absolute_path(self, app_config: AppConfig):
            """
            Retrieve the absolute file path according to the data directory specified in the application configuration.

            :param app_config: application configuration data.
            :return: absolute audio file path.
            """

            return path.join(app_config.data_dir, self.file_path)

        def play(self, app_config: AppConfig, volume_adjustment = 0):
            """
            Play the word (if an interface was configured initializing this word).
            *Note*: no sound volume adjustment is available using this method.

            :param app_config: prepared application configuration object.
            :param volume_adjustment: adjustment to the word volume in decibels.
            """

            if self.interface:
                self.interface.play_sound(self.get_absolute_path(app_config), volume_adjustment=volume_adjustment)

    WORDS = [
        Word(file_path=os.path.join(AUDIO_DIR, "01.wav"), emotions=[Emotions.NEUTRAL, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "02.wav"), emotions=[Emotions.NEUTRAL, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "03.wav"), emotions=[Emotions.CONFUSED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "04.wav"), emotions=[Emotions.NEUTRAL, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "05.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "06.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "07.wav"), emotions=[Emotions.SCARED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "08.wav"), emotions=[Emotions.HAPPY, Emotions.CONFUSED]),
        Word(file_path=os.path.join(AUDIO_DIR, "09.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "10.wav"), emotions=[Emotions.NEUTRAL, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "11.wav"), emotions=[Emotions.NEUTRAL, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "12.wav"), emotions=[Emotions.NEUTRAL, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "13.wav"), emotions=[Emotions.NEUTRAL, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "14.wav"), emotions=[Emotions.CONFUSED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "15.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "16.wav"), emotions=[Emotions.NEUTRAL, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "17.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "18.wav"), emotions=[Emotions.HAPPY, Emotions.CONFUSED]),
        Word(file_path=os.path.join(AUDIO_DIR, "19.wav"), emotions=[Emotions.CONFUSED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "20.wav"), emotions=[Emotions.SCARED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "21.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "22.wav"), emotions=[Emotions.SCREAMING, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "23.wav"), emotions=[Emotions.NEUTRAL, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "24.wav"), emotions=[Emotions.NEUTRAL, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "25.wav"), emotions=[Emotions.NEUTRAL, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "26.wav"), emotions=[Emotions.CONFUSED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "27.wav"), emotions=[Emotions.CONFUSED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "28.wav"), emotions=[Emotions.NEUTRAL, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "29.wav"), emotions=[Emotions.CONFUSED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "30.wav"), emotions=[Emotions.CONFUSED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "31.wav"), emotions=[Emotions.CONFUSED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "32.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "33.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "34.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "34.wav"), emotions=[Emotions.HAPPY, Emotions.CONFUSED]),
        Word(file_path=os.path.join(AUDIO_DIR, "35.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "36.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "37.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "38.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "39.wav"), emotions=[Emotions.CONFUSED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "40.wav"), emotions=[Emotions.CONFUSED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "41.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "42.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "43.wav"), emotions=[Emotions.HAPPY, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "44.wav"), emotions=[Emotions.SCARED, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "45.wav"), emotions=[Emotions.SCREAMING, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "46.wav"), emotions=[Emotions.SCREAMING, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "47.wav"), emotions=[Emotions.SCREAMING, ]),
        Word(file_path=os.path.join(AUDIO_DIR, "48.wav"), emotions=[Emotions.CONFUSED, ]),
    ]

    def __init__(self, parent_path: str = ""):
        """
        Initialize the speech library.

        :param parent_path: the path in which word file paths reside,
            i.e. the path that is the parent to Word.file_path.
        """

        self._parent_path = parent_path

    def get_words(self, emotions: list[Emotions],
                  filtering_method: EmotionFilters = EmotionFilters.INCLUDING,
                  interface: Audio.Interface.AudioInterface = None) -> list[Word]:
        """
        Retrieve all words according to the specified emotions and filtering method.

        :param emotions: list of emotions to search words by.
        :param filtering_method: how to filter words according to the specified emotions.
        :param interface: audio interface to play the words through.
        :return: a list of zero or more words that match the query.
        """

        if not (isinstance(emotions, list) or isinstance(emotions, set)):
            try:
                emotions = list(emotions)
            except TypeError:
                raise TypeError("Expected list of 'Emotions'.")

        if len(emotions) == 0:
            return self.WORDS

        for emotion in emotions:
            if not isinstance(emotion, SpeechLibrary.Emotions):
                raise TypeError("Invalid type for 'emotion', expected 'SpeechLibrary.Emotions'.")

        matching_words = []

        for word in self.WORDS:
            word.file_path = path.join(self._parent_path, word.file_path)

            if filtering_method == SpeechLibrary.EmotionFilters.INCLUDING:
                if all(emotion in word.emotions for emotion in emotions):
                    matching_words.append(word)
                    matching_words[-1].interface = interface

            if filtering_method == SpeechLibrary.EmotionFilters.EXCLUSIVE:
                if emotions == word.emotions:
                    matching_words.append(word)
                    matching_words[-1].interface = interface

            if filtering_method == SpeechLibrary.EmotionFilters.AT_LEAST_ONE:
                if any(emotion in word.emotions for emotion in emotions):
                    matching_words.append(word)
                    matching_words[-1].interface = interface

        return matching_words
