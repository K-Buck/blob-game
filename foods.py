# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 23:41:17 2019

@author: pi
"""

import random

class Food:
    
    def __init__(self, x_max, y_max):
        
        size_range=(2,4)
        
        self.size = random.randrange(size_range[0],size_range[1])
        self.color = (0, 255, 0)
        
        self.x = random.randrange(0, x_max)
        self.y = random.randrange(0, y_max)
