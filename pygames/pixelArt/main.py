import pygame
from math import floor
    
class pixel_drawer:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((634,500))
    pygame.display.set_caption('pixel draw')
    self.clock = pygame.time.Clock()
    self.running = True

    self.grid_surface = pygame.surface.Surface((480,480))
    self.grid_surface = self.grid_surface.convert_alpha()

    self.grid_background = pygame.surface.Surface((480,480))
    self.grid = {}

    self.color0 = (255,0,0)
    self.color1 = (0,0,255)
  
  def run(self):
    self.render()
    while self.running:
      self.inputs()
      self.render()
      self.update()

      pygame.display.update()
      self.screen.blit(self.grid_surface,(144,10))

      self.clock.tick(60)

  def render(self):
    self.screen.fill((20,20,20))
    
    self.grid_background.fill((7,7,7))

    for section in range(15):
      pygame.draw.line(self.grid_background,(20,20,20),(0,(section+1)*30),(480,(section+1)*30),2)
      pygame.draw.line(self.grid_background,(20,20,20),((section+1)*30,0),((section+1)*30,480),2)
    self.screen.blit(self.grid_background,(144,10))
    
    self.grid_surface.fill(pygame.color.Color(0,0,0,0))
    for val in self.grid.values():
      pygame.draw.rect(self.grid_surface,val[1],val[0])
    self.screen.blit(self.grid_surface,(144,10))
  
  def inputs(self):
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False

    if 144 <= mouse_pos[0] <= 624 and  10 <= mouse_pos[1] <= 490:
      mouse_pressed = pygame.mouse.get_pressed()
      if mouse_pressed[0]:
        self.draw(mouse_pos,self.color0)
      elif mouse_pressed[2]:
        self.draw(mouse_pos,self.color1)

  def update(self):
    pass

  def draw(self,mouse_pos=(0,0),color=(255,255,255)):
    base_x,base_y = floor((mouse_pos[0] - 144)/30)  ,  floor((mouse_pos[1] - 10)/30)
    chunk = str(base_x)+':'+str(base_y)
    if chunk in self.grid:
      chuck_color = self.grid[chunk][1]
      if chuck_color[0] != color[0] or chuck_color[1] != color[1] or chuck_color[2] != color[2]:
        self.erase(chunk,True)
        
    self.grid[chunk] = [pygame.rect.Rect(base_x*30,base_y*30,30,30),color]

  def erase(self, mouse_pos = (0,0), chunk=False):
    if chunk and mouse_pos in self.grid:
      self.grid.pop(mouse_pos)
      return  
    chunk = str(floor((mouse_pos[0] - 144)/30))+':'+str(floor((mouse_pos[1] - 10)/30))
    if chunk in self.grid: self.erase(chunk,True)


pixel_drawer().run()