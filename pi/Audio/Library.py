from enum import Enum
from os import path

from Configuration.Configuration import AppConfig


class SpeechLibrary:
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
        def __init__(self, file_path: str, emotions: list):
            """
            Initialize a new word sound effect.
            :param file_path: path of the sound file relative to the data directory.
            :param emotions: the emotions embodied in this sound effect.
            """

            if not isinstance(emotions, list):
                raise TypeError("Expected type 'list' for 'emotions'.")

            self.file_path = file_path
            self.emotions = emotions

        def get_absolute_path(self, app_config: AppConfig):
            """
            Retrieve the absolute file path according to the data directory specified in the application configuration.
            :param app_config: application configuration data.
            :return: absolute audio file path.
            """

            return path.join(app_config.data_dir, self.file_path)

    WORDS = [
        Word(file_path="audio/01.wav", emotions=[Emotions.NEUTRAL, ]),
        Word(file_path="audio/02.wav", emotions=[Emotions.NEUTRAL, ]),
        Word(file_path="audio/03.wav", emotions=[Emotions.CONFUSED, ]),
        Word(file_path="audio/04.wav", emotions=[Emotions.NEUTRAL, ]),
        Word(file_path="audio/05.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/06.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/07.wav", emotions=[Emotions.SCARED, ]),
        Word(file_path="audio/08.wav", emotions=[Emotions.CONFUSED, Emotions.HAPPY]),
        Word(file_path="audio/09.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/10.wav", emotions=[Emotions.NEUTRAL, ]),
        Word(file_path="audio/11.wav", emotions=[Emotions.NEUTRAL, ]),
        Word(file_path="audio/12.wav", emotions=[Emotions.NEUTRAL, ]),
        Word(file_path="audio/13.wav", emotions=[Emotions.NEUTRAL, ]),
        Word(file_path="audio/14.wav", emotions=[Emotions.CONFUSED, ]),
        Word(file_path="audio/15.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/16.wav", emotions=[Emotions.NEUTRAL, ]),
        Word(file_path="audio/17.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/18.wav", emotions=[Emotions.HAPPY, Emotions.CONFUSED]),
        Word(file_path="audio/19.wav", emotions=[Emotions.CONFUSED, ]),
        Word(file_path="audio/20.wav", emotions=[Emotions.SCARED, ]),
        Word(file_path="audio/21.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/22.wav", emotions=[Emotions.SCREAMING, ]),
        Word(file_path="audio/23.wav", emotions=[Emotions.NEUTRAL, ]),
        Word(file_path="audio/24.wav", emotions=[Emotions.NEUTRAL, ]),
        Word(file_path="audio/25.wav", emotions=[Emotions.NEUTRAL, ]),
        Word(file_path="audio/26.wav", emotions=[Emotions.CONFUSED, ]),
        Word(file_path="audio/27.wav", emotions=[Emotions.CONFUSED, ]),
        Word(file_path="audio/28.wav", emotions=[Emotions.NEUTRAL, ]),
        Word(file_path="audio/29.wav", emotions=[Emotions.CONFUSED, ]),
        Word(file_path="audio/30.wav", emotions=[Emotions.CONFUSED, ]),
        Word(file_path="audio/31.wav", emotions=[Emotions.CONFUSED, ]),
        Word(file_path="audio/32.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/33.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/34.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/34.wav", emotions=[Emotions.HAPPY, Emotions.CONFUSED]),
        Word(file_path="audio/35.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/36.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/37.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/38.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/39.wav", emotions=[Emotions.CONFUSED, ]),
        Word(file_path="audio/40.wav", emotions=[Emotions.CONFUSED, ]),
        Word(file_path="audio/41.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/42.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/43.wav", emotions=[Emotions.HAPPY, ]),
        Word(file_path="audio/44.wav", emotions=[Emotions.SCARED, ]),
        Word(file_path="audio/45.wav", emotions=[Emotions.SCREAMING, ]),
        Word(file_path="audio/46.wav", emotions=[Emotions.SCREAMING, ]),
        Word(file_path="audio/47.wav", emotions=[Emotions.SCREAMING, ]),
        Word(file_path="audio/48.wav", emotions=[Emotions.CONFUSED, ]),
    ]

    def __init__(self, parent_path: str = ""):
        """
        Initialize the speech library.
        :param parent_path: the path in which word file paths reside,
        i.e. the path that is the parent to Word.file_path.
        """

        self._parent_path = parent_path

    def get_words(self, emotions: list[Emotions],
                  filtering_method: EmotionFilters = EmotionFilters.INCLUDING) -> list[Word]:
        """
        Retrieve all words according to the specified emotions and filtering method.
        :param emotions: list of emotions to search words by.
        :param filtering_method: how to filter words according to the specified emotions.
        :return: a list of zero or more words that match the query.
        """

        if not isinstance(emotions, list):
            try:
                emotions = list(emotions)
            except TypeError:
                raise TypeError("Expected list of 'Emotions'.")

        for emotion in emotions:
            if not isinstance(emotion, SpeechLibrary.Emotions):
                raise TypeError("Invalid type for 'emotion', expected 'SpeechLibrary.Emotions'.")

        matching_words = list()

        for word in self.WORDS:
            word.file_path = path.join(self._parent_path, word.file_path)

            if filtering_method == SpeechLibrary.EmotionFilters.INCLUDING:
                if all(emotion in word.emotions for emotion in emotions):
                    matching_words.append(word)

            if filtering_method == SpeechLibrary.EmotionFilters.EXCLUSIVE:
                if emotions == word.emotions:
                    matching_words.append(word)

            if filtering_method == SpeechLibrary.EmotionFilters.AT_LEAST_ONE:
                if any(emotion in word.emotions for emotion in emotions):
                    matching_words.append(word)

        return matching_words
