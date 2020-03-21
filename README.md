# Matrix Box

A box powered by a raspberry pi, using data from an IMU to display various simulations on a RGB LED matrix.

The original goal of this project was to make a simulated box of sand. Tilting the box would move the sand, inspired by [adafruit link]. I bought a 64x64 LED matrix, 3D-printed a small casing and put a raspberry pi (running Raspian Lite) together with an IMU into it. Below are some demo videos of the sand simulation, as well as 3D animations using OpenGL. 

The files for the 3D printed case can be downloaded [here]. Instructions containing all the necessary steps to build the project can be found [here].



## Demos


## Requirements
The hardware setup is described [here]. 

### System requirements

- rpi-rgb-matrix
- RTIMULib (if you don't want to use the mpu6050 python package)
- OpenGL libraries (should already be installed with Raspian)

### Python requirements
The project should work with both Python 2 and 3 (I tested 2.7.16 and 3.7.3 specifically). Install the following python packages:

- `numpy`
- `mpu6050-raspberrypi` (if you don't want to use RTIMULib)
- `PIL` (should be installed with the rgb-matrix library)

## Running and configuration

Run the project by simply executing:
```bash
sudo python main.py
```
The script needs to be run with root privileges, required by the RGB LED matrix library (as well as the headless OpenGL library, I think).

The `config.ini` contains various configuration parameters to choose what simulation to run and for tweaking the simulation itsself (see corresponding sections of each simulation). It also has parameters for the RGB Matrix and the IMU libraries. 
A quick overview of the simulations is given here:

- SandSim: simulates sand, could be extended to make a labyrinth game
- CubeSim: a 3D-wireframe rendered cube, rotating either on its own or using the IMU
- ArrowSim: arrow that always points upwards regardless of the orientation of the box