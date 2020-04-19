# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 23:33:04 2019

@author: pi
"""

from gym import spaces

import math
import random
import logging
import numpy as np
from matplotlib import pyplot as plt

from foods import Food
from models.DQN import DQNAgent

class Blob:

    def __init__(self, x_max, y_max, col=None):
        
        if col is None:
            # Generate random RGB color with min value of 0.1
            col = np.random.uniform(0.1,0.9,(1,3))[0]
            
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
        
        self.circle = None
        
    @property
    def speed(self):
        return (self.dx*self.dx + self.dy*self.dy)**0.5
        
    def setRandomMove(self):
        
        self.ux = random.randrange(-1, 2)
        self.uy = random.randrange(-1, 2)
    
    def move(self):
        
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
            
    def step(self, env):
        
        self.setRandomMove()
        self.move()

    def is_touching(self, obj2):

        slantRange = np.linalg.norm(np.array([self.x, self.y])-np.array([obj2.x, obj2.y]))
        Radii = (self.size + obj2.size)
        
        return slantRange < Radii

    def __add__(self, other_obj):
        
        logging.debug('Blob add op {} + {}'.format(str(self.color), str(other_obj.color)))
        logging.debug('Blob add op {} + {}'.format(str(self.size), str(other_obj.size)))
                
        if isinstance(other_obj,Food):
            self.size = np.sqrt(self.size**2 + other_obj.size**2)
            other_obj.size = 0
            
        elif self.size > other_obj.size:
            self.size = np.sqrt(self.size**2 + other_obj.size**2)
            other_obj.size = 0
            
        elif self.size < other_obj.size:
            other_obj.size = np.sqrt(self.size**2 + other_obj.size**2)
            self.size = 0
    
    def kill_entity(self, env):
        self.destroy_display()
        
    def register_display(self, ax):
        self.circle = plt.Circle((self.x,self.y), self.size, facecolor=self.color)
        ax.add_patch(self.circle)
        
    def update_display(self):
        self.circle.set_radius(self.size)
        self.circle.set_center((self.x,self.y))
        
    def destroy_display(self):
        if self.circle is not None:
            self.circle.remove()
            self.circle = None
        
class smart_blob(Blob):
    
    def __init__(self, x_max, y_max, col=None):
        
        super().__init__(x_max, y_max, col)
        
        # Observation space:
            # Size of self [units]
            # Angle to nearest entity [rad]
            # Range to nearest entity [units]
            # Size of nearest entity [units]
            # Angle to nearest food [rad]
            # Range to nearest food [units]
            
        high = np.array([np.finfo(np.float32).max,
                         math.pi,
                         np.finfo(np.float32).max,
                         np.finfo(np.float32).max,
                         math.pi,
                         np.finfo(np.float32).max],
                        dtype=np.float32)
        
        low = np.array([0.0,
                         -math.pi,
                         0.0,
                         0.0,
                         -math.pi,
                         0.0],
                        dtype=np.float32)
        
        observation_space = spaces.Box(low, high, dtype=np.float32)
        action_space = spaces.Discrete(4)
        
        self.agent = DQNAgent(observation_space, action_space)
        
        self.actions = {0:( 0, 1), # Up
                        1:( 0,-1), # Down
                        2:(-1, 0), # Left
                        3:( 1, 0), # Right
                        }
        
        self.total_reward = 0
        self.prev_size = self.size
        
    def reset(self):
        
        sizeRange = (5,8)

        self.size = random.randrange(sizeRange[0],sizeRange[1])
        self.prev_size = self.size
        
        self.x = random.randrange(0, self.x_max)
        self.y = random.randrange(0, self.y_max)
        
        self.dx = 0
        self.dy = 0
        
        self.ux = 0
        self.uy = 0
        
        self.circle = None
        
        self.total_reward = 0
        
    def step(self, env):
        
        # Generate sensor observation from current environment
        self.observation = self.get_observation(env)
        
        # Generate an action from the Agent based on the observation
        self.action = self.agent.choose_action(self.observation)
        
        # Set the entity control signal (ux,uy)
        self.set_action(self.action)
        
        # Move the Entity based on the control signal
        self.move()
        
        self.prev_size = self.size
        
    def post_step(self, env):
                
        # Set done to False for now, object destruction with assign this to True
        done = False
        
        # Calculate the reward based on the environment
        reward = self.calculate_reward(env)
        self.total_reward += reward
        
        new_observation = self.get_observation(env)
        
        # Store the states
        self.agent.update_replay_memory((self.observation, self.action, reward, new_observation, done))
        
        # Train the agent
        self.agent.train(terminal_state=False)
        
    def get_observation(self, env):
        
        observation = np.zeros((6,),dtype=np.float32)
        observation[0] = self.size
        
        # Get nearest entity
        def distance(entity1, entity2):
            return np.linalg.norm(np.array([entity2.x, entity2.y])-np.array([entity1.x, entity1.y]))
            
        range_entity = 1e6
        closest_entity = self
        for entity in env.entities:
            if entity == self:
                continue
            
            temp = distance(self, entity)
            if temp < range_entity:
                range_entity = temp
                closest_entity = entity
                
        range_food = 1e6
        for food in env.foods:
            temp = distance(self, food)
            if temp < range_food:
                range_food = temp
                closest_food = food
        
        az_entity = math.atan2(closest_entity.y - self.y, closest_entity.x - self.x)
        az_food = math.atan2(closest_food.y - self.y, closest_food.x - self.x)
                
        observation[1] = az_entity
        observation[2] = range_entity
        observation[3] = closest_entity.size
        observation[4] = az_food
        observation[5] = range_food
        
        return observation
    
    def set_action(self, action):
        direction = self.actions[action]
        self.ux = direction[0]
        self.uy = direction[1]
    
    def calculate_reward(self, env):
        
        if self.size == self.prev_size:
            reward = -0.5
        elif self.size > self.prev_size:
            reward = (self.size - self.prev_size)*20
            #reward = 10
        else:
            reward = -10
                
        return reward
    
    def kill_entity(self, env):
        logging.info("agent died")
        self.destroy_display()
        
        self.post_step(env)
        
        # Change last memory to a terminal state and retrain
        last_memory = self.agent.replay_memory.pop()
        observation, action, reward, new_observation, done = last_memory
        reward = -10
        done = True
        self.agent.update_replay_memory((observation, action, reward, new_observation, done))
        self.agent.train(terminal_state=True)
        