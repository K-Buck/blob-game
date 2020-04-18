# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 17:29:24 2020

@author: kevin
"""

import numpy as np
from Displays import Overview
from foods import Food

class BlobGameEnv():
    
    
    def __init__(self, x_max=400, y_max=400):
        
        self.x_max = x_max
        self.y_max = y_max
        
        self.entities = []
        
        self.n_food = 30
        self.foods = []
        
        self.count = 0
        self.viewer = None
        
    def start_game(self, render=False):
                
        if render:
            print('Rendering')
            self.viewer = Overview(self)
                
        while len(self.entities) > 1:
            
            for entity in self.entities:
                entity.step(self)    
                
            self.handle_collisions()
            
            self.grow_food()
            
            self.count += 1
            
            if render:
                self.viewer.update_display()
            
        self.close()
               
    def handle_collisions(self):
        
        dead_entities = []
        for entity in self.entities:
            
            if entity in dead_entities:
                continue
            
            for other_entity in self.entities:
                
                if other_entity in dead_entities:
                    continue
                
                if np.array_equal(entity.color, other_entity.color):
                    continue
                
                if entity.is_touching(other_entity):
                    entity + other_entity
                    if other_entity.size <= 0:
                        other_entity.destroy_display()
                        dead_entities.append(other_entity)
                    elif entity.size <= 0:
                        entity.destroy_display()
                        dead_entities.append(entity)
                        break

        [self.entities.remove(entity) for entity in dead_entities]
        
        eaten_foods = []
        for entity in self.entities:
            for food in self.foods:
                if entity.is_touching(food):
                    entity + food
                    food.destroy_display()
                    eaten_foods.append(food)
                    
        [self.foods.remove(food) for food in eaten_foods]
        
    def grow_food(self):
        
        if len(self.foods) < self.n_food:
            for n in range(self.n_food - len(self.foods)):
                
                new_food = Food(self.x_max, self.y_max)
                new_food.register_display(self.viewer.ax)
                self.foods.append(new_food)
    
    def reset(self):
        self.entities = []
        self.count = 0
        
        if self.viewer is not None:
            self.close()
    
    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None