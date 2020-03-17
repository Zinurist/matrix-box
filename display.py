
from PIL import Image

class RGBMatrixDisplay():

    def __init__(self, size):
        if len(size) != 2:
            raise ValueError('Invalid size, display has to be 2D')
    
        from rgbmatrix import RGBMatrix, RGBMatrixOptions
        options = RGBMatrixOptions()
        options.rows = size[0]
        options.cols = size[1]
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat-pwm'
        
        self.matrix = RGBMatrix(options=options)
        
    def display(self, img):
        img = Image.fromarray(img).convert('RGB')
        self.matrix.SetImage(img)
    

class PILDisplay():

    def __init__(self, size):
        pass
        
    def display(self, img):
        img = Image.fromarray(img).convert('RGB')
        img.show()
    


