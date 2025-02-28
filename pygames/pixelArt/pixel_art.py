"""
Filename: pixel_art.py
Author: <Lastname, Firstname>
Created: <MM/DD/YYYY>
Instructor: <Lastname>
"""

import json
import pygame

class pixel_drawer:
    def __init__(self):
        # basic pygame initialization sequence
        pygame.init()

        self.screen = pygame.display.set_mode((634, 500))
        pygame.display.set_caption('pixel draw')

        self.clock = pygame.time.Clock()
        self.running = True

        # loads drawing surface
        self.grid_surface = pygame.surface.Surface((480, 480))
        self.grid_surface = self.grid_surface.convert_alpha()

        # storage for the grid of each pixel
        self.grid = {}

        # loads the background of the grid
        self.grid_background = pygame.surface.Surface((480, 480))

        # mouse storge
        self.color0 = (255, 0, 0)
        self.color1 = (0, 0, 255)

        self.mouse0 = 'red'
        self.mouse1 = 'blue'

        
        """
        pos = y position
        signal = the way to differentiate each button
        color = allows for the mouse to change color
        border = if button is outlined or not (works without color)
        invert = if the L and R text should change from white

        """
        self.buttons = [

            
            {'pos': 15, 'signal': 'clear'},
            {'pos': 40, 'signal':'fill', 'border':(255,255,255)},

            {'pos': 105, 'signal': 'orange', 'color': (255, 165, 0), 'invert':(0,0,0)},
            {'pos': 135, 'signal': 'red', 'color': (255, 0, 0)},
            {'pos': 165, 'signal': 'violet', 'color': (238, 130, 238), 'invert':(0,0,0)},
            {'pos': 195, 'signal': 'blue', 'color': (0, 0, 255)},
            {'pos': 225, 'signal': 'yellow', 'color': (255, 255, 0),'invert':(0,0,0)},
            {'pos': 255, 'signal': 'green', 'color': (0, 255, 0),'invert':(0,0,0)},
            {'pos': 285, 'signal': 'indigo', 'color': (75, 0, 130)},
            {'pos': 315, 'signal': 'black', 'color': (0, 0, 0)},
            {'pos': 345, 'signal': 'white', 'color': (255, 255, 255),'invert':(0,0,0)},

            {'pos': 375, 'signal': 'eraser','invert':(255,0,0)},

            {'pos': 445, 'signal': 'save', 'border': (0, 255, 0)},
            {'pos': 470, 'signal': 'load', 'border': (0, 255, 0)},
        ]

        corner_radius = 2 # radius for bevel
        
        for index in range(len(self.buttons)):
            #values per button
            val = self.buttons[index]

            # sets radius limit
            radius = min(20 / 2, 124 / 2, corner_radius)

            # gets all the points for the bevel
            offset0_x, offset0_y = (9 + radius, val['pos']), (9, val['pos'] + radius)
            offset1_x, offset1_y = (133 - radius, val['pos']), (133, val['pos'] + radius)
            offset2_x, offset2_y = (9 + radius, val['pos'] + 20), (9, val['pos'] + 20 - radius)
            offset3_x, offset3_y = (133 - radius, val['pos'] + 20), (133, val['pos'] + 20 - radius)

            # gets button color
            color = val['color'] if 'color' in val else (255, 0, 0)
            if 'border' in val: color = val['border']

            # stores each point for rendering
            self.buttons[index]['geometry'] = [[offset0_y, offset0_x, offset1_x, offset1_y, offset3_y, offset3_x, offset2_x, offset2_y], color,
                        not 'color' in val]

        # body 1 font / main font
        self.b1 = pygame.font.Font(None, 16)

    def run(self):
        self.render()
        # game loop
        while self.running:
            self.inputs()
            self.render()

            pygame.display.update()
            self.screen.blit(self.grid_surface, (144, 10))

            self.clock.tick(60)

    def render(self):

        # background colors
        self.screen.fill((20, 20, 20))
        self.grid_background.fill((7, 7, 7))

        # grid lines decor
        for section in range(15):
            pygame.draw.line(self.grid_background, (20, 20, 20), (0, (section + 1) * 30), (480, (section + 1) * 30), 2)
            pygame.draw.line(self.grid_background, (20, 20, 20), ((section + 1) * 30, 0), ((section + 1) * 30, 480), 2)
        self.screen.blit(self.grid_background, (144, 10))

        # makes grid background transparent
        self.grid_surface.fill(pygame.color.Color(0, 0, 0, 0))

        # each grid pixel
        for val in self.grid.values():
            pygame.draw.rect(self.grid_surface, val[1], val[0])

        #button render
        self.render_buttons()

        # grid render
        self.screen.blit(self.grid_surface, (144, 10))
    
    def render_buttons(self):
        # loops each button
        for button in self.buttons:
            button_geometry = button['geometry']
            if not button_geometry: continue

            # chooses button color , outline and text
            if button_geometry[2]:
                pygame.draw.polygon(self.screen, button_geometry[1], button_geometry[0], 1)
                render = self.b1.render(button['signal'], 1, button_geometry[1])
                size = render.get_size()
                self.screen.blit(render, ( 71-size[0]/2 , button['pos']+size[1]/2))
            else:
                # simple color button
                pygame.draw.polygon(self.screen, button_geometry[1], button_geometry[0])
            
            # left and right update
            if self.mouse0 == button['signal']:
                l_text = self.b1.render('L', 1, button['invert'] if 'invert' in button else (255,255,255))
                self.screen.blit(l_text, ( 20 , button['pos']+5))
            if self.mouse1 == button['signal']:
                r_text = self.b1.render('R', 1, button['invert'] if 'invert' in button else (255,255,255))
                self.screen.blit(r_text, ( 113 , button['pos']+5))

    def inputs(self):
        mouse_pos = pygame.mouse.get_pos()

        # loops the events
        for event in pygame.event.get():
            #quitter
            if event.type == pygame.QUIT:
                self.running = False

            # checks if possible button press
            if (pygame.MOUSEBUTTONUP == event.type or event.type == pygame.MOUSEBUTTONDOWN) and (
                    event.button == 1 or event.button == 3) and (9 <= mouse_pos[0] <= 133):
                
                # loops buttons
                for button in self.buttons:
                    if not (button['pos'] <= mouse_pos[1] <= button['pos'] + 20): 
                        continue
                    
                    # changes mouse color
                    if 'color' in button:
                        if event.button == 1:
                            self.color0 = button['color']
                            self.mouse0 = button['signal']
                        else:
                            self.color1 = button['color']
                            self.mouse1 = button['signal']

                    # clears grid
                    elif button['signal'] == 'clear':
                        self.grid = {}

                    # saves data
                    elif button['signal'] == 'save': 
                        self.save()

                    # loads data
                    elif button['signal'] == 'load': 
                        self.load()

                    # adds eraser as tool
                    elif button['signal'] == 'eraser':
                        if event.button == 1:
                            self.color0 = False
                            self.mouse0 = button['signal']
                        else:
                            self.color1 = False
                            self.mouse1 = button['signal']
                    # fills background                            
                    elif button['signal'] == 'fill':
                        if event.button == 1:
                            self.fill(self.color0 or self.color1 or (0,0,0))
                        else:
                            self.fill(self.color1 or self.color0 or (0,0,0))

        # grid drawn 
        if 144 <= mouse_pos[0] <= 624 and 10 <= mouse_pos[1] <= 490:
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:
                if self.color0:
                    self.draw(mouse_pos, self.color0)
                else:
                    self.erase(mouse_pos)
            elif mouse_pressed[2]:
                if self.color1:
                    self.draw(mouse_pos, self.color1)
                else:
                    self.erase(mouse_pos)

    def load(self): # loads json to grid
        self.grid = {}
        with open('saves/image_data.json', 'r') as jsonSave:
            for pos, color in json.load(jsonSave).items():
                x, y = pos.split(':')
                self.grid[pos] = [pygame.rect.Rect(int(x) * 30, int(y) * 30, 30, 30), tuple(color)]

    def save(self): 
        savefile = {}

        # sets data up for json
        for i, v in self.grid.items():
            savefile[i] = v[1]

        # stores data as json
        with open('saves/image_data.json', 'w') as jsonSave:
            json.dump(savefile, jsonSave)

        # stores image as png
        pygame.image.save(pygame.transform.scale(self.grid_surface, (16, 16)), 'saves/image.png')

    def draw(self, mouse_pos=(0, 0), color=(255, 255, 255)):
        # gets mouse pos to grid pos
        base_x, base_y = (mouse_pos[0] - 144) // 30, (mouse_pos[1] - 10) // 30
        chunk = str(base_x) + ':' + str(base_y)

        if chunk in self.grid:

            # checks if color is the same
            chuck_color = self.grid[chunk][1]
            if chuck_color[0] != color[0] or chuck_color[1] != color[1] or chuck_color[2] != color[2]:

                # erases different color
                self.erase(chunk, True)

        # adds color to grid
        self.grid[chunk] = [pygame.rect.Rect(base_x * 30, base_y * 30, 30, 30), color]

    def erase(self, mouse_pos=(0, 0), chunk=False):

        # checks if mode is chunk
        if chunk and mouse_pos in self.grid:
            self.grid.pop(mouse_pos)
            return
        
        # otherwise turns pos to chunk
        chunk = str((mouse_pos[0] - 144) // 30) + ':' + str((mouse_pos[1] - 10) // 30)
        if chunk in self.grid: self.erase(chunk, True)
    
    def fill(self,color=(0,0,0)):
      # loops x and y of a 16x16 grid
      for y in range(16):
          for x in range(16):
              chunk = str(x)+':'+str(y)
              
              # checks if point exists or isn't a background color
              if chunk in self.grid:
                  
                  if not ('bgc' in self.grid[chunk]):
                      continue
                  self.erase(chunk, True)

              # draws point on grid
              self.grid[chunk] = [pygame.rect.Rect(x * 30, y * 30, 30, 30), color,'bgc']
                  

if __name__ == "__main__":
   pixel_drawer().run()



