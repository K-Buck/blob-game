# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 17:29:24 2020

@author: kevin
"""

from Displays import Overview
from foods import Food

class BlobGameEnv():
    
    
    def __init__(self, x_max=400, y_max=400):
        
        self.x_max = x_max
        self.y_max = y_max
        
        self.entities = []
        
        self.n_food = 30
        self.food = []
        
        self.count = 0
        self.viewer = None
        
    def start_game(self, render=False):
                
        if render:
            print('Rendering')
            self.viewer = Overview(self)
                
        while len(self.entities) > 1:
            
            for entity in self.entities:
                entity.step(self)    
                
            self.grow_food()
            
            self.count += 1
            
        self.close()
                        
    def grow_food(self):
        
        if len(self.food) < self.n_food:
            for n in range(self.n_food - len(self.food)):
                self.food.append(Food, self.x_max, self.y_max)
    
    def reset(self):
        self.entities = []
        self.count = 0
        
        if self.viewer is not None:
            self.close()
    
    def render(self, mode='human'):
        pass
    
    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None