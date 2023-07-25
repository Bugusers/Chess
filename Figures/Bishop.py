import pygame as pg
from Figures.Figure import Figure

class Bishop(Figure): 
    def __init__(self, color, cell):
        super().__init__(color, cell)
        self.name = "BISHOP"
        self.image = pg.image.load("assets/blackBishop.png") if self.color == (0, 0, 0) else pg.image.load("assets/whiteBishop.png")

    def can_move(self, target):
        if not super().can_move(target):
            return False    
        
        if self.cell.is_empty_diagonal(target):
            return True
        
        return False   

    def can_attack(self, target):
        if self.can_move(target):
            return True
            
        return False
    


    
