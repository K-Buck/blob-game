# -*- coding: utf-8 -*-

from abc import ABC

class Environment(ABC):
    
    def __init__(self):
        
        self.coefStaticFriction = 1
        self.coefDynamicFriction = 1
        self.gravity = 9.81

class Ground(Environment):
    
    def __init__(self):
        
        super().__init__()
        self.coefStaticFriction = 2
        self.coefDynamicFriction = .5