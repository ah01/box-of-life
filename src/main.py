import machine
import time
from machine import Pin, PWM
import framebuf
import random

mode_btn = machine.Pin(10, machine.Pin.IN, Pin.PULL_UP);
pwr_btn = machine.Pin(11, machine.Pin.IN, Pin.PULL_UP);


clk_pin = machine.Pin(2, machine.Pin.OUT);
data_pin = machine.Pin(3, machine.Pin.OUT);
en_pin = machine.Pin(4, machine.Pin.OUT);
latch_pin = machine.Pin(5, machine.Pin.OUT);

pwm0 = PWM(en_pin)

p = 1

pwm0.duty_u16(65534 - p*655)

print("start")

def send_bit(val):
    if val:
        data_pin.on()
    else:
        data_pin.off()
    clk_pin.on()
    clk_pin.off() 
    
def send_byte(val):
    for x in range(0,8):
        send_bit(val & (1 << x) > 0)
    
def send_buffer(b):
    en_pin.off()

    for i in range(0,32):
        send_byte(b[i])
    
    latch_pin.on()
    time.sleep_ms(1)
    latch_pin.off()
    time.sleep_ms(1)

def setp(buff, x, y, v):
    B = x
    if (y >= 8):
        B = B + 16
    b = y % 8
    
    if (v):
        buff[B] = buff[B] | (1 << b)
    else:
        buff[B] = buff[B] & (~(1 << b))

def getp(buff, x, y):
    return (buff[x if y < 8 else x + 16] & (1 << (y % 8))) > 0 #if 1 else 0

def clear(buff):
    for i in range(0,32):
        buff[i] = 0

def init_random(buff):
    for i in range(0,32):
        buff[i] = random.randrange(0, 255)

def val2(buffer, x, y):
    if (x >= 16 or x < 0 or y >= 16 or y < 0):
        return 0
    return getp(buffer, x, y)

def val(buffer, x, y):
    return getp(buffer, x % 16, y % 16)


def iterate(src, target):
    clear(target)
    for i in range(0, 16):
        for j in range(0, 16):
            total = val(src, i-1, j-1) + val(src, i, j-1) + val(src, i+1, j-1) + val(src, i-1, j) + val(src, i+1, j) + val(src, i-1, j+1) + val(src, i, j+1) + val(src, i+1, j+1)
            if (getp(src, i, j)):
                if (total < 2) or (total > 3):
                    setp(target, i, j, 0)
                else:
                    setp(target, i, j, 1)
            else:
                if (total == 3):
                    setp(target, i, j, 1)
                else:
                    setp(target, i, j, 0)
    send_buffer(target)
    

buffer1 = bytearray(32)
buffer2 = bytearray(32)

print(buffer1 == buffer2)


beg = [
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 1 0 0 0 0 1 0 1 0 0 0 0 1 0",
    "0 0 1 0 0 0 0 1 0 1 0 0 0 0 1 0",
    "0 0 1 0 0 0 0 1 0 1 0 0 0 0 1 0",
    "0 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0",
    "0 0 1 0 0 0 0 1 0 1 0 0 0 0 1 0",
    "0 0 1 0 0 0 0 1 0 1 0 0 0 0 1 0",
    "0 0 1 0 0 0 0 1 0 1 0 0 0 0 1 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
]

beg3 = [
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
]

beg2 = [
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0",
    "0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0",
    "0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0",
    "0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
    "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
]

def fill(src, target):
    for y in range(0,16):
        x = 0
        for a in src[y]:
            if (a == " "):
                continue
            setp(target, x, y, a == "1")
            x = x + 1



b = 1
buffer1[4] = 0b1110000
buffer1[3] = 0b0010000
buffer1[2] = 0b0100000
#buffer1[5] = 0b11110000 

D = 50
init_random(buffer1)
#fill(beg2, buffer1)

def print_B(b):
    for i in range(0, 16):
        s = ""
        for j in range(0, 16):
            if (getp(b,i,j) == 1):
                s = s + " X"
            else:
                s = s + " ."                        
        print(s)


send_buffer(buffer1)

buffers = [
    bytearray(32), bytearray(32), bytearray(32)        
]

#init_random(buffers[0])

buffers[0][5] = 0b0111000

bi = 0

for i in range(50000):
    ne = (bi + 1) % 3
    iterate(buffers[bi], buffers[ne])
    bi = ne
    
    if (buffers[0] == buffers[1] or buffers[1] == buffers[2] or buffers[0] == buffers[2]):
        print("Stable")
       
        clear(buffers[ne])
        send_buffer(buffers[ne])
        init_random(buffers[ne])
        time.sleep(2)
        
    time.sleep_ms(D)
    



for i in range(10000):

    time.sleep_ms(D)
    iterate(buffer1, buffer2)
    time.sleep_ms(D)
    iterate(buffer2, buffer1)
        
    if (buffer1 == buffer2):
        print("restart")
        clear(buffer1)
        send_buffer(buffer1)
        init_random(buffer1)
        time.sleep(2)
        init_random(buffer1)
    
    if (pwr_btn.value() == 0):
        print("PWR")
        init_random(buffer1)
        
    if(mode_btn.value() == 0):
        print("Mode")
    
clear(buffer1)
send_buffer(buffer1)

