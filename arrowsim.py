
import sys
sys.path.append("gl")

import numpy as np
from PIL import Image

from OpenGL.GL import *
from OpenGL.GLU import *
from libegl import EGLContext


class ArrowSim():

    def __init__(self, config):
        self.h,self.w = config.getint('rows'), config.getint('cols')
        ctx = EGLContext()
        if not ctx.initialize(self.w, self.h):
            raise ValueError("Couldn't initialize OpenGL context")

        self.scale = config.getfloat('scale')
        self.slices = config.getint('slices')
        self.stacks = config.getint('stacks')
        if config['draw_style'] == 'GLU_FILL':
            self.draw_style = GLU_FILL
        elif config['draw_style'] == 'GLU_LINE':
            self.draw_style = GLU_LINE
        elif config['draw_style'] == 'GLU_SILHOUETTE':
            self.draw_style = GLU_SILHOUETTE
        elif config['draw_style'] == 'GLU_POINT':
            self.draw_style = GLU_POINT
        else:
            print('Unknown GLU draw style %s, using GLU_FILL instead' % config['draw_style'])
            self.draw_style = GLU_FILL
        
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, 1.0, 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        glMatrixMode(GL_MODELVIEW)
        
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glColor3f(0.0, 1.0, 0.9)
        glTranslatef(-0.2, 0.0, 0.)
        glScalef(self.scale, self.scale, self.scale)

        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, self.draw_style)

        glRotatef(90.0, 0.0, 1.0, 0.0)
        gluCylinder(quadric, 0.8, 0.0, 1.5, self.slices, self.stacks)
        gluDisk(quadric, 0.0, 0.8, self.slices, self.stacks)
        glTranslatef(0.0, 0.0, -0.8)
        gluCylinder(quadric, 0.4, 0.4, 0.8, self.slices, self.stacks)

        gluDeleteQuadric(quadric)

        img_buf = glReadPixels(0, 0, self.w, self.h, GL_RGB, GL_UNSIGNED_BYTE)
        return Image.frombytes('RGB', (self.w, self.h), img_buf)
        
    def step(self, deltatime, data):
        glLoadIdentity()
        glRotatef(data['fusionPose'][0], 1, 0, 0)
        glRotatef(data['fusionPose'][1], 0, 1, 0)
        glRotatef(-data['fusionPose'][2], 0, 0, 1)

        
        
        
        