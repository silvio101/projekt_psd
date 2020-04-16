#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main controller class, broker for other functions
"""
from sys import argv
from threading import Thread, Event
from speech import run_speech_thread
from gpio_control import run_gpio_controller_thread
from connectivity import run_connectivity_thread


class Controller:
    def __init__(self):
        event = Event()
        self.metrics = {'ready': False, 'data': [], 'conn': False, 'conn_e': event}
        self.threads = []

    def run_threads(self):
        self.threads.append(Thread(target=run_connectivity_thread, name='ConnectivityThread', args=(self.metrics,)))
        self.threads.append(Thread(target=run_speech_thread, name='SpeechThread', args=(self.metrics,)))
        self.threads.append(Thread(target=run_gpio_controller_thread, name='GpioThread', args=(self.metrics,)))
        self.threads[0].start()
        self.threads[1].start()
        while not self.metrics['ready']:
            continue
        self.threads[2].start()


def main(args):
    controller = Controller()
    controller.run_threads()


def run():
    """
    Entry point for consle_run
    :return:
    """
    main(argv[1:])
