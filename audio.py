#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module with functions which process speech from microphone
"""
import pyaudio
import wave
import sys
import re
from six.moves import queue


class PlaySound(object):
    """
    Play warning sound
    """
    def __init__(self):

        self.chunk = 1024
        self.no_internet = wave.open('files/nointernet.wav', 'rb')
        self.wrong_command = wave.open('files/wrong_command.wav', 'rb')

    def __enter__(self):
        self.__pyaudio_interface = pyaudio.PyAudio()
        self.__pyaudio_stream = self.__pyaudio_interface.open(
            format=8, channels=1, rate=48000, output=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__pyaudio_stream.stop_stream()
        self.__pyaudio_stream.close()
        self.__pyaudio_interface.terminate()

    def play_nointernet(self):
        data = self.no_internet.readframes(self.chunk)
        while data != b'':
            self.__pyaudio_stream.write(data)
            data = self.no_internet.readframes(self.chunk)

    def play_wrong_command(self):
        data = self.wrong_command.readframes(self.chunk)
        while data != b'':
            self.__pyaudio_stream.write(data)
            data = self.wrong_command.readframes(self.chunk)


class MicrophoneStream(object):
    """
    Open a recording stream
    """
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue()
        self.closed = True

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate, input=True,
            frames_per_buffer=self._chunk, stream_callback=self._fill_buffer,
        )

        self.closed = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses, metrics):
    num_chars_printed = 0
    try:
        for response in responses:
            if not response.results:
                continue
            result = response.results[0]

            if not result.alternatives:
                continue
            transcript = result.alternatives[0].transcript

            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                print(transcript + overwrite_chars)
                metrics['data'] = transcript.lower().strip()
                metrics['ready'] = True
                if re.search(r'\b(exit|quit)\b', transcript, re.I):
                    print('Exiting..')
                    break
                num_chars_printed = 0
    except KeyboardInterrupt as err:
        print(err)
