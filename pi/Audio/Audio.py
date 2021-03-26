# Module:  Audio Interface Manager
# Purpose: Provide an interface to all audio and sound-related aspects of the droid.

from os import path

from pydub import AudioSegment
from pydub.playback import play

from SCM.Configuration import AudioConfig
from TLM.TLM import AppExceptions


class AudioInterface:
    class Defaults:
        VOLUME = 1.0

    def __init__(self, audio_config: AudioConfig):
        self._config = audio_config

    def play_sound(self, file_path: str, volume: float = Defaults.VOLUME):
        """
        Play a sound file in the background at the specified volume.
        :param file_path: path to the sound file to play.
        :param volume: adjustment to the audio file amplitude, in Decibels.
        """

        if not path.exists(file_path):
            raise AppExceptions.InvalidPathException(file_path)

        if volume > 1 or volume < 0:
            raise ValueError("'volume' must be between 0 and 1.")

        sound = AudioSegment.from_wav(file_path)

        sound = sound[:] + volume

        play(sound)
