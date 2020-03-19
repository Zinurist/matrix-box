
import sys
sys.path.append("gl")

import numpy as np
from PIL import Image

from OpenGL.GL import *
from OpenGL.GLU import *
from libegl import EGLContext


class CubeSim():

    def __init__(self, config):
        self.h,self.w = config.getint('rows'), config.getint('cols')
        ctx = EGLContext()
        if not ctx.initialize(self.w, self.h):
            raise ValueError("Couldn't initialize OpenGL context")
        
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, 1.0, 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        glMatrixMode(GL_MODELVIEW)

        self.rotate = config.getboolean('rotate')
        
    def render(self):
        #Taken from https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        vertices= (
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1),
        )

        edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7),
        )

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

        img_buf = glReadPixels(0, 0, self.w, self.h, GL_RGB, GL_UNSIGNED_BYTE)
        return Image.frombytes('RGB', (self.w, self.h), img_buf)
        
    def step(self, deltatime, data):
        if self.rotate:
            #glRotatef(deltatime*70.0, 3, 1, 1)
            glRotatef(deltatime*70.0, 3, 1, 1)
        else:
            glLoadIdentity()
            glRotatef(data['fusionPose'][0], 1, 0, 0)
            glRotatef(data['fusionPose'][1], 0, 1, 0)
            glRotatef(-data['fusionPose'][2], 0, 0, 1)

        
        