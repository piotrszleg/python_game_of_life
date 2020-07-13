import sys
import pygame
from pygame.locals import *

# all positions inside the games are represented by this type
class Vector2:
  def __init__(self, x, y):
    self.x=x
    self.y=y

TILE_SIZE=4 # width and height of one tile in screen pixels
TILE_COUNT=Vector2(300, 200) # size of screen in tiles
SCREEN=Vector2(TILE_COUNT.x*TILE_SIZE, TILE_COUNT.y*TILE_SIZE) # size of screen in tiles
FPS=30.0 # frames per second

# draw array of blocks on screen
def drawBlocks(display, blocks, position=Vector2(0, 0)):
  for y in range(0,  len(blocks)):
    for x in range(0, len(blocks[y])):
      if blocks[y][x]:
        color=(255,)*3
        if isinstance(blocks[y][x], tuple):  # if block contains color information as tuple use it
          color=blocks[y][x]
        pygame.draw.rect(display, color, tuple(i*TILE_SIZE for i in (x+position.x, y+position.y, 1,1)))

# change color of all blocks inside array
def colorBlocks(blocks, color):
  for y in range(0,  len(blocks)):
    for x in range(0, len(blocks[y])):
      if blocks[y][x]:  # if tile is nonempty change it to color tuple
        blocks[y][x]=color
  return blocks

class GameOfLife:
  def start(self):# starts game
    self.board = [[0 for x in range(TILE_COUNT.x)] for y in range(TILE_COUNT.y)] # array containing all cells
    self.mouse_down=False
    #self.randomise()

  def randomise(self):
    from random import random
    self.board = [[random()>0.1 for x in range(TILE_COUNT.x)] for y in range(TILE_COUNT.y)]

  def circle(self, cx, cy, r):
    rr=r*r
    for y in range(0, TILE_COUNT.y):
      for x in range(0, TILE_COUNT.x):
        dx=x-cx
        dy=y-cy
        if dx*dx+dy*dy<=rr:
          self.board[y][x]=1

  def run(self): # initializes pygame and starts game loop
    pygame.init()
    self.start()
    fpsClock = pygame.time.Clock()
    display = pygame.display.set_mode((SCREEN.x, SCREEN.y))
    dt = 1/FPS
    while True:
      for event in pygame.event.get():
        self.handleEvent(event)
      if not self.mouse_down:
        self.update(dt)
      self.draw(display)
      dt = fpsClock.tick(FPS)
  
  def handleEvent(self, event):
    if event.type == QUIT: # quit game when 'x' button on window is pressed
      pygame.quit()
      sys.exit()
    elif event.type == MOUSEBUTTONDOWN:
      self.mouse_down=True
    elif event.type == MOUSEBUTTONUP:
      self.mouse_down=False
    elif event.type == MOUSEMOTION and self.mouse_down: # add blocks if the mouse button is held
      x, y = pygame.mouse.get_pos()
      self.circle(x/TILE_SIZE, y/TILE_SIZE, 4)
      # self.board[int(y/TILE_SIZE)][int(x/TILE_SIZE)]=1

  def get(self, x, y):
    return self.board[y%TILE_COUNT.y][x%TILE_COUNT.x]

  def neighbours(self, x, y):
    return self.get(x+1, y)+self.get(x-1, y)+self.get(x+1, y+1)+self.get(x-1, y-1)+self.get(x-1, y+1)+self.get(x+1, y-1)+self.get(x, y+1)+self.get(x, y-1)
  
  def update(self, dt):
    nboard=self.board.copy()
    for y in range(0, TILE_COUNT.y):
      for x in range(0, TILE_COUNT.x):
        neighbours=self.neighbours(x, y)
        if self.get(x, y)==1:
          if neighbours<2 or neighbours>3:
            nboard[y][x]=0
        elif neighbours==3:
          nboard[y][x]=1
    self.board=nboard
 
  def draw(self, display):
    display.fill((0, 0, 0))
    drawBlocks(display, self.board)
    pygame.display.flip()

if __name__ == "__main__":
  GameOfLife().run()