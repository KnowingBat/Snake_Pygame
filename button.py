import pygame 
from pygame import Vector2, Rect, Color

class Button:
    def __init__(self, rect: Rect, color: Color):
        self.rect = rect
        self.color = color

    def draw_button(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
    
    def onclick(self, fun):
        fun()

    #def on_hover(self):
        #Do something on hover