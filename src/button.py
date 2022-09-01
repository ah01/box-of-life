import time
import uasyncio
from micropython import const


LONG_PRESS_MS = const(600)
DEBOUNCE_INTERVAL = const(20)


async def wait_for(pin, value):
    while True:
        if pin.value() == value:
            await uasyncio.sleep_ms(DEBOUNCE_INTERVAL)
            if pin.value() == value:
                return
        await uasyncio.sleep_ms(DEBOUNCE_INTERVAL)


async def wait_for_or_timeout(pin, value, timeout):
    start = time.ticks_ms()
    while True:
        if pin.value() == value:
            await uasyncio.sleep_ms(20)
            if pin.value() == value:
                return time.ticks_diff(time.ticks_ms(), start)
        await uasyncio.sleep_ms(20)
        if time.ticks_diff(time.ticks_ms(), start) > timeout:
            return -1


async def create_btn_task(pin, short_fn, long_fn):
    while 1:
        await wait_for(pin, 0)
        dur = await wait_for_or_timeout(pin, 1, LONG_PRESS_MS)
        if dur == -1 or dur > LONG_PRESS_MS:
            long_fn()
        else:
            short_fn()
        await wait_for(pin, 1)
