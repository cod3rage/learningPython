import pygame
import math


class WobblyBody:
  def __init__(self,bones=12,width=12, position=(0,0),boneInfo={}, tail = None, color = (255,255,255), debug = False, grow = False, maxFoodWidth = 15):
    self.growable = grow
    self.maxFoodWidth = maxFoodWidth
    self.tail = tail or width
    self.debug = debug
    self.width = width
    self.radius = self.width/2
    self.bones = {}
    self.boneInfo = boneInfo
    self.angle = math.pi/2
    self.eatingPaused = False
    self.position = position
    self.color = color
    self.points = [[],[]]
    for i in range(abs(round(bones))+1):
      pos = (self.radius*i+position[0], position[1])
      segment = self.radius
      if str(i) in boneInfo:
        segment = boneInfo[str(i)]
      elif i-1 >= self.tail:
        segment = (bones-i)/(bones-self.tail)*self.radius
      pointSegments = ((pos[0], pos[1] + segment),(pos[0], pos[1] - segment))
      self.bones[str(i)] = {
        'pos':pos,
        'rotation':0,
        'boneRadius': segment,
        'additionalRad':0,
        'point0': pointSegments[0],
        'point1': pointSegments[1],
      }
      self.points[1].append(pointSegments[1])
      self.points[0].append(pointSegments[0])

      self.stomach = []
    
  # def evolve():
  #   pass

  def update(self):
    self.points =[[],[]]
    quickWrap = False

    for i in range(len(self.stomach)): 
      contents = self.stomach[i]
      if contents['moved']:
        pos = contents['pos']
        if pos + 1 >= len(self.bones):
          if (pastpos := self.bones.get(str(pos))):
            pastpos['additionalRad'] -= contents['scale']/2
          if (pastpos := self.bones.get(str(pos-1))):
            pastpos['additionalRad'] -= contents['scale']
          if (pastpos := self.bones.get(str(pos-2))):
            pastpos['additionalRad'] -= contents['scale']/2
          self.bones['0']['additionalRad'] += contents['scale']/2
          self.stomach.pop(i)
          self.grow() 
          break
          # digested
        else:
          half = contents['scale'] / 2
          if (pastpos := self.bones.get(str(pos - 2))):
            pastpos['additionalRad'] -= half #-2 pos
          if (pastpos := self.bones.get(str(pos - 1))):
            pastpos['additionalRad'] -= half #-1 pos
          if (pastpos := self.bones.get(str(pos))):
            pastpos['additionalRad'] += half #0 pos
          if (pastpos := self.bones.get(str(pos + 1))):
            pastpos['additionalRad'] += half #+1 pos
          contents['pos'] += 1
          contents['moved'] = False


    for index in range(len(self.bones)):
      value = self.bones[str(index)]
      if index == 0: continue
      if quickWrap:
        self.points[0].append(value['point0'])
        self.points[1].append(value['point1'])
        continue
      lastValue = self.bones[str(index-1)]
      xDifference = value['pos'][0]-lastValue['pos'][0]
      yDifference = value['pos'][1]-lastValue['pos'][1]
      # basic distance formula
      distance = math.sqrt(math.pow(xDifference,2)+math.pow(yDifference,2))
      pastPoint = distance > self.width

      if pastPoint:
        # atan2 takes the relitive position and the angle make from it and 0,0
        # then returns a number -pi through pi
        value['rotation'] = math.atan2(yDifference,xDifference) 
        value['pos'] = (
          # cos turns the x rotation into the corisponding x position
          # then it;s multiplied by max distance - 1 (-1 so then it doesnt update too much)
          # lastValue makes it relitive to the last point position
          math.cos(value['rotation'])*(self.width-1)+lastValue['pos'][0],
          math.sin(value['rotation'])*(self.width-1)+lastValue['pos'][1]
        ) # rotation to pos
        value['point0'] = (
          # cos ( rotation + angle ) adds the 90* or 1/2pi to the original angle
          # then the x position is calculated with the cos*radius
          # value pos makes it relitive to the bone
          math.cos(value['rotation']+self.angle)*(value['boneRadius']+min(value['additionalRad'],self.maxFoodWidth))+value['pos'][0],
          math.sin(value['rotation']+self.angle)*(value['boneRadius']+min(value['additionalRad'],self.maxFoodWidth))+value['pos'][1]
        ) # edge attachments (bone width)
        value['point1'] = (
          math.cos(value['rotation']-self.angle)*(value['boneRadius']+min(value['additionalRad'],self.maxFoodWidth))+value['pos'][0],
          math.sin(value['rotation']-self.angle)*(value['boneRadius']+min(value['additionalRad'],self.maxFoodWidth))+value['pos'][1]
        )
        
        for contents in self.stomach:
          if contents['pos'] == index:
            contents['moved'] = True
      else:
        quickWrap = True
      
      self.points[0].append(value['point0'])
      self.points[1].append(value['point1'])
      
      

  def render(self,screen, offset):
    copy0, copy1 = self.points[0].copy(),self.points[1].copy()
    for x in range(len(copy0)):
      copy0[x] = (copy0[x][0]+offset[0], copy0[x][1]+offset[1])
    
    for x in range(len(copy1)):
      copy1[x] = (copy1[x][0]+offset[0], copy1[x][1]+offset[1])
       
    copy1.reverse()
    copy0.extend(copy1)
    
    if self.debug:
      for v in self.bones.values():
        pygame.draw.circle(screen,(255,255,255),(v['pos'][0]+offset[0],v['pos'][1]+offset[1]),self.radius)
        pygame.draw.circle(screen,(255,0,0),(v['point0'][0]+offset[0],v['point0'][1]+offset[1]),3)
        pygame.draw.circle(screen,(255,0,0),(v['point1'][0]+offset[0],v['point1'][1]+offset[1]),3)
    
    pygame.draw.polygon(screen,self.color,copy0)
  
  def move(self,add=(0,0)):
    if add[0] == 0 and add[1] == 0: return
    Bone0 = self.bones['0']
    Bone0['pos'] = (Bone0['pos'][0]+add[0], Bone0['pos'][1]+add[1])
    Bone0['rotation'] = math.atan2(add[1],add[0])
    Bone0['point0'] = (
      math.cos(Bone0['rotation']+self.angle)*Bone0['boneRadius']+Bone0['pos'][0],
      math.sin(Bone0['rotation']+self.angle)*Bone0['boneRadius']+Bone0['pos'][1]
    )
    Bone0['point1'] = (
      math.cos(Bone0['rotation']-self.angle)*Bone0['boneRadius']+Bone0['pos'][0],
      math.sin(Bone0['rotation']-self.angle)*Bone0['boneRadius']+Bone0['pos'][1]
    )
    self.position = Bone0['pos']
  
  def feed(self, scale = 5):
    self.stomach.append({'scale':scale, 'pos':0, 'moved':True})
  
  def grow(self):
    if not self.growable: return
    
    i = len(self.bones)
    v = self.bones[str(i-1)]
    pos = (v['pos'][0], v['pos'][1])
    pointSegments = ((pos[0], pos[1]),(pos[0]+.1, pos[1]))
    self.bones[str(i)] = {
      'pos':pos,
      'rotation':0,
      'boneRadius': .1,
      'additionalRad':0,
      'point0': pointSegments[0],
      'point1': pointSegments[1],
    }

    
    for num in range(i):
      segment = self.radius
      if str(num) in self.boneInfo:
        segment = self.boneInfo[str(num)]
      elif num-1 >= self.tail:
        segment = (i-num)/(i-self.tail)*self.radius
      self.bones[str(num)]['boneRadius'] = segment
      
    
    

class Snake(WobblyBody):
  def __init__(self,bones=32,width=12,position=(0,0),tail=14,color=(50,168,82),debug=False):
    boneInfo = {'2':width-width/4, '3':width-width/12}
    return super().__init__(bones, width, position, boneInfo,tail,color,debug,True)
  
  def update(self):
    return super().update()
  
  def render(self, screen, offset = (0,0)):
    return super().render(screen, offset)

  def move(self, add=(0, 0)):
    return super().move(add)
  
class Leech(WobblyBody):
  def __init__(self,bones=32,width=16,position=(0,0),tail=14,color=(168, 97, 50),debug=False):
    boneInfo = {'1':width/4,'2':width, '3':width, '4':width, '5':width-width/4}
    return super().__init__(bones, width, position, boneInfo,tail,color,debug,True)
  
  def update(self):
    return super().update()
  
  def render(self, screen, offset = (0,0)):
    return super().render(screen, offset)

  def move(self, add=(0, 0)):
    return super().move(add)
