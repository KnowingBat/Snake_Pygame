import pygame
from pygame import Rect
from button import Button

class MainMenu:
    def __init__(self):
        rect = Rect(0,0,50,50)
        self.x = 1
        self.button = Button(rect, (0,0,0))