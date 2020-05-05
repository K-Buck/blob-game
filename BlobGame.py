# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 17:29:24 2020

@author: kevin
"""

import numpy as np
from Displays import Overview
import blobs
from foods import Food
import logging

class BlobGameEnv():
    
    
    def __init__(self, x_max=400, y_max=400):
        
        self.x_max = x_max
        self.y_max = y_max
        
        self.entities = []
        
        self.n_food = 30
        self.foods = []
        
        self.count = 0
        self.viewer = None
        
    def start_game(self, render=False, max_frames=2000):
                
        self.grow_food()
        
        if render:
            logging.info('Rendering')
            self.viewer = Overview(self)
        
        while len(self.entities) > 1 :
            
            # Step 1: All entities get an opportunity to take an action
            for entity in self.entities:
                entity.step(self)    
                
            # Step 2: Adjudicate collisions between blobs/blobs and blobs/food
            self.handle_collisions()
     
            # FIXME
            # I dont like this implementation
            # Post process the smart blobs for memory and training
            alive = 0
            for entity in self.entities:
                if isinstance(entity, blobs.smart_blob):
                    entity.post_step(self)
                    alive +=1
            
            # If no more smart blobs are alive, break
            if alive == 0:
                break
            
            # Step 3: Grow food
            self.grow_food()
            
            # Break if max frames played
            self.count += 1
            if self.count > max_frames:
                break
            
            # Update display
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
                        other_entity.kill_entity(self)
                        dead_entities.append(other_entity)
                    elif entity.size <= 0:
                        entity.kill_entity(self)
                        dead_entities.append(entity)
                        break

        [self.entities.remove(entity) for entity in dead_entities]
        
        eaten_foods = []
        for entity in self.entities:
            for food in self.foods:
                
                if food in eaten_foods:
                    continue
                
                if entity.is_touching(food):
                    entity + food
                    food.destroy_display()
                    eaten_foods.append(food)
                    
        [self.foods.remove(food) for food in eaten_foods]
        
    def grow_food(self):
        
        if len(self.foods) < self.n_food:
            for n in range(self.n_food - len(self.foods)):
                
                new_food = Food(self.x_max, self.y_max)
                if self.viewer is not None:
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