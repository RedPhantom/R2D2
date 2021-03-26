import random

from AIM.AIM import AudioInterface
from AIM.Library import SpeechLibrary
from SCM.Configuration import AppConfig, AudioConfig


def audio_test():
    """
    Test get_word and play_sound.
    """

    speech_lib = SpeechLibrary()
    ai = AudioInterface(AudioConfig())
    words = speech_lib.get_words(emotions=[SpeechLibrary.Emotions.HAPPY],
                                 filtering_method=SpeechLibrary.EmotionFilters.EXCLUSIVE)
    word = random.choice(words)
    ai.play_sound(word.get_absolute_path(AppConfig()))


if __name__ == '__main__':
    audio_test()
