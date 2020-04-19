# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 23:41:17 2019

@author: pi
"""

import random
from matplotlib import pyplot as plt

class Food:
    
    def __init__(self, x_max, y_max):
        
        size_range=(2,4)
        
        self.size = random.randrange(size_range[0],size_range[1])
        self.color = (0, 1, 0)
        
        self.x = random.randrange(0, x_max)
        self.y = random.randrange(0, y_max)
        
        self.circle = None
        
    def register_display(self, ax):
        self.circle = plt.Circle((self.x,self.y), self.size, facecolor=self.color)
        ax.add_patch(self.circle)
        
    def update_display(self):
        self.circle.set_center((self.x,self.y))
        
    def destroy_display(self):
        if self.circle is not None:
            self.circle.remove()
            self.circle = None