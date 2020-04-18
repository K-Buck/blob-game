# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 23:10:37 2020

@author: Kevin
"""

from matplotlib import pyplot as plt

class Overview():
    
    def __init__(self, env):
        
        self.env = env
        self.create_display()
        
    # Create display
    def create_display(self):
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.perimeter = plt.Rectangle((0,0), self.env.x_max, self.env.y_max,
                                       linewidth=1,edgecolor='r',facecolor='none')
        self.ax.add_patch(self.perimeter)
        self.ax.axis('equal')
        
        for entity in self.env.entities:
            entity.register_display(self.ax)
        
        for food in self.env.food:
            food.register_display(self.ax)
            
    def update_display(self):
        
        for entity in self.env.entities:
            entity.update_display()
        
        for food in self.env.food:
            food.update_display()
            
        plt.draw()
        plt.pause(0.00001)
        
    # Initialize entity in figure
    def register_entity(self, entity):
        pass
    
    # Close figure and child graphics objects
    def close(self):
        self.destroy_displays()
    
    # Loop through entities and destroy graphics objects
    def destroy_displays(self):
        pass
    
if __name__ == '__main__':
    
    from BlobGame import BlobGameEnv
    
    ov = Overview(BlobGameEnv())