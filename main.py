
import argparse
import configparser
import sys, time, os

sys.path.append("sims")
from sims import get_sim_for
from display import get_display_for
from imu import get_imu_for

#default configuration, overwritten by settings in the config file
DEFAULT_CONFIG = {
    'DEFAULT': {
        'size' : '64x64',
        'sleep_ms' : 10,
        'imu_type' : 'MPUIMU',
        'display_type' : 'RGBMatrixDisplay',
        'sim_type' : 'SandSim',
    },
    'MPUIMU' : {
        'address' : 105,
    },
    'RTIMU' : {
        'settings_file' : 'RTIMULib',
    },
    'DummyIMU' : {
        'random' : True,
    },
    'RGBMatrixDisplay' : {
        'led_hardware_mapping' : 'adafruit-hat-pwm',
        'led_chain' : 1,
        'led_parallel' : 1,
        'led_pwm_bits' : 11,
        'led_brightness' : 100,
        'led_pwm_lsb_nanoseconds' : 130,
        'led_inverse' : False,
        'led_rgb_sequence' : 'RGB',
        'led_pixel_mapper' : '',
        'led_row_addr_type' : 0,
        'led_multiplexing' : 0,
        'led_scan_mode' : 0,
        'led_slowdown_gpio' : 1,
        'led_no_hardware_pulse' : False,
        'led_show_refresh' : False,
        'led_pwm_dither_bits' : 0,
        #'led_panel_type' : '',
    },
    'PILDisplay' : {
    },
    'SandSim' : {
        'num_particles' : "",
    },
    'ArrowSim' : {
        'draw_style' : 'GLU_SILHOUETTE',
        'slices' : 4,
        'stacks' : 2,
        'scale' : 1.5,
        'enable_light' : True,
    },
    'CubeSim' : {
        'rotate': False,
    },
}


def main(args):
    config = configparser.ConfigParser()
    config.read_dict(DEFAULT_CONFIG)

    parser = argparse.ArgumentParser(description='IMU-powered sand simulation displayed on a RGB LED matrix.')
    parser.add_argument('-s', '--size', type=str, help='Size of the display, e.g. 64x32 or 64 (interpreted as 64x64). Will overwrite the setting in the config file.')
    parser.add_argument('-t', '--sleep-ms', type=int, help='Time in ms to sleep between frames. Will overwrite the setting in the config file.')
    parser.add_argument('-c', '--conf', default="config.ini", type=str, help='Config file to use')
    args = parser.parse_args(args)
    

    configfile = args.conf
    if not os.path.exists(configfile):
        print("WARNING: config file doesn't exist! Creating it with default config.")
        with open(configfile, 'w+') as cf:
            config.write(cf)
        #since we run with sudo, fix file ownership
        uid = int(os.environ.get('SUDO_UID'))
        gid = int(os.environ.get('SUDO_GID'))
        os.chown(configfile, uid, gid)
    else:
        config_parsed = configparser.ConfigParser()
        config_parsed.read(configfile)
        config.read_dict(config_parsed)

    if args.size is None:
        args.size = config['DEFAULT']['size']
    if args.sleep_ms is None:
        args.sleep_ms = int(config['DEFAULT']['sleep_ms'])

    size = args.size.split('x')
    try:
        if len(size) == 2:
            size = (int(size[0]), int(size[1]))
        elif len(size) == 1:
            size = int(size[0])
        else: raise Error()
    except:
        raise ValueError("Couldn't parse size, please check that the format is correct: %s" % args.size)
    
    config['DEFAULT']['rows'] = str(size[0])
    config['DEFAULT']['cols'] = str(size[1])
    sleep_ms = args.sleep_ms
    
    # Note: sim needs to be loaded before display
    # sims that use OpenGL require root privileges, and display removes those
    # alternatively: set the led-no-drop-privs flag in RGBMatrix
    sim = get_sim_for(config)
    imu = get_imu_for(config)
    display = get_display_for(config)
    
    try:
        print("Press CTRL-C to stop")
        
        start_time = time.time()
        while True:
            time.sleep(sleep_ms/1000.0)
            end_time = time.time()
            deltatime = end_time-start_time
            start_time = end_time
            
            data = imu.get_data(deltatime)
            sim.step(deltatime, data)
            img = sim.render()
            display.display(img)
            
    except KeyboardInterrupt:
        print("")
        sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
