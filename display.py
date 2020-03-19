
from PIL import Image

def get_display_for(config):
    display_type = config['DEFAULT']['display_type']

    if display_type == 'RGBMatrixDisplay':
        display = RGBMatrixDisplay(config['RGBMatrixDisplay'])
    elif display_type == 'PILDisplay':
        display = PILDisplay(config['PILDisplay'])
    else:
        raise ValueError('Unknown Display type: %s' % display_type)
    return display


class RGBMatrixDisplay():

    def __init__(self, config):
        from rgbmatrix import RGBMatrix, RGBMatrixOptions
        options = RGBMatrixOptions()

        options.rows = config.getint('rows')
        options.cols = config.getint('cols')
        options.hardware_mapping = config['led_hardware_mapping']

        options.chain_length = config.getint('led_chain')
        options.parallel = config.getint('led_parallel')
        options.pwm_bits = config.getint('led_pwm_bits')
        options.brightness = config.getint('led_brightness')
        options.pwm_lsb_nanoseconds = config.getint('led_pwm_lsb_nanoseconds')
        options.inverse_colors = config.getboolean('led_inverse')
        options.led_rgb_sequence = config['led_rgb_sequence']
        options.pixel_mapper_config = config['led_pixel_mapper']
        options.row_address_type = config.getint('led_row_addr_type')
        options.multiplexing = config.getint('led_multiplexing')
        options.scan_mode = config.getint('led_scan_mode')
        options.gpio_slowdown = config.getint('led_slowdown_gpio')
        options.disable_hardware_pulsing = config.getboolean('led_no_hardware_pulse')
        options.show_refresh_rate = config.getboolean('led_show_refresh')
        options.pwm_dither_bits = config.getint('led_pwm_dither_bits')
        #options.panel_type = config['led_panel_type']

        self.matrix = RGBMatrix(options=options)
        
    def display(self, img):
        img = Image.fromarray(img).convert('RGB')
        self.matrix.SetImage(img)
    

class PILDisplay():

    def __init__(self, config):
        pass
        
    def display(self, img):
        img = Image.fromarray(img).convert('RGB')
        img.show()
    


