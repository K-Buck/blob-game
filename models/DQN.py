# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 23:23:50 2020

@author: Kevin
"""

import gym
from keras.layers import Dense
from keras import Sequential
from keras.optimizers import Adam

import numpy as np
from collections import deque
import random
import logging

# Agent class
class DQNAgent(object):
    
    def __init__(self,
                 observation_space,
                 action_space,
                 lr=0.001,
                 epsilon=1.0,
                 epsilon_decay=1-1e-5,
                 epsilon_min=0.01,
                 gamma=0.99):
        
        self.DISCOUNT = gamma
        self.REPLAY_MEMORY_SIZE = 1_000_000  # How many last steps to keep for model training
        self.MIN_REPLAY_MEMORY_SIZE = 1_000  # Minimum number of steps in a memory to start training
        self.MINIBATCH_SIZE = 256  # How many steps (samples) to use for training
        self.UPDATE_TARGET_EVERY = 2  # Terminal states (end of episodes)
        self.hidden_dims = 128
        self.lr = lr
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
        self.observation_space = observation_space
        self.n_obs = observation_space.shape[0]
        
        self.action_space = action_space
        if type(action_space) is gym.spaces.Discrete:
            self.n_act = action_space.n
        else:
            self.n_act = action_space.shape[0]

        # Main model
        self.model = self.create_model()
        
        # Target network
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        # An array with last n steps for training
        self.replay_memory = deque(maxlen=self.REPLAY_MEMORY_SIZE)

        # Used to count when to update target network with main network's weights
        self.target_update_counter = 0

    def decay_exploration(self):
              
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            self.epsilon = max(self.epsilon_min,self.epsilon)
        
    def choose_action(self, observation):
        
        
        if np.random.random() > self.epsilon:
            observation = np.reshape(observation,[1,self.n_obs])
            q_values = self.model.predict(observation)
            action = np.argmax(q_values)
        else:
            action = self.action_space.sample()
            
        self.decay_exploration()
        
        return action
        
    def create_model(self):
            
        model = Sequential()
        
        model.add(Dense(self.hidden_dims, input_shape=(self.n_obs,), activation='relu'))
        model.add(Dense(self.hidden_dims, activation='relu'))
        model.add(Dense(self.n_act, activation='linear'))

        model.compile(loss="mse", optimizer=Adam(lr=self.lr), metrics=['accuracy'])
        
        return model

    # Adds step's data to a memory replay array
    # (observation space, action, reward, new observation space, done)
    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    # Trains main network every step during episode
    def train(self, terminal_state):

        # Start training only if certain number of samples is already saved
        if len(self.replay_memory) < self.MIN_REPLAY_MEMORY_SIZE:
            return

        # Get a minibatch of random samples from memory replay table
        minibatch = random.sample(self.replay_memory, self.MINIBATCH_SIZE)

        # Get current states from minibatch, then query NN model for Q values
        current_states = np.array([i[0] for i in minibatch])
        current_qs_list = self.model.predict(current_states)

        # Get future states from minibatch, then query NN model for Q values
        # When using target network, query it, otherwise main network should be queried
        new_current_states = np.array([transition[3] for transition in minibatch])
        future_qs_list = self.target_model.predict(new_current_states)

        X = []
        y = []

        # Now we need to enumerate our batches
        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):

            # If not a terminal state, get new q from future states, otherwise set it to 0
            # almost like with Q Learning, but we use just part of equation here
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + self.DISCOUNT * max_future_q
            else:
                new_q = reward
            
            # Update Q value for given state
            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            # And append to our training data
            X.append(current_state)
            y.append(current_qs)

        # Fit on all samples as one batch, log only on terminal state
        self.model.fit(np.array(X), np.array(y), batch_size=self.MINIBATCH_SIZE, verbose=0, shuffle=False)

        # Update target network counter every episode
        if terminal_state:
            self.target_update_counter += 1

        # If counter reaches set value, update target network with weights of main network
        if self.target_update_counter > self.UPDATE_TARGET_EVERY:
            logging.info('Updating weights')
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0
