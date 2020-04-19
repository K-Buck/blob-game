# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:15:47 2020

@author: Kevin
"""

from BlobGame import BlobGameEnv
from blobs import Blob
from blobs import smart_blob
import numpy as np
import logging
import pickle

if __name__ == '__main__':
    
    logging.getLogger().setLevel(logging.INFO)
    
    filename = 'smart_entity_v0.pickle'
        
    x_max = 400
    y_max = 400
    num_entities = 3
    num_food = 50
    episodes = 1000
    
    env = BlobGameEnv(x_max, y_max)
    
    black = (0,0,0)
    try:
        with open(filename,'rb') as f:
            logging.info("Loading Agent {}".format(filename))
            agent = pickle.load(f)
    except:
        logging.info("Failed to reload agent, creating new one")
        agent = smart_blob(x_max, y_max, col=black)
    
    win_history= []
    for episode in range(episodes):
                
        render = False
        if episode % 10 == 0:
            render = True
            
        env.reset()
        agent.reset()
        
        for i in range(num_entities):
            entity = Blob(x_max, y_max)
            env.entities.append(entity)
        
        env.entities.append(agent)
            
        env.start_game(render=render)
        
        agent.agent.train(terminal_state=True)
        
        logging.info('Episode {}'.format(episode))
        logging.info('Exploration {}'.format(agent.agent.epsilon))
        
        if agent in env.entities and len(env.entities) == 1:
            logging.info("WIN")
            win_history.append(1)
        else:
            logging.info("LOSE")
            win_history.append(0)
            
        logging.info("Win Rate: {}".format(np.mean(win_history[-100:])))
        logging.info("Final Size: {}".format(agent.size))
        logging.info("Total Reward: {}".format(agent.total_reward))
        
        if episode % 10 == 0:
            logging.info("Saving Agent")
            with open(filename,'wb') as f:
                pickle.dump(agent, f)