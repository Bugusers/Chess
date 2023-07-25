import pygame as pg
from abc import ABC, abstractmethod

class Figure(ABC):
    def __init__(self, color, cell):
        self.image = None
        self.name = None

        self.color = color
        self.cell = cell


    def draw(self, screen, x, y, size):
        resized_image = pg.transform.scale(self.image, (size - 16, size - 16))
        screen.blit(resized_image, (x + 8, y + 8)) 
    

    def move(self, target):
        self.cell = target


    def can_move(self, target):
        if target.figure and target.figure.color == self.color:
            return False
        # if target.figure and target.figure.name == "KING":
        #     return False
        
        return True
    
    @abstractmethod
    def can_attack(self, target):
        pass
