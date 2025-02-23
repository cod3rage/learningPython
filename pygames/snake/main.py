import sys
import pygame
import enitity 
import foods
import random

pygame.init()

class game:
  def __init__(self):
    self.screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption('snake test.     FPS:??')
    self.clock = pygame.time.Clock()
    self.running = True
    # base run varibles

    self.scroll = [0,0]
    self.innerClock = 0
    
    # customize this
    self.Snake = enitity.Snake(bones=5,width=8,position=(250,250),tail=18,debug=False)
    
    self.foodTable = foods.table()
    self.foodTable.spawnRandom(40,(-250,250,-250,250))
    

  def start(self):
    while self.running:
      self.inputs() # captures user inputs
      self.update() # updates physics and positioning
      self.render() # renders on screen
      pygame.display.update()
      self.dt = self.clock.tick(60) / 1000
      pygame.display.set_caption(f'snake test.     FPS:{round(self.clock.get_fps())}')
  
  def update(self):
    self.scroll[0]+=round((self.screen.get_width()/2-self.Snake.position[0]-self.scroll[0])/30,2)
    self.scroll[1]+=round((self.screen.get_height()/2-self.Snake.position[1]-self.scroll[1])/30,2)
    self.Snake.update()

    

  def render(self):
    self.screen.fill((31, 38, 32))
    self.Snake.render(self.screen,self.scroll)
    self.foodTable.render(self.screen,self.scroll)

  def inputs(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
        pygame.quit()
        sys.exit()
    
    keys_down = pygame.key.get_pressed()
    speed = 20 if keys_down[pygame.K_LSHIFT] else 5
    
    vals = (
      (keys_down[pygame.K_d] - keys_down[pygame.K_a])*speed, 
      (keys_down[pygame.K_s] - keys_down[pygame.K_w])*speed
    )

    # true = 1 false = 0 

    if keys_down[pygame.K_q]:
      self.scroll = (self.scroll[0]+1,self.scroll[1]+1)


    self.Snake.move(vals)
    food = self.foodTable.foodInRadius(self.Snake.position, 50)
    if food:
      self.Snake.feed(food[0]['feedAmt'])
      self.foodTable.remove(food[1])
      self.foodTable.spawnRandom(1,(-250,250,-250,250))

    

game().start()
pygame.quit() # ends if game loops quits / ends