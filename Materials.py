# -*- coding: utf-8 -*-

from abc import ABC

class Material(ABC):
    
    def __init__(self):
        
        self.density = 1
        

class Slime(Material):
    
    def __init__(self):
        
        super().__init__()
        self.density = 0.05