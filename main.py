# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:15:47 2020

@author: Kevin
"""

from BlobGame import BlobGameEnv
from blobs import Blob

if __name__ == '__main__':
    
    x_max = 400
    y_max = 400
    num_entities = 10
    num_food = 20
    
    env = BlobGameEnv(x_max, y_max)
    env.reset()
    
    entity = Blob(x_max, y_max)
    env.entities.append(entity)
    
    env.start_game(render=True)