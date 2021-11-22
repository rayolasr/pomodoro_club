import sys
import time

from pydub import AudioSegment
from pydub.playback import play


class Counter:
    def __init__(self):
        print('Creating counter')
        self.seconds = 0

    def start_countdown(self, duration):
        self.seconds = duration
        print('Starting countdown')
        for i in range(duration, 0, -1):
            sys.stdout.write(str(i))
            self.seconds = i
            time.sleep(1)
            sys.stdout.write('\r')

        play(AudioSegment.from_wav("assets/sounds/notification.wav"))
        print('Production time is finished. Extending production time')

    def start_countup(self):
        print('Starting count')
        for i in range(0, 5, 1):
            sys.stdout.write(str(i))
            self.seconds = i
            time.sleep(1)
            sys.stdout.write('\r')

        play(AudioSegment.from_wav("assets/sounds/notification.wav"))

    def finish(self):
        pass
