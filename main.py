import pygame
import random
from pygame import Vector2, Rect, Color, Surface
from button import Button
from menu import MainMenu
import os

class Snake:
    def __init__(self):
        self.body = [Vector2(7,6), Vector2(6,6), Vector2(5,6)]
        self.color = SNAKE_COLOR
        self.direction = Vector2(1,0) #To the right
        self.new_block = False

        self.tail_up = pygame.image.load(os.path.join(IMGDIR, 'tail_up.png'))
        self.tail_down = pygame.image.load(os.path.join(IMGDIR, 'tail_down.png'))
        self.tail_left = pygame.image.load(os.path.join(IMGDIR, 'tail_left.png'))
        self.tail_right = pygame.image.load(os.path.join(IMGDIR, 'tail_right.png'))

        self.head_up = pygame.image.load(os.path.join(IMGDIR, 'head_up.png'))
        self.head_down = pygame.image.load(os.path.join(IMGDIR, 'head_down.png'))
        self.head_left = pygame.image.load(os.path.join(IMGDIR, 'head_left.png'))
        self.head_right = pygame.image.load(os.path.join(IMGDIR, 'head_right.png'))

        self.body_bottomleft = pygame.image.load(os.path.join(IMGDIR, 'body_bottomleft.png'))
        self.body_bottomright = pygame.image.load(os.path.join(IMGDIR, 'body_bottomright.png'))
        self.body_horizontal = pygame.image.load(os.path.join(IMGDIR, 'body_horizontal.png'))
        self.body_topleft = pygame.image.load(os.path.join(IMGDIR, 'body_topleft.png'))
        self.body_topright = pygame.image.load(os.path.join(IMGDIR, 'body_topright.png'))
        self.body_vertical = pygame.image.load(os.path.join(IMGDIR, 'body_vertical.png'))

    def draw_snake(self):
        sz = len(self.body) 
        for index, block in enumerate(self.body):
            block_rect = Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            if index == 0: # If head
                self.draw_head(block_rect)
            elif index < (sz - 1):
                
                if (self.body[index - 1] - block) == Vector2(1,0) \
                        or (self.body[index - 1] - block) == Vector2(-1,0):
                    surface = self.body_horizontal
                elif (self.body[index - 1] - block) == Vector2(0,1) \
                        or (self.body[index - 1] - block) == Vector2(0,-1):
                    surface = self.body_vertical

                if ((self.body[index - 1] - self.body[index + 1]) == Vector2(1,1) \
                            and (self.body[index - 1] - block) == Vector2(0,1)) \
                        or ((self.body[index - 1] - self.body[index + 1]) == Vector2(-1,-1) \
                            and (self.body[index - 1] - block) == Vector2(-1,0)):
                    surface = self.body_bottomleft
                    
                elif ((self.body[index - 1] - self.body[index + 1]) == Vector2(1,-1) \
                            and (self.body[index - 1] - block) == Vector2(1,0)) \
                        or ((self.body[index - 1] - self.body[index + 1]) == Vector2(-1,1) \
                            and (self.body[index - 1] - block) == Vector2(0,1)):
                    surface = self.body_bottomright

                elif ((self.body[index - 1] - self.body[index + 1]) == Vector2(-1,-1) \
                            and (self.body[index - 1] - block) == Vector2(0,-1)) \
                        or ((self.body[index - 1] - self.body[index + 1]) == Vector2(1,1) \
                            and (self.body[index - 1] - block) == Vector2(1,0)):
                    surface = self.body_topright

                elif ((self.body[index - 1] - self.body[index + 1]) == Vector2(1,-1) \
                            and (self.body[index - 1] - block) == Vector2(0,-1)) \
                        or ((self.body[index - 1] - self.body[index + 1]) == Vector2(-1,1) \
                            and (self.body[index - 1] - block) == Vector2(-1,0)):
                    surface = self.body_topleft

                screen.blit(surface, block_rect)
                
                #self.draw_body(block, block_rect)
            else: 
                if (self.body[sz - 2] - block) == Vector2(1,0): 
                    screen.blit(self.tail_left, block_rect)
                elif (self.body[sz - 2] - block) == Vector2(-1,0):
                    screen.blit(self.tail_right, block_rect) 
                elif (self.body[sz - 2] - block) == Vector2(0,1):
                    screen.blit(self.tail_up, block_rect)
                else:
                    screen.blit(self.tail_down, block_rect)
            #pygame.draw.rect(screen, self.color, block_rect)

    def draw_head(self, rect: Rect):
        # Check the head direction
        if self.direction == Vector2(1,0):
            surface = self.head_right
        elif self.direction == Vector2(-1,0):
            surface = self.head_left
        elif self.direction == Vector2(0,1):
            surface = self.head_down
        else:
            surface = self.head_up

        screen.blit(surface, rect)



    def move_snake(self, direction):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False 
        else:       
            body_copy = self.body[:-1]
        
        body_copy.insert(0, self.body[0] + direction)
        self.body = body_copy.copy()

    def set_direction(self, direction):
        self.direction = direction

    def add_block(self):
        self.new_block = True

class Fruit:
    def __init__(self):
        self.randomize()
        self.color = FRUIT_COLOR
        self.sprite = pygame.image.load(os.path.join(IMGDIR, 'apple.png')) 

    def draw_fruit(self):
        fruit_rect = Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.sprite, fruit_rect)

    def randomize(self):
        self.x = random.randint(2, cell_num-1)
        self.y = random.randint(2, cell_num-1)
        self.pos = Vector2(self.x, self.y)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 3
        self.state = 1

    def update(self, direction): #Check if the new direction is allowed
        self.check_collision()
        self.check_game_over()
        self.snake.set_direction(direction) 
        self.snake.move_snake(direction)

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.snake.body[0] == self.fruit.pos: # If the head touches the body
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 1

    def draw_score(self):
        score_string = str(self.score)
        score_text = font.render(score_string, True, TEXT_COLOR)
        score_text_rect = score_text.get_rect(center=((3*cell_size)/2 + (pos_score_x), cell_size))
        screen.blit(score_text, score_text_rect)

    def game_over(self):
        self.state = 2

    def check_game_over(self):
        if (self.snake.body[0].x < 0 or self.snake.body[0].x > cell_num-1) \
                or (self.snake.body[0].y < 2 or self.snake.body[0].y > cell_num + 1):
            #Game over
            self.game_over()
        
        for index, block in enumerate(self.snake.body):
            if block == self.snake.body[0] and index != 0: # If the head bumps into the body
                #Game over
                self.game_over()

    def draw_main_menu(self):
        screen.fill((124,124,124))

    def draw_game_over(self):
        width = cell_size * 7
        height = cell_size * 10
        x_pos_tile = cell_num/2 * cell_size - width/2
        y_pos_tile = (cell_num + 2)/2 * cell_size - cell_size/2 - (cell_size * 8)/2 
        game_over_tile = Rect(x_pos_tile, y_pos_tile , width, height)
        pygame.draw.rect(screen, (0,0,0), game_over_tile)

#Variables
IMGDIR = 'snake/assets/'
cell_size = 40
cell_num = 15 
game_time = 150 #150ms
game_fps = 60
running = True
dir = Vector2(1,0)

# Constants 
SNAKE_COLOR = Color(73, 159, 104)
FRUIT_COLOR = Color(219, 58, 52)
BCG_COLOR = Color(87, 100, 144)
BAR_COLOR = Color(191, 152, 160)
SCORE_BOX_COLOR = Color(255,255,255)
TEXT_COLOR = Color(0, 0, 0)

pygame.init()
font = pygame.font.SysFont('arial', 48, bold=True)
pygame.display.set_caption('Snake')
size = width, height = (int(cell_size * cell_num), int(cell_size * cell_num) + 2*cell_size)
top_bar = pygame.Rect(0, 0, int(width), int(2 * cell_size))
pos_score_box = pos_score_x, pos_score_y = (int(cell_num / 2) - 1) * cell_size, 0
score_box = pygame.Rect(pos_score_x, pos_score_y + 5, 3 * cell_size, 2 * cell_size - 10)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, game_time)

main_game = Main()

while running:
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.USEREVENT and main_game.state == 1:
            main_game.update(dir)
        
        #Keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: # Go left
                dir = Vector2(-1, 0)
            if event.key == pygame.K_s: # Go down
                dir = Vector2(0, 1)
            if event.key == pygame.K_d: # Go right
                dir = Vector2(1, 0)
            if event.key == pygame.K_w:
                dir = Vector2(0, -1)

    if (dir == Vector2(1, 0) and main_game.snake.direction == Vector2(-1, 0)) \
            or (dir == Vector2(-1, 0) and main_game.snake.direction == Vector2(1, 0)) \
            or (dir == Vector2(0, 1) and main_game.snake.direction == Vector2(0, -1)) \
            or (dir == Vector2(0, -1) and main_game.snake.direction == Vector2(0, 1)): 
        dir = main_game.snake.direction

    # Game handler
    if main_game.state == 0: # Main menu
        main_game.draw_main_menu()
    elif main_game.state == 1: # Main game
        screen.fill(BCG_COLOR)
        pygame.draw.rect(screen, BAR_COLOR, top_bar)  
        pygame.draw.rect(screen, SCORE_BOX_COLOR, score_box, border_radius=15)
        main_game.draw_elements()    
    elif main_game.state == 2: #Game over
        main_game.draw_game_over()

    pygame.display.flip()
    clock.tick(60) #Max 60fps
