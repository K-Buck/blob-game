# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:15:47 2020

@author: Kevin
"""

from BlobGame import BlobGameEnv
from blobs import Blob

if __name__ == '__main__':
    
    x_max = 1000
    y_max = 1000
    num_entities = 20
    num_food = 50
    
    env = BlobGameEnv(x_max, y_max)
    env.reset()
    
    for i in range(num_entities):
        entity = Blob(x_max, y_max)
        env.entities.append(entity)
    
    env.start_game(render=True)