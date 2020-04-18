# -*- coding: utf-8 -*-
import sys
import pygame
import numpy as np
import Environments
from blobs import Blob
from foods import Food

import logging

class blobApp():
    
    def __init__(self):
        
        self.NUM_STARTING_BLOBS = 30
        self.NUM_STARTING_FOODS = 50
        self.env = Environments.Ground()
        
        self.FPS = 30
        self.WIDTH = 800
        self.HEIGHT = 600
        self.WHITE = (255, 255, 255)
            
        pygame.init()
        self.game_display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Blob World")
        self.game_clock = pygame.time.Clock()

    def runGame(self):
        
        # Initialize the blobs and food
        self.initialize_game()
        
        # While more than 1 blob is still alive loop through game steps
        while len(self.blobs) > 1:
            
            # Check for user inputs (escape, up, down, left, right)
            self.process_input_events()
        
            # Move all of the blobs
            self.moveBlobs()
            
            # Check if any blobs collided and handle the collision
            self.handle_collisions()
            
            if 'player1' not in self.blobs.keys():
                print('Player 1 Died')
                self.terminate()
                
            # Generate more food if necessary
            self.generate_food()        
            
            # Redraw all of the food and blobs
            self.draw_environment()
            
            # Limits frame rate to specified FPS
            self.game_clock.tick(self.FPS)
            
        # 1 Blob remains
        self.terminate()
        
    def initialize_game(self):
        
        color = {'RED'   : (255,   0,   0),
                 'BLUE'  : (  0,   0, 255),
                 'BLACK' : (  0,   0,   0),
                 'TEAL'  : (  0, 255, 255)}
        
        self.blobs = dict(enumerate([Blob(self.WIDTH, self.HEIGHT) for i in range(self.NUM_STARTING_BLOBS)]))
        self.foods = dict(enumerate([Food(self.WIDTH, self.HEIGHT) for i in range(self.NUM_STARTING_FOODS)]))
        
        self.blobs['player1'] = Blob(self.WIDTH, self.HEIGHT, color['BLACK'])
        self.blobs['player1'].size = 7
        
    def process_input_events(self):
        
        for event in pygame.event.get(): # event handling loop
            if event.type == pygame.QUIT:
                self.terminate()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    logging.info('Player 1 up')
                    self.blobs['player1'].uy = -1
                elif event.key == pygame.K_DOWN:
                    logging.info('Player 1 down')
                    self.blobs['player1'].uy = 1
                elif event.key == pygame.K_LEFT:
                    logging.info('Player 1 left')
                    self.blobs['player1'].ux = -1
                elif event.key == pygame.K_RIGHT:
                    logging.info('Player 1 right')
                    self.blobs['player1'].ux = 1

            elif event.type == pygame.KEYUP:
                # stop moving the player's blob
                if event.key == pygame.K_UP:
                    self.blobs['player1'].uy = 0
                elif event.key == pygame.K_DOWN:
                    self.blobs['player1'].uy = 0
                elif event.key == pygame.K_LEFT:
                    self.blobs['player1'].ux = 0
                elif event.key == pygame.K_RIGHT:
                    self.blobs['player1'].ux = 0
                elif event.key == pygame.K_ESCAPE:
                    self.terminate()
        
    def moveBlobs(self):
        
        for blob_id in self.blobs:
            
            if blob_id == 'player1':
                self.blobs['player1'].move()
            else:
                self.blobs[blob_id].setRandomMove()
                self.blobs[blob_id].move()            
            
    def handle_collisions(self):
            
        dead_blobs = []
        for blob_id, blob in self.blobs.items():
            
            if blob_id in dead_blobs:
                continue
            
            for other_id, other_blob in self.blobs.items():
                
                if other_id in dead_blobs:
                    continue
                
                if blob.color == other_blob.color:
                    continue
                
                if blob.is_touching(other_blob):
                    blob + other_blob
                    if other_blob.size <= 0:
                        logging.debug('Other blob eaten')
                        #del self.blobs[other_id]
                        dead_blobs.append(other_id)
                    elif blob.size <= 0:
                        logging.debug('This blob eaten')
                        #del self.blobs[blob_id]
                        dead_blobs.append(blob_id)
                        break

        [self.blobs.pop(key) for key in dead_blobs]
        
        for blob_id, blob in self.blobs.copy().items():
            for food_id, food in self.foods.copy().items():
                if blob.is_touching(food):
                    blob + food
                    del self.foods[food_id]
                    logging.debug('Blob {} ate Food {}'.format(blob.color,food_id))

    def generate_food(self):

        num_remaining_food = len(self.foods)
        if num_remaining_food < (self.NUM_STARTING_FOODS * 0.5):
            self.foods = dict(enumerate([Food(self.WIDTH,self.HEIGHT) for i in range(self.NUM_STARTING_FOODS)]))
    
    def draw_environment(self):

        self.game_display.fill(self.WHITE)

        for blob_id in self.blobs:
            blob = self.blobs[blob_id]
            pygame.draw.circle(self.game_display, blob.color, (int(blob.x), int(blob.y)), int(np.floor(blob.size)))
            
        for food_id in self.foods:
            food = self.foods[food_id]
            pygame.draw.circle(self.game_display, food.color, [food.x, food.y], food.size)

        pygame.display.update()
        
    def terminate(self):
        
        pygame.quit()
        sys.exit()
        
if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG)
    
    myApp = blobApp()
    myApp.runGame()
