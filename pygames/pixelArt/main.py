import json
import pygame

class pixel_drawer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((634, 500))
        pygame.display.set_caption('pixel draw')
        self.clock = pygame.time.Clock()
        self.running = True

        self.grid_surface = pygame.surface.Surface((480, 480))
        self.grid_surface = self.grid_surface.convert_alpha()

        self.grid = {}

        self.grid_background = pygame.surface.Surface((480, 480))

        self.color0 = (255, 0, 0)
        self.color1 = (0, 0, 255)

        self.mouse0 = 'red'
        self.mouse1 = 'blue'

        self.buttons = [
            {'pos': 15, 'signal': 'clear'},
            {'pos': 40, 'signal':'fill', 'border':(255,255,255)},

            {'pos': 105, 'signal': 'orange', 'color': (255, 165, 0)},
            {'pos': 135, 'signal': 'red', 'color': (255, 0, 0)},
            {'pos': 165, 'signal': 'violet', 'color': (238, 130, 238)},
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

        corner_radius = 2

        for index in range(len(self.buttons)):
            val = self.buttons[index]
            radius = min(20 / 2, 124 / 2, corner_radius)
            offset0_x, offset0_y = (9 + radius, val['pos']), (9, val['pos'] + radius)
            offset1_x, offset1_y = (133 - radius, val['pos']), (133, val['pos'] + radius)
            offset2_x, offset2_y = (9 + radius, val['pos'] + 20), (9, val['pos'] + 20 - radius)
            offset3_x, offset3_y = (133 - radius, val['pos'] + 20), (133, val['pos'] + 20 - radius)

            color = val['color'] if 'color' in val else (255, 0, 0)
            if 'border' in val: color = val['border']

            geometry = [[offset0_y, offset0_x, offset1_x, offset1_y, offset3_y, offset3_x, offset2_x, offset2_y], color,
                        not 'color' in val]
            self.buttons[index]['geometry'] = geometry

        self.b1 = pygame.font.Font(None, 16)

    def run(self):
        self.render()
        while self.running:
            self.inputs()
            self.render()

            pygame.display.update()
            self.screen.blit(self.grid_surface, (144, 10))

            self.clock.tick(60)

    def render(self):
        self.screen.fill((20, 20, 20))

        self.grid_background.fill((7, 7, 7))

        for section in range(15):
            pygame.draw.line(self.grid_background, (20, 20, 20), (0, (section + 1) * 30), (480, (section + 1) * 30), 2)
            pygame.draw.line(self.grid_background, (20, 20, 20), ((section + 1) * 30, 0), ((section + 1) * 30, 480), 2)
        self.screen.blit(self.grid_background, (144, 10))

        self.grid_surface.fill(pygame.color.Color(0, 0, 0, 0))
        for val in self.grid.values():
            pygame.draw.rect(self.grid_surface, val[1], val[0])
        for button in self.buttons:
            button_geometry = button['geometry']
            if not button_geometry: continue
            if button_geometry[2]:
                pygame.draw.polygon(self.screen, button_geometry[1], button_geometry[0], 1)
                render = self.b1.render(button['signal'], 1, button_geometry[1])
                size = render.get_size()
                self.screen.blit(render, ( 71-size[0]/2 , button['pos']+size[1]/2))
            else:
                pygame.draw.polygon(self.screen, button_geometry[1], button_geometry[0])

            if self.mouse0 == button['signal']:
                l_text = self.b1.render('L', 1, button['invert'] if 'invert' in button else (255,255,255))
                self.screen.blit(l_text, ( 20 , button['pos']+5))
            if self.mouse1 == button['signal']:
                r_text = self.b1.render('R', 1, button['invert'] if 'invert' in button else (255,255,255))
                self.screen.blit(r_text, ( 113 , button['pos']+5))

        self.screen.blit(self.grid_surface, (144, 10))

    def inputs(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (pygame.MOUSEBUTTONUP == event.type or event.type == pygame.MOUSEBUTTONDOWN) and (
                    event.button == 1 or event.button == 3) and (9 <= mouse_pos[0] <= 133):
                for button in self.buttons:

                    if button['pos'] <= mouse_pos[1] <= button['pos'] + 20:
                        if 'color' in button:
                            if event.button == 1:
                                self.color0 = button['color']
                                self.mouse0 = button['signal']
                            else:
                                self.color1 = button['color']
                                self.mouse1 = button['signal']

                        elif button['signal'] == 'clear':
                            self.grid = {}

                        elif button['signal'] == 'save':
                            savefile = {}

                            for i, v in self.grid.items():
                                savefile[i] = v[1]

                            with open('saves/image_data.json', 'w') as jsonSave:
                                json.dump(savefile, jsonSave)
                            pygame.image.save(pygame.transform.scale(self.grid_surface, (16, 16)), 'saves/image.png')

                        elif button['signal'] == 'load':
                            self.grid = {}
                            with open('saves/image_data.json', 'r') as jsonSave:
                                for pos, color in json.load(jsonSave).items():
                                    x, y = pos.split(':')
                                    self.grid[pos] = [pygame.rect.Rect(int(x) * 30, int(y) * 30, 30, 30), tuple(color)]

                        elif button['signal'] == 'eraser':
                            if event.button == 1:
                                self.color0 = False
                                self.mouse0 = button['signal']
                            else:
                                self.color1 = False
                                self.mouse1 = button['signal']
                        elif button['signal'] == 'fill':
                            self.fill(self.color0 or self.color1 or (0,0,0))

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


    def draw(self, mouse_pos=(0, 0), color=(255, 255, 255)):
        base_x, base_y = (mouse_pos[0] - 144) // 30, (mouse_pos[1] - 10) // 30
        chunk = str(base_x) + ':' + str(base_y)
        if chunk in self.grid:
            chuck_color = self.grid[chunk][1]
            if chuck_color[0] != color[0] or chuck_color[1] != color[1] or chuck_color[2] != color[2]:
                self.erase(chunk, True)

        self.grid[chunk] = [pygame.rect.Rect(base_x * 30, base_y * 30, 30, 30), color]

    def erase(self, mouse_pos=(0, 0), chunk=False):
        if chunk and mouse_pos in self.grid:
            self.grid.pop(mouse_pos)
            return
        chunk = str((mouse_pos[0] - 144) // 30) + ':' + str((mouse_pos[1] - 10) // 30)
        if chunk in self.grid: self.erase(chunk, True)
    
    def fill(self,color=(0,0,0)):
      for y in range(16):
          for x in range(16):
              chunk = str(x)+':'+str(y)
              if chunk in self.grid:
                  if not ('bgc' in self.grid[chunk]):
                      continue
                  self.erase(chunk, True)
              
              self.grid[chunk] = [pygame.rect.Rect(x * 30, y * 30, 30, 30), color,'bgc']
                  


pixel_drawer().run()
