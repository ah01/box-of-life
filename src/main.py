import machine
import time
from machine import Pin, PWM, Timer
import framebuf
import random
from display import Screen
import game

mode_btn = machine.Pin(10, machine.Pin.IN, Pin.PULL_UP);
pwr_btn = machine.Pin(11, machine.Pin.IN, Pin.PULL_UP);





print("start")

D = 50

buffers = [
    Screen(), Screen(), Screen()
]

buffers[0].fill_random()

#buffers[0][5] = 0b0111000

bi = 0
last = time.ticks_ms()


def draw(t):
    global last
    
    now = time.ticks_ms()
    #print (now - last)
    last = now
    
    global bi
    
    ne = (bi + 1) % 3
    game.next_get(buffers[bi], buffers[ne])
    bi = ne
    
    if (buffers[0] == buffers[1] or buffers[1] == buffers[2] or buffers[0] == buffers[2]):
        print("Stable")
       
        buffers[ne].clear()
        buffers[ne].show()
        buffers[ne].fill_random()
        buffers[ne].show()


tim = Timer(period=200, mode=Timer.PERIODIC, callback=draw)

