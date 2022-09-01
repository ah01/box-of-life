import gc
import uasyncio
from micropython import const
from machine import Pin

from button import create_btn_task
from display import Screen, pwm
from game import next_gen


# --- Global vars. ------------------------------------------------------------

# buttons:
mode_btn = Pin(10, Pin.IN, Pin.PULL_UP)
pwr_btn = Pin(11, Pin.IN, Pin.PULL_UP)

GENERATION_DELAY = const(50)

# led brightness
current_pwm = 0
pwm_options = [65500, 65000, 50000, 20000, 0]

# generation delay
current_t = 0
t_options = [50, 0, 500, 1000]

# state control
is_on = True
reset_requested = True
restart_event = uasyncio.Event()

# game screen buffers
buffers = [
    Screen(), Screen(), Screen()
]


# --- Game  -------------------------------------------------------------------


async def restart_game():
    print("Restart game")
    await uasyncio.sleep_ms(GENERATION_DELAY * 2)
    buffers[0].clear()
    buffers[0].show()
    await uasyncio.sleep_ms(GENERATION_DELAY * 2)
    # fill random and calculate first generation without showing it
    # there is typically big visual step between first random generation and next one, so we will start with second gen.
    buffers[2].fill_random()
    await next_gen(buffers[2], buffers[0])
    buffers[0].show()


async def game_task(t):
    bi = 0  # current buffer index
    osc = 0  # oscillation counter (we want to keep oscillate for while and then restart)
    print("Start game (delay {} ms)".format(t))
    try:
        while True:
            ni = (bi + 1) % 3
            await next_gen(buffers[bi], buffers[ni])
            buffers[ni].show()

            # detect stable and oscillations in game
            if buffers[bi] == buffers[ni]:
                print("Stable")
                await restart_game()
                ni = 0
            elif buffers[0] == buffers[2]:
                print("Oscillate")
                osc += 1
                if osc >= 3:
                    await restart_game()
                    ni = 0
                    osc = 0

            bi = ni
            await uasyncio.sleep_ms(t)

    except uasyncio.CancelledError:
        pass


async def mem_cleanup_info():
    while 1:
        gc.collect()
        gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

        f = gc.mem_free()
        a = gc.mem_alloc()
        t = a+f
        print("MEM Used {} % (Free: {}, Alloc: {}, Tot: {})".format(100*a/t, f, a, t))
        await uasyncio.sleep(10)


# --- Button handlers ---------------------------------------------------------

def pwr_short_press():
    print("Power short press")
    global current_pwm, is_on
    if is_on:
        current_pwm = (current_pwm + 1) % len(pwm_options)
        print("PWM: {}".format(current_pwm))
        pwm.duty_u16(pwm_options[current_pwm])
    else:
        is_on = True
        restart_event.set()
        print(is_on)


def pwr_long_press():
    print("Power long press")
    global is_on
    is_on = False
    print(is_on)
    restart_event.set()


def mode_short_press():
    print("Mode short press")
    global current_t
    current_t = (current_t + 1) % len(t_options)
    restart_event.set()


def mode_long_press():
    global reset_requested
    print("Mode long press")
    reset_requested = True
    restart_event.set()


# --- Main --------------------------------------------------------------------

async def main():
    uasyncio.create_task(mem_cleanup_info())

    # button handler tasks
    uasyncio.create_task(create_btn_task(pwr_btn, pwr_short_press, pwr_long_press))
    uasyncio.create_task(create_btn_task(mode_btn, mode_short_press, mode_long_press))

    # main loop
    global reset_requested, is_on

    while True:
        if reset_requested:
            await restart_game()
            reset_requested = False

        if is_on:
            print("Start game")
            gt = uasyncio.create_task(game_task(t_options[current_t]))
        else:
            print("Turn off game")
            buffers[0].clear()
            buffers[0].show()

        await restart_event.wait()
        gt.cancel()
        restart_event.clear()


print("Start main")
uasyncio.run(main())
