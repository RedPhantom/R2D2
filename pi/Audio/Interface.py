# Purpose: Provide an interface to all audio and sound-related aspects of the droid.

from os import path

from pydub import AudioSegment
from pydub.playback import play

from Configuration.Configuration import AudioConfig
from Telemetry.Telemetry import AppExceptions


class AudioInterface:
    class Defaults:
        VOLUME = 1.0

    def __init__(self, audio_config: AudioConfig):
        self._config = audio_config

    @staticmethod
    def play_sound(file_path: str, volume_adjustment: float = Defaults.VOLUME):
        """
        Play a sound file in the background at the specified volume.

        :param file_path: path to the sound file to play.
        :param volume_adjustment: adjustment to the audio file amplitude, in Decibels.
        """

        if not path.exists(file_path):
            raise AppExceptions.InvalidPathException(file_path)

        sound = AudioSegment.from_file(file_path)
        sound = sound[:] + volume_adjustment

        play(sound)
