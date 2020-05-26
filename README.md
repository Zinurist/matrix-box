# Matrix Box

A box powered by a raspberry pi, using data from an IMU to display various simulations on a RGB LED matrix.

The original goal of this project was to make a simulated box of sand. Tilting the box would move the sand, inspired by [adafruit's demo video](https://cdn-shop.adafruit.com/product-videos/1200x900/3649-06.mp4). I bought a 64x64 LED matrix, 3D-printed a small casing and put a raspberry pi (running Raspian Lite) together with an IMU into it. Below are some demo videos of the sand simulation, as well as 3D animations using OpenGL. 

The files for the 3D-printed case can be downloaded [here](https://www.thingiverse.com/thing:4248711).



## Demos

[![SandSim](https://thumbs.gfycat.com/FlamboyantShockedCleanerwrasse-small.gif)](https://gfycat.com/flamboyantshockedcleanerwrasse)

* [Wireframe Cube rotating](https://gfycat.com/gracefuldistantasiandamselfly) (the cube and animation was taken from [here](https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/))
* [Wireframe Cube with IMU](https://gfycat.com/clumsyenlightenedboto)
* [Arrow rotating](https://gfycat.com/admirableadorableglobefish)
* [Arrow with IMU](https://gfycat.com/wildnaughtyfirebelliedtoad)
* [Blinking stars](https://gfycat.com/totalflippantaplomadofalcon)
* [Dodo sim](https://gfycat.com/secondforcefulbarnswallow)


## Requirements

### Hardware setup

You will need the following:

* Raspberry Pi 2 or 3 (haven't tested OpenGL with a pi 4)
* a RGB LED matrix, I used [this](https://www.aliexpress.com/item/32966322666.html) 64x64 matrix
* [Adafruit's RGB Matrix HAT](https://www.adafruit.com/product/2345) for raspberry pi
* an IMU, I used a MPU6050, that can be connected via I2C and doesn't use address 0x68 (if it does, check if it has an AD0 pin, see below)
* a power supply, for 64x64 it should deliver at least 8A (adafruit has more info on this)
* optionally [this](https://www.thingiverse.com/thing:4248711) 3D-printed case (or make one of your own if you have a different LED matrix)

Adafruit provides a [great tutorial](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi) on setting up the LED matrix with a raspberry pi. Additionally, you'll have to connect the IMU (simply connect the SDA, SCL, 3.3V (VCC) and GND pins between IMU and the Matrix HAT) and make sure to enable I2C. My IMU used address 0x68 on the I2C bus, which is already used by the RTC of the Matrix HAT (I had problems even when disabling it in the setup script), but the IMU provided an AD0 pin, that changed the address to 0x69 when set high. The default configuration in this project also expects the IMU to be available at 0x69 (decimal: 105), and can be changed in [config.ini](config.ini).

The 3D printed case makes the entire project a pretty, contained box. I attached the pi in the box simply with Blu Tack.

### System requirements

- rpi-rgb-matrix
- RTIMULib (if you don't want to use the mpu6050 python package)

RTIMULib needs to be calibrated. I never really got this library working, so I recommend mpu6050 for now. mpu6050 however doesn't provide fused IMU data, but it works well enough.

### OpenGL requirements

This project was designed to run on Raspian Lite, meaning I needed to run Open GL on a headless pi (no GUI etc., in particular no X11). I used [eduble](https://github.com/eduble/gl)'s library for this, check the submodule out by running:
```bash
git submodule update --init --recursive
```

You'll also have to make sure that OpenGL is enabled on your pi. Run `sudo raspi-config` and in *Advanced Options > GL Driver* change to the second option, GL (Fake KMS).

In the future, I'll add an option to change between eduble's library for a headless pi and the normal PyOpenGL library for a desktop pi.

### Python requirements
The project should work with both Python 2 and 3 (I tested 2.7.16 and 3.7.3 specifically). Since it needs to be run with root privileges, make sure that all required packages are part of the python path when running python as root. This can be done by either installing the pre-compiled libraries provided by your distro (i.e. `sudo apt install python-XXX`), or by running pip with sudo (generally discouraged, but shouldn't matter for a embedded project like this). The following python packages are needed:

- `numpy`
- `PyOpenGL` and preferably `PyOpenGL_accelerate` (for animations relying on OpenGL)
- `mpu6050-raspberrypi` (if you don't want to use RTIMULib)
- `PIL` (will be installed with the rgb-matrix library)

## Running and configuration

Run the project by simply executing:
```bash
sudo python main.py
```
The script needs to be run with root privileges, required by the RGB LED matrix library (as well as the headless OpenGL library, I think).

The [config.ini](config.ini) contains various configuration parameters to choose what simulation to run and for tweaking the simulation itsself (see corresponding sections of each simulation). It also has parameters for the RGB Matrix and the IMU libraries. 
A quick overview of the simulations is given here:

- SandSim: Simple simulation of sand, could be extended to make a labyrinth game.
- CubeSim: A 3D-wireframe rendered cube, rotating either on its own or using the IMU.
- ArrowSim: Arrow that always points upwards regardless of the orientation of the box.
- StarSim: Displays blinking stars, randomly distributed, optionally with a "random" galaxy.
- DodoSim: Small simulation where dodos need to search for food (green dots). Each dodo has a DNA made of 3 values that are used for the RGB values: range (red, how far they see), speed (blue, how fast they move) and life (green, influences rate of deat+reproduction). The idea was to let it run for a while and see if a specific DNA takes over.
