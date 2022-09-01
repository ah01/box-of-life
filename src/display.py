import machine
import time
from machine import Pin, PWM, Timer
import random

# --- HW -------------------------------------------

# GPIO:

clk_pin = machine.Pin(2, machine.Pin.OUT)
data_pin = machine.Pin(3, machine.Pin.OUT)
en_pin = machine.Pin(4, machine.Pin.OUT)
latch_pin = machine.Pin(5, machine.Pin.OUT)

pwm = PWM(en_pin)


# Send data:

# TODO: Use SPI or PIO instead of bitbanging

def toggle(pin):
    pin.on()
    pin.off()


def send_bit(val):
    if val:
        data_pin.on()
    else:
        data_pin.off()
    toggle(clk_pin)


def send_byte(val):
    for x in range(0, 8):
        send_bit(val & (1 << x) > 0)


def send_buffer(b):
    for i in range(0, 32):
        send_byte(b[i])
    toggle(latch_pin)


# --- buffer operations -------------------------------------------

class Screen:

    def __init__(self):
        self.buffer = bytearray(32)

    def __eq__(self, other):
        return self.buffer == other.buffer

    def get(self, x, y):
        return (self.buffer[x if y < 8 else x + 16] & (1 << (y % 8))) > 0

    def set(self, x, y, v):
        i = x if y < 8 else x + 16
        b = y % 8
        if v:
            self.buffer[i] = self.buffer[i] | (1 << b)
        else:
            self.buffer[i] = self.buffer[i] & (~(1 << b))

    def clear(self):
        for i in range(0, 32):
            self.buffer[i] = 0

    def fill_random(self):
        for i in range(0, 32):
            self.buffer[i] = random.randrange(0, 255)

    def show(self):
        send_buffer(self.buffer)

    def print(self):
        for x in range(0, 16):
            s = ""
            for y in range(0, 16):
                if self.get(x, y) == 1:
                    s = s + " X"
                else:
                    s = s + " ."
        print(s)
