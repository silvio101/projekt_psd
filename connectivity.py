#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Helper methods and classes
"""
import socket
from time import sleep
from audio import PlaySound


def run_connectivity_thread(metrics):
    while True:
        try:
            sock = socket.create_connection(('google.com', 443), timeout=3)
            metrics['conn_e'].clear()
        except socket.timeout:
            print('Timeout error')
            metrics['conn_e'].set()
            with PlaySound() as play:
                play.play_nointernet()
        except socket.error:
            print('Socker error')
            metrics['conn_e'].set()
            with PlaySound() as play:
                play.play_nointernet()
        # print(not(metrics['conn_e'].isSet()))
        sleep(5)
