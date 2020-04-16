#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Control GPIO on Raspberry PI
"""
from audio import PlaySound
from gpiozero import LED
from time import sleep
import enum


class Colors(enum.Enum):
    White = 21
    Blue = 16
    Red = 12
    Green = 5
    Yellow = 25


class BlinkMethod(enum.Enum):
    Pulsed = 1
    Continuous = 2


class GpioController:
    def __init__(self):
        self.__white_led = LED(Colors.White.value)
        self.__blue_led = LED(Colors.Blue.value)
        self.__red_led = LED(Colors.Red.value)
        self.__green_led = LED(Colors.Green.value)
        self.__yellow_led = LED(Colors.Yellow.value)

    def blink_led_white(self, mode):
        if mode is BlinkMethod.Continuous:
            self.__white_led.on()
            sleep(4)
            self.__white_led.off()
        if mode is BlinkMethod.Pulsed:
            for _ in range(1, 4):
                self.__white_led.on()
                sleep(1)
                self.__white_led.off()
                sleep(1)

    def blink_led_blue(self, mode):
        if mode is BlinkMethod.Continuous:
            self.__blue_led.on()
            sleep(4)
            self.__blue_led.off()
        if mode is BlinkMethod.Pulsed:
            for _ in range(1, 4):
                self.__blue_led.on()
                sleep(1)
                self.__blue_led.off()
                sleep(1)

    def blink_led_red(self, mode):
        if mode is BlinkMethod.Continuous:
            self.__red_led.on()
            sleep(4)
            self.__red_led.off()
        if mode is BlinkMethod.Pulsed:
            for _ in range(1, 4):
                self.__red_led.on()
                sleep(1)
                self.__red_led.off()
                sleep(1)

    def blink_led_green(self, mode):
        if mode is BlinkMethod.Continuous:
            self.__green_led.on()
            sleep(4)
            self.__green_led.off()
        if mode is BlinkMethod.Pulsed:
            for _ in range(1, 4):
                self.__green_led.on()
                sleep(1)
                self.__green_led.off()
                sleep(1)

    def blink_led_yellow(self, mode):
        if mode is BlinkMethod.Continuous:
            self.__yellow_led.on()
            sleep(4)
            self.__yellow_led.off()
        if mode is BlinkMethod.Pulsed:
            for _ in range(1, 4):
                self.__yellow_led.on()
                sleep(1)
                self.__yellow_led.off()
                sleep(1)

    def blink_led(self, color):
        if color == Colors.White:
            self.__white_led.on()
            sleep(3)
            self.__white_led.off()
        if color == Colors.Blue:
            self.__blue_led.on()
            sleep(3)
            self.__blue_led.off()
        if color == Colors.Red:
            self.__red_led.on()
            sleep(3)
            self.__red_led.off()
        if color == Colors.Green:
            self.__green_led.on()
            sleep(3)
            self.__green_led.off()
        if color == Colors.Yellow:
            self.__yellow_led.on()
            sleep(3)
            self.__yellow_led.off()

    def make_decision(self, transcr):
        if transcr == 'biały':
            self.blink_led(Colors.White)
        elif transcr == 'niebieski':
            self.blink_led(Colors.Blue)
        elif transcr == 'czerwony':
            self.blink_led(Colors.Red)
        elif transcr == 'zielony':
            self.blink_led(Colors.Green)
        elif transcr == 'żółty':
            self.blink_led(Colors.Yellow)
        elif transcr == 'okno otwórz':
            self.blink_led_white(BlinkMethod.Pulsed)
        elif transcr == 'okno zamknij':
            self.blink_led_white(BlinkMethod.Continuous)
        elif transcr == 'temperaturę zwiększ':
            self.blink_led_blue(BlinkMethod.Pulsed)
        elif transcr == 'temperaturę zmniejsz':
            self.blink_led_blue(BlinkMethod.Continuous)
        elif transcr == 'radio głośniej':
            self.blink_led_red(BlinkMethod.Pulsed)
        elif transcr == 'radio ciszej':
            self.blink_led_red(BlinkMethod.Continuous)
        elif transcr == 'nawiew szybciej':
            self.blink_led_green(BlinkMethod.Pulsed)
        elif transcr == 'nawiew wolniej':
            self.blink_led_green(BlinkMethod.Continuous)
        elif transcr == 'pulpit jaśniej':
            self.blink_led_yellow(BlinkMethod.Pulsed)
        elif transcr == 'pulpit ciemniej':
            self.blink_led_yellow(BlinkMethod.Continuous)
        else:
            with PlaySound() as play:
                play.play_wrong_command()


def run_gpio_controller_thread(metrics):
    gpio = GpioController()
    while metrics['ready']:
        if metrics['data'] is not None:
            gpio.make_decision(metrics['data'])
            metrics['data'] = None
