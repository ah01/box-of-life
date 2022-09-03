# Box *full* of Life

<p align="center">
<img src="https://github.com/ah01/box-of-life/raw/master/doc/box.gif">
</p>

Modification of [Ikea FREKVENS](https://www.ikea.com/cz/en/p/frekvens-led-multi-use-lighting-black-30420354/) with **Raspberry Pi Pico** to play [Conway's **Game of Life**](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

## Features

- Start with random pattern and play *game of life* 
- If stable pattern or [oscillator](https://conwaylife.com/wiki/Oscillator) with period 2 occurs game will be restarted.
- Control:
  - Red button
     - *short press* - turn ON and cycle LED brightness
     - *long press* - turn OFF 
  - Yellow button
      - *short press* - cycle speed
      - *long press* - restart life

## Firmware

FW is written in [MicroPython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html). 
Use [Thonny](https://thonny.org/) or [`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html) 
to load content of `src` directory into Pico.

```bash
cd src
# copy everything (.) in to remote (:)
mpremote cp -r . :
# run main.py to see stdout
mpremote run main.py
```

## Ikea FREKVENS HW Modification

One need to disassembly Ikea FREKVENS box, remove original MCU board and connect RPi Pico. Steps:

1. Disassembly, there are some tutorials already, e.g. [here](https://spritesmods.com/?art=frekvens&page=2) or [here](https://github.com/frumperino/FrekvensPanel/blob/master/frekvens-hacking.pdf)
2. Remove original MCU (green) PCB and solder connector in place (or directly connect according to the following table via wires). 
3. (optional) disassembly power supply block and replace AC output plug with 3D printed [USB connector holder](https://www.printables.com/model/262441-usb-connector-holder-for-ikea-frekvens). USB data pins are available on back side of RPi Pico as test points.

### Connection

| Board     | Pin/Wire   | RPi Pico PIN | Note          |
|-----------|------------|--------------|---------------|
| LED PCB   | 1 (Vcc)    | VSYS         |               |
| LED PCB   | 2          | GPIO 4       | En            |
| LED PCB   | 3          | GPIO 3       | Data          |
| LED PCB   | 4          | GPIO 2       | Clk           |
| LED PCB   | 5          | GPIO 5       | Latch         |
| LED PCB | 6 (Gnd)    | GND          |               |
| Buttons | Red wire   | GND          |               |
| Buttons | Black wire | GPIO 10      | Yellow button |
| Buttons | White wire | GPIO  11     | Red button    |

Connection between power supply and main PCB (4V and GND) is same.

‼ **If USB connection is used, one must de-solder diode that are between `VUSB` and `VSYS` from Pico PCB.**

## Ideas for improvements

- Add predefined startup (e.g. glider)
- Performance improvement (use SPI or PIO for communication, speed up game generation computation)
