import pygame, sys, random
from pygame.math import Vector2
from tetris import *
from random import randint
import copy

pygame.init()
cell_size = 40
cell_height = 20
cell_width = 10
screen = pygame.display.set_mode((cell_width * cell_size, cell_height * cell_size))
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)
clock = pygame.time.Clock()
game_state = 'start_menu'

blocks = ['O', 'L', 'J', 'S', 'Z', 'T', 'I']

map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

#text stuff
game_font = pygame.font.Font("freesansbold.ttf", 23)

def draw_start_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('arial', 40)
    title = font.render('My Game', True, (255, 255, 255))
    start_button = font.render('Start', True, (255, 255, 255))
    screen.blit(title, (400, 800))
    pygame.display.update()


class Tetris():
    def __init__(self):
        self.new_block()
        self.end = False
        self.player_score = 0

    def draw_grid(self):
        screen.fill((128, 128, 128))
        self.draw_blocks()

        for i in range(cell_height):
            for x in range(cell_width):
                pygame.draw.rect(screen, 'black', (x * cell_size, i * cell_size, cell_size, cell_size), 1)
        
        player_text = game_font.render(f"{self.player_score}", True, (255, 255, 255))
        screen.blit(player_text, (20, 12))

        pygame.display.update()

    def draw_blocks(self):
        for i in range(len(map)):
            for x in range(len(map[i])):
                if map[i][x] == 'O':
                    pygame.draw.rect(screen, 'yellow', (x * cell_size, i * cell_size, cell_size, cell_size))
                if map[i][x] == 'L':
                    pygame.draw.rect(screen, 'orange', (x * cell_size, i * cell_size, cell_size, cell_size))
                if map[i][x] == 'J':
                    pygame.draw.rect(screen, 'magenta', (x * cell_size, i * cell_size, cell_size, cell_size))
                if map[i][x] == 'I':
                    pygame.draw.rect(screen, 'cyan', (x * cell_size, i * cell_size, cell_size, cell_size))
                if map[i][x] == 'T':
                    pygame.draw.rect(screen, 'purple', (x * cell_size, i * cell_size, cell_size, cell_size))
                if map[i][x] == 'S':
                    pygame.draw.rect(screen, 'green', (x * cell_size, i * cell_size, cell_size, cell_size))
                if map[i][x] == 'Z':
                    pygame.draw.rect(screen, 'red', (x * cell_size, i * cell_size, cell_size, cell_size))

    def random_block(self):
        num = randint(0, 6)
        return blocks[num]


    def game_loop(self):
        if self.current_block.grounded == False:
            vals = [pos.x for pos in self.current_block.pos]
            vals.sort()
            if vals[-1] == 19:
                self.current_block.grounded = True
                tetris.line_check()
                # generate new block
                self.new_block()
                print(self.current_block.pos)
            else:
                self.current_block.move_down()
        else:
            self.new_block()

    def new_block(self):
        self.current_block = Tetromino(self.random_block())
        self.current_block.spawn_block()

    def line_check(self):
        for i in range(len(map)):
            if 0 not in map[i] and self.current_block.grounded == True:
                map.pop(i)
                map.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                self.player_score += 100

        for x in map[0]:
            if x != 0 and self.current_block.grounded:
                self.end = True

    def reset(self):
        self.player_score = 0
        self.new_block()
        global map
        print(map)
        map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        print(map)
       

class Tetromino():
    def __init__(self, block_type):
        self.orientation = 0
        self.block_type = block_type
        self.pos = []
        self.grounded = False

    def spawn_block(self):
        if self.block_type == 'O':
            self.pos = [Vector2(0, 5), Vector2(0, 6), Vector2(1, 5), Vector2(1,6)]
        if self.block_type == 'L':
            self.pos = [Vector2(0, 5), Vector2(1, 5), Vector2(2, 5), Vector2(2,6)]
        if self.block_type == 'J':
            self.pos = [Vector2(0, 6), Vector2(1, 6), Vector2(2, 6), Vector2(2,5)]
        if self.block_type == 'I':
            self.pos = [Vector2(0, 5), Vector2(1, 5), Vector2(2, 5), Vector2(3,5)]
        if self.block_type == 'T':
            self.pos = [Vector2(0, 5), Vector2(0, 6), Vector2(0, 7), Vector2(1, 6)]
        if self.block_type == 'S':
            self.pos = [Vector2(0, 5), Vector2(0, 6), Vector2(1, 4), Vector2(1, 5)]
        if self.block_type == 'Z':
            self.pos = [Vector2(0, 5), Vector2(0, 6), Vector2(1, 6), Vector2(1, 7)]

        self.update_pos()

    def rotate(self):
        past = copy.deepcopy(self.pos)
        counter = 0
        for position in self.pos:
            map[round(position.x)][round(position.y)] = 0

        if self.block_type == 'O':
            pass
        if self.block_type == 'L':
            if self.orientation == 0:
                self.pos[0] += (1, 1)
                self.pos[1] += (0, 0)
                self.pos[2] += (-1, -1)
                self.pos[3] += (0, -2)

            if self.orientation == 1:
                self.pos[0] += (1, -1)
                self.pos[1] += (0, 0)
                self.pos[2] += (-1, 1)
                self.pos[3] += (-2, 0)

            if self.orientation == 2:
                self.pos[0] += (-1, -1)
                self.pos[1] += (0, 0)
                self.pos[2] += (1, 1)
                self.pos[3] += (0, 2)

            if self.orientation == 3:
                self.pos[0] += (-1, 1)
                self.pos[1] += (0, 0)
                self.pos[2] += (1, -1)
                self.pos[3] += (2, 0)

        if self.block_type == 'J':
            if self.orientation == 0:
                self.pos[0] += (1, 1)
                self.pos[1] += (0, 0)
                self.pos[2] += (-1, -1)
                self.pos[3] += (-2, 0)

            if self.orientation == 1:
                self.pos[0] += (1, -1)
                self.pos[1] += (0, 0)
                self.pos[2] += (-1, 1)
                self.pos[3] += (0, 2)

            if self.orientation == 2:
                self.pos[0] += (-1, -1)
                self.pos[1] += (0, 0)
                self.pos[2] += (1, 1)
                self.pos[3] += (2, 0)

            if self.orientation == 3:
                self.pos[0] += (-1, 1)
                self.pos[1] += (0, 0)
                self.pos[2] += (1, -1)
                self.pos[3] += (0, -2)

        if self.block_type == 'I':
            if self.orientation == 0:
                self.pos[0] += (1, 2)
                self.pos[1] += (0, 1)
                self.pos[2] += (-1, 0)
                self.pos[3] += (-2, -1)

            if self.orientation == 1:
                self.pos[0] += (2, -1)
                self.pos[1] += (1, 0)
                self.pos[2] += (0, 1)
                self.pos[3] += (-1, 2)
                
            if self.orientation == 2:
                self.pos[0] += (-1, -2)
                self.pos[1] += (0, -1)
                self.pos[2] += (1, 0)
                self.pos[3] += (2, 1)

            if self.orientation == 3:
                self.pos[0] += (-2, 1)
                self.pos[1] += (-1, 0)
                self.pos[2] += (0, -1)
                self.pos[3] += (1, -2)

        if self.block_type == 'T':
            if self.orientation == 0:
                self.pos[0] += (-1, 1)
                self.pos[1] += (0, 0)
                self.pos[2] += (1, -1)
                self.pos[3] += (-1, -1)

            if self.orientation == 1:
                self.pos[0] += (1, 1)
                self.pos[1] += (0, 0)
                self.pos[2] += (-1, -1)
                self.pos[3] += (-1, 1)
                
            if self.orientation == 2:
                self.pos[0] += (1, -1)
                self.pos[1] += (0, 0)
                self.pos[2] += (-1, 1)
                self.pos[3] += (1, 1)

            if self.orientation == 3:
                self.pos[0] += (-1, -1)
                self.pos[1] += (0, 0)
                self.pos[2] += (1, 1)
                self.pos[3] += (1, -1)
        
        if self.block_type == 'Z':
            if self.orientation == 0:
                self.pos[0] += (0, 2)
                self.pos[1] += (1, 1)
                self.pos[2] += (0, 0)
                self.pos[3] += (1, -1)

            if self.orientation == 1:
                self.pos[0] += (2, 0)
                self.pos[1] += (1, -1)
                self.pos[2] += (0, 0)
                self.pos[3] += (-1, -1)
                
            if self.orientation == 2:
                self.pos[0] += (0, -2)
                self.pos[1] += (-1, -1)
                self.pos[2] += (0, 0)
                self.pos[3] += (-1, 1)

            if self.orientation == 3:
                self.pos[0] += (-2, 0)
                self.pos[1] += (-1, 1)
                self.pos[2] += (0, 0)
                self.pos[3] += (1, 1)

        if self.block_type == 'S':
            if self.orientation == 0:
                self.pos[0] += (1, 1)
                self.pos[1] += (2, 0)
                self.pos[2] += (-1, 1)
                self.pos[3] += (0, 0)

            if self.orientation == 1:
                self.pos[0] += (1, -1)
                self.pos[1] += (0, -2)
                self.pos[2] += (1, 1)
                self.pos[3] += (0, 0)
                
            if self.orientation == 2:
                self.pos[0] += (-1, -1)
                self.pos[1] += (-2, 0)
                self.pos[2] += (1, -1)
                self.pos[3] += (0, 0)

            if self.orientation == 3:
                self.pos[0] += (-1, 1)
                self.pos[1] += (0, 2)
                self.pos[2] += (-1, -1)
                self.pos[3] += (0, 0)

        for element in self.pos:
            try:
                if map[round(element.x)][round(element.y)] or round(element.y) < 0:
                    print('detected')
                    self.orientation -= 1
                    break
                else:
                    print('not detected')
                    print(element.y)
                    counter += 1
            except IndexError:
                print('out of bounds')
                self.orientation -= 1
                break
        
        print(counter)
        if counter != 4:
            print('changing')
            self.pos = past

        self.orientation += 1
        if self.orientation >= 4:
            self.orientation = 0

        self.update_pos()
        


    def move_down(self):
        lst = [x for x in self.pos]
        unique_vectors = {}

        for vec in lst:
            y, x = vec
            if x not in unique_vectors or y > unique_vectors[x][0]:
                unique_vectors[x] = vec

        final = list(unique_vectors.values())

        
        ground_vectors = [x + Vector2(1, 0) for x in final]

        for element in ground_vectors:
            try:
                if map[round(element.x)][round(element.y)] != 0:
                    self.grounded = True
                    tetris.line_check()
                    break
            except IndexError:
                self.grounded = True
                tetris.line_check()
                break

        if self.grounded == False: 
            for i in self.pos:
                map[round(i.x)][round(i.y)] = 0
                i += Vector2(1, 0)
            self.update_pos()

    def move_right(self):
        self.colliding_right = False
        lst = [x for x in self.pos]
        unique_vectors = {}

        for vec in lst:
            y, x = vec
            print(y, x)
            if y not in unique_vectors or x > unique_vectors[y][1]:
                unique_vectors[y] = vec

        final = list(unique_vectors.values())

        
        ground_vectors = [x + Vector2(0, 1) for x in final]

        for element in ground_vectors:
            try:
                if map[round(element.x)][round(element.y)] != 0:
                    self.colliding_right = True
                    break
            except IndexError:
                    self.colliding_right = True
                    break


        if self.colliding_right == False:
            for i in self.pos:
                map[round(i.x)][round(i.y)] = 0
                i += Vector2(0, 1)
            self.update_pos()
    
    def move_left(self):
        self.colliding_left = False
        lst = [x for x in self.pos]
        unique_vectors = {}

        for vec in lst:
            y, x = vec
            if y not in unique_vectors or x < unique_vectors[y][1]:
                unique_vectors[y] = vec

        final = list(unique_vectors.values())

        
        ground_vectors = [x - Vector2(0, 1) for x in final]

        print(ground_vectors)
        for element in ground_vectors:
            if map[round(element.x)][round(element.y)] != 0 or element.y < 0:
                self.colliding_left = True
                break

        if self.colliding_left == False:
            for i in self.pos:
                map[round(i.x)][round(i.y)] = 0
                i -= Vector2(0, 1)
            self.update_pos()

    def update_pos(self):
        for block in self.pos:
            map[round(block.x)][round(block.y)] = self.block_type


# tetro = Tetromino('I')

# tetro.spawn_block()
tetris = Tetris()    


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if tetris.end == True:
                print('tetris called')
                tetris.reset()
                tetris.end = False
            if tetris.current_block.grounded == False:
                if event.key == pygame.K_DOWN and tetris.end == False:
                    tetris.current_block.move_down()
                if event.key == pygame.K_LEFT and tetris.end == False:
                    tetris.current_block.move_left()
                if event.key == pygame.K_RIGHT and tetris.end == False:
                    tetris.current_block.move_right()
                if event.key == pygame.K_UP and tetris.end == False:
                    tetris.current_block.rotate()
        if event.type == GAME_UPDATE and tetris.end == False:
            tetris.game_loop()

    # if tetris.end:
    #     break

    tetris.draw_grid()

    clock.tick(60)