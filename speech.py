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

RATE = 44000
CHUNK = int(RATE / 10)


def run_speech_thread(transcription):
    language_code = 'pl-PL'

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

        listen_print_loop(responses, transcription)
