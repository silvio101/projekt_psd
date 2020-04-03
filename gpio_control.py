#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Control GPIO on Raspberry PI
"""
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
            for i in range(1, 4):
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
            for i in range(1, 4):
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
            for i in range(1, 4):
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
            for i in range(1, 4):
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
            for i in range(1, 4):
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
        if transcr == 'niebieski':
            self.blink_led(Colors.Blue)
        if transcr == 'czerwony':
            self.blink_led(Colors.Red)
        if transcr == 'zielony':
            self.blink_led(Colors.Green)
        if transcr == 'żółty':
            self.blink_led(Colors.Yellow)
        if transcr == 'okno otwórz':
            self.blink_led_white(BlinkMethod.Pulsed)
        if transcr == 'okno zamknij':
            self.blink_led_white(BlinkMethod.Continuous)
        if transcr == 'temperaturę zwiększ':
            self.blink_led_blue(BlinkMethod.Pulsed)
        if transcr == 'temperaturę zmniejsz':
            self.blink_led_blue(BlinkMethod.Continuous)
        if transcr == 'radio głośniej':
            self.blink_led_red(BlinkMethod.Pulsed)
        if transcr == 'radio ciszej':
            self.blink_led_red(BlinkMethod.Continuous)
        if transcr == 'nawiew szybciej':
            self.blink_led_green(BlinkMethod.Pulsed)
        if transcr == 'nawiew wolniej':
            self.blink_led_green(BlinkMethod.Continuous)
        if transcr == 'pulpit jaśniej':
            self.blink_led_yellow(BlinkMethod.Pulsed)
        if transcr == 'pulpit ciemniej':
            self.blink_led_yellow(BlinkMethod.Continuous)


def run_gpio_controller_thread(metrics):
    gpio = GpioController()
    while metrics['ready']:
        if metrics['data'] is not None:
            gpio.make_decision(metrics['data'])
            metrics['data'] = None
