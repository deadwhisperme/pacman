import sys
import pygame
from pygame.locals import *
from math import floor
import random


def init_window():
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Packman')


def draw_background(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((0, 0, 0))
        scr.blit(bg, (0, 0))


class GameObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y, tile_size, map_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.tile_size = tile_size
        self.map_size = map_size
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size )

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class Ghost(GameObject):
    ghosts=[]
    num=2
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0


    def game_tick(self):
        super(Ghost, self).game_tick()
        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)

        if self.direction == 1:
            if not is_wall(floor(self.x+self.velocity), self.y):
                self.x += self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 2:
            if not is_wall(self.x,(floor( self.y+self.velocity))):
                self.y += self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 3:
            if not is_wall(floor(self.x-self.velocity),self.y):
                self.x -= self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.x <= 0:
                self.x = 0
                self.direction = random.randint(1, 4)
        elif self.direction == 4:
            if not is_wall(self.x,(floor(self.y-self.velocity))):
                self.y -= self.velocity
            else:
                self.direction = random.randint(1, 4)
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
        self.set_coord(self.x, self.y)

def draw_ghosts(screen):
    for g in ghosts:
        g.draw(screen)
        g.game_tick()


def tick_ghosts():
    for g in Ghost.ghosts:
        g.game_tick()

class Map(GameObject):
    def __init__(self,x,y):
        self.map=[[list]*x for i in range (y)]
    def get(self,x,y):
        return self.map[x][y]


class Pacman(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        self.food=0
        GameObject.__init__(self, './resources/pacmanvpravo.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 1:
            if not is_wall(floor(self.x+self.velocity), self.y):
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
        elif self.direction == 2:
            if not is_wall(self.x,(floor(self.y+self.velocity))):
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
        elif self.direction == 3:
            if not is_wall(floor(self.x-self.velocity),self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if not is_wall(self.x,(floor(self.y-self.velocity))):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0

        self.set_coord(self.x, self.y)

class Food(GameObject):

    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/food.png', x,y,tile_size,map_size)
        self.life=1

def draw_food(screen):
    for f in food:
        if f.life>0:
            GameObject.draw(f,screen)

def process_events(events, packman):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
                pacman.image=pygame.image.load('./resources/pacmanvlevo.png')
            elif event.key == K_RIGHT:
                packman.direction = 1
                pacman.image=pygame.image.load('./resources/pacmanvpravo.png')
            elif event.key == K_UP:
                packman.direction = 4
                pacman.image=pygame.image.load('./resources/pacmanvverh.png')
            elif event.key == K_DOWN:
                packman.direction = 2
                pacman.image=pygame.image.load('./resources/pacmanvniz.png')
            elif event.key == K_SPACE:
                packman.direction = 0


class Wall(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/wall.png', x, y, tile_size, map_size)

    def get(self,x,y):
        return self.map[x][y]


def is_wall(x, y):
    for w in walls:
        if (int(w.x), int(w.y)) == (int(x), int(y)):
            return True
    return False

def draw_walls(screen):
    for w in walls:
        GameObject.draw(w,screen)


if __name__ == '__main__':
    init_window()
    tile_size = 32
    map_size = 16
    walls=[]
    ghosts=[]
    food=[]
    input=open('map.txt','r')
    for i in range (17):
        for a in range(17):
            s=input.read(1)
            if s=='w':
                walls.append(Wall(a,i,tile_size,map_size))
            elif s=='g':
                ghosts.append(Ghost(a,i,tile_size,map_size))
            elif s=='f':
                food.append(Food(a,i,tile_size,map_size))
    pacman = Pacman(5, 5, tile_size, map_size)
    background = pygame.image.load("./resources/background.png")
    screen = pygame.display.get_surface()


    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(100)
        pacman.game_tick()
        draw_background(screen, background)
        draw_walls(screen)
        draw_food(screen)
        draw_ghosts(screen)
        for f in food:
            if int(f.x)==int(pacman.x) and int(f.y)==int(pacman.y):
                food.remove(f)
                if len(food) == 0:
                    sys.exit()
        pacman.draw(screen)
        pygame.display.update()
        for g in ghosts:
            if int(g.x)==int(pacman.x) and int(g.y)==int(pacman.y):
                sys.exit()

