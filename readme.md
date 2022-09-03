# Box of Life



![box](doc\img\box.gif)



Ikea FREKVENS modification with **Raspberry Pi Pico** to play [Conway's **Game of Life**](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

## Control

- Red button
    - *short press* - turn ON and cycle LED brightness
    - *long press* - turn OFF 
- Yellow button
    - *short press* - cycle generation speed
    - *long press* - restart life

## Ikea FREKVENSE HW Modification

One need to disassembly Ikea FREKVCENS box, remove original MCU board and connect RPi Pico. Steps:

1. Disassembly, there are some tutorials already, e.g. [here](https://spritesmods.com/?art=frekvens&page=2) or [here](https://github.com/frumperino/FrekvensPanel/blob/master/frekvens-hacking.pdf)
2. Remove original MCU (green) PCB and solder there connector (or directly connect according to the following table via wires). 
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

Connection between powersupply and main PCB (4V and GND) is same.

‼ **If USB connection is used, one must de-solder diode that are between `VUSB` and `VSYS` from Pico PCB.**

## Ideas for improvements

- Add predefined startup (e.g. glider)
- Performance improvement (use SPI or PIO for communication, speed up game generation computation)
