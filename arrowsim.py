
import sys
sys.path.append("gl")

import numpy as np
from PIL import Image
from OpenGL.GL import *
from libegl import EGLContext

class ArrowSim():

    def __init__(self, config):
        self.h,self.w = config.getint('rows'), config.getint('cols')
        ctx = EGLContext()
        if not ctx.initialize(self.w, self.h):
            raise ValueError("Couldn't initialize OpenGL context")
        
    def render(self):
        img_buf = glReadPixels(0, 0, self.w, self.h, GL_RGB, GL_UNSIGNED_BYTE)
        return Image.frombytes('RGB', (self.w, self.h), img_buf)
        
    def step(self, deltatime, data):
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(0, 0, 1.0)
        x1, x2 = -0.9, 0.3
        y1, y2 = -0.5, 0.7
        glRectf(x1, y1, x2, y2)
        
        
        
        