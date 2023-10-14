import pygame
import math

def draw_sin(amplitude: int, frequency: float, offset: int) -> int:
    if frequency < 1:
        t = pygame.time.get_ticks() % (1000/frequency)
    else:
        t = pygame.time.get_ticks() % 1000
    
    y = amplitude*math.sin((2*math.pi*frequency*t)/1000) + offset 
    return int(y)

def draw_bounce(amplitude: int, frequency: float, offset: int)->int:
    if frequency < 1:
        t = pygame.time.get_ticks() % (1000/frequency)
    else:
        t = pygame.time.get_ticks() % 1000
    
    y = -abs(amplitude*math.sin((2*math.pi*frequency*t)/1000)) + offset 
    return int(y)
