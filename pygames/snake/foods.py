import pygame
import random
import math

foods = [
  {
    'name':'apple',
    'feedAmt':3,
  },{
    'name':'banana',
    'feedAmt':8,
  },
]

class table:
  def __init__(self):
    self.foodTable = []

  def spawnRandom(self, amt = 2, border = (1000,-1000,1000,-1000)):
    for _ in range(amt):
      position = (
        ((border[1]-border[0])*random.random())+border[0],
        ((border[3]-border[2])*random.random())+border[2]
        )
      num = random.randrange(0,len(foods),1)
      self.newFood(num, position)

  def newFood(self, index = 0, position=(250,250)):
    if 0 > index or index > len(foods): return
    self.foodTable.append(
      {
        'Id':index,
        'pos':position,
      }
    )

  def foodInRadius(self, pos=(0,0), radius=12):
    for i in range(len(self.foodTable)):
      v = self.foodTable[i]
      if math.sqrt(math.pow(pos[0]-v['pos'][0],2)+math.pow(pos[1]-v['pos'][1],2)) <= radius:
        return foods[v['Id']], i 

  def remove(self,index):
     return self.foodTable.pop(index)

  def render(self, screen,offset = (0,0)):
    for v in self.foodTable:
      pygame.draw.circle(screen,(255,0,0), (v['pos'][0]+offset[0],v['pos'][1]+offset[1]), 10)