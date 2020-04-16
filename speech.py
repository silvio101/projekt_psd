#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module with speech process function
GoogleAPI is operated here
"""
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from audio import MicrophoneStream, listen_print_loop
from google.api_core.exceptions import OutOfRange, ServiceUnavailable
from time import sleep

RATE = 44000
CHUNK = int(RATE / 10)


def run_speech_thread(metrics):
    language_code = 'pl-PL'
    while True:
        client = speech.SpeechClient()
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code
        )
        streaming_config = types.StreamingRecognitionConfig(
            config=config,
            interim_results=True
        )

        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)
            try:
                listen_print_loop(responses, metrics)
            except OutOfRange as err:
                print("[Google speech api] Timeout... {0}".format(err))
            except ServiceUnavailable as err:
                print("[Google speech api] All services unavailable... {0}".format(err))

            while not metrics['conn_e']:
                sleep(5)
