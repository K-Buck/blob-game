# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 23:33:04 2019

@author: pi
"""

import random
from foods import Food
import logging
import numpy as np

class Blob:

    def __init__(self, x_max, y_max, col=None):
        
        if col is None:
            col = (random.randrange(0, 256),
                   random.randrange(0, 256),
                   random.randrange(0, 256))
            
        sizeRange = (5,8)
        
        self.x_max = x_max
        self.y_max = y_max

        self.size = random.randrange(sizeRange[0],sizeRange[1])
        
        self.color = col
        
        self.x = random.randrange(0, self.x_max)
        self.y = random.randrange(0, self.y_max)
        
        self.dx = 0
        self.dy = 0
        
        self.ux = 0
        self.uy = 0
        
    @property
    def speed(self):
        return (self.dx*self.dx + self.dy*self.dy)**0.5
        
    def setRandomMove(self):
        
        self.ux = random.randrange(-1, 2)
        self.uy = random.randrange(-1, 2)
    
    def step(self, env):
            
        self.dx += self.ux
        self.dy += self.uy
        
        self.dx = np.clip(self.dx,-5,5)
        self.dy = np.clip(self.dy,-5,5)
        
        self.x += self.dx
        self.y += self.dy

        if self.x < 0:
            self.x = 0
            self.dx = -self.dx
        elif self.x > self.x_max:
            self.x = self.x_max
            self.dx = -self.dx
        
        if self.y < 0:
            self.y = 0
            self.dy = -self.dy
        elif self.y > self.y_max:
            self.y = self.y_max
            self.dy = -self.dy

    def is_touching(self, obj2):

        slantRange = np.linalg.norm(np.array([self.x, self.y])-np.array([obj2.x, obj2.y]))
        Radii = (self.size + obj2.size)
        
        return slantRange < Radii

    def __add__(self, other_obj):
        
        logging.info('Blob add op {} + {}'.format(str(self.color), str(other_obj.color)))
        logging.info('Blob add op {} + {}'.format(str(self.size), str(other_obj.size)))
                
        if isinstance(other_obj,Food):
            self.size = np.sqrt(self.size**2 + other_obj.size**2)
            other_obj.size = 0
            
        elif self.size > other_obj.size:
            self.size = np.sqrt(self.size**2 + other_obj.size**2)
            other_obj.size = 0
            
        elif self.size < other_obj.size:
            other_obj.size = np.sqrt(self.size**2 + other_obj.size**2)
            self.size = 0
