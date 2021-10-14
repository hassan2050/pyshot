import os, time, math
import pygame, sys
from pygame.locals import *


BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 128)
RED = (255, 0, 0)

def blit_alpha(target, source, location, opacity):
  x = location[0]
  y = location[1]
  temp = pygame.Surface((source.get_width(), source.get_height())).convert()
  temp.blit(target, (-x, -y))
  temp.blit(source, (0, 0))
  temp.set_alpha(opacity)        
  target.blit(temp, location)

Rect = pygame.rect.Rect
def Point(x,y):
  return Rect(x,y,0,0)

class Sprite(pygame.sprite.DirtySprite):
  def __init__(self, app, g_rect):
    self.g_rect = g_rect
    super().__init__()
    self.app = app

  def update(self, viewport):
    self.rect = self.g_rect.copy()
    #self.update_image()

    r = pygame.sprite.RenderPlain(self)
    r.draw(viewport.surface)
    


  def update_image(self):
    pass
  
  def on_resize(self, event, old_size, new_size):
    pass

  def on_init(self):  pass
  def on_mousemotion(self, event, pos):  pass
  def on_keyup(self, event):  pass
  def on_keydown(self, event): pass
  def on_switch(self): pass
  def on_mousebuttonup(self, event, pos): pass
  def on_mousebuttondown(self, event, pos): pass
  
  def hide(self):
    self.visible = False
    self.dirty = True
    
  def show(self):
    self.visible = True
    self.dirty = True
    
class ImageSprite(Sprite):
  def __init__(self, app, g_rect, image):
    super().__init__(app, g_rect)
    if type(image) == type(""):
      self.image = pygame.image.load(image)
    else:
      self.image = image

    self.rect = self.g_rect.copy()
    self.rect.size = self.image.get_size()
    

class TextInput:
    """
    This class lets the user input a piece of text, e.g. a name or a message.
    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    """
    def __init__(self, x,y, width, height, func=None,
                     font_family = "",
                        font_size = 35,
                        antialias=True,
                        text_color=(0, 0, 0),
                        cursor_color=(0, 0, 1),
                        repeat_keys_initial_ms=400,
                        repeat_keys_interval_ms=35):
        """
        Args:
            font_family: Name or path of the font that should be used. Default is pygame-font
            font_size: Size of the font in pixels
            antialias: (bool) Determines if antialias is used on fonts or not
            text_color: Color of the text
            repeat_keys_initial_ms: ms until the keydowns get repeated when a key is not released
            repeat_keys_interval_ms: ms between to keydown-repeats if key is not released
        """

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.func = func
        
        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.input_string = "" # Inputted text
        if not os.path.isfile(font_family): font_family = pygame.font.match_font(font_family)
        self.font_object = pygame.font.Font(font_family, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {} # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size/20+1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = 0 # Inside text
        self.cursor_visible = True # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500 # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def on_keydown(self, event):
        self.cursor_visible = True # So the user sees where he writes

        # If none exist, create counter for that key:
        if not event.key in self.keyrepeat_counters:
            self.keyrepeat_counters[event.key] = [0, event.unicode]

        if event.key == K_BACKSPACE: # FIXME: Delete at beginning of line?
            self.input_string = self.input_string[:max(self.cursor_position - 1, 0)] + \
                                self.input_string[self.cursor_position:]

            # Subtract one from cursor_pos, but do not go below zero:
            self.cursor_position = max(self.cursor_position - 1, 0)
        elif event.key == K_DELETE:
            self.input_string = self.input_string[:self.cursor_position] + \
                                self.input_string[self.cursor_position + 1:]

        elif event.key == K_RETURN:
            if self.func: self.func(self.input_string)
            return True

        elif event.key == K_RIGHT:
            # Add one to cursor_pos, but do not exceed len(input_string)
            self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

        elif event.key == K_LEFT:
            # Subtract one from cursor_pos, but do not go below zero:
            self.cursor_position = max(self.cursor_position - 1, 0)

        elif event.key == K_END:
            self.cursor_position = len(self.input_string)

        elif event.key == K_HOME:
            self.cursor_position = 0

        else:
            # If no special key is pressed, add unicode of key to input_string
            self.input_string = self.input_string[:self.cursor_position] + \
                                event.unicode + \
                                self.input_string[self.cursor_position:]
            self.cursor_position += len(event.unicode) # Some are empty, e.g. K_UP
            
        self.on_update()

    def on_keyup(self, event):
        # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
        if event.key in self.keyrepeat_counters:
            del self.keyrepeat_counters[event.key]
            
        self.on_update()

    def on_update(self):
        # Update key counters:
        for key in self.keyrepeat_counters :
            self.keyrepeat_counters[key][0] += self.clock.get_time() # Update clock
            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = self.keyrepeat_intial_interval_ms - \
                                                    self.keyrepeat_interval_ms

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(KEYDOWN, key=event_key, unicode=event_unicode))

        # Rerender text surface:
        self.surface = self.font_object.render(self.input_string, self.antialias, self.text_color)

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
            self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

        self.clock.tick()
        return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def on_mousemotion(self, event, pos):
      pass

    def update(self, viewport):
      self.on_update()
      
      pygame.draw.rect(viewport.screen, WHITE, (self.x-5, self.y-5, self.width, self.height), 0)
      pygame.draw.rect(viewport.screen, BLACK, (self.x-5, self.y-5, self.width, self.height), 2)
      screen.blit(self.surface, (self.x, self.y))


class TextButton(Sprite):
    def __init__(self, app, g_rect, text, font_size=100, color=None, anchor="center", font_family="",
                 func=None, args=None, shiny_color=None):
        super().__init__(app, g_rect)
        if color is None: color = NORMAL
        self.image = None

        self.shiny_color = shiny_color
        self.normal_color = color
        
        self.font_size = font_size
        self.font_family = font_family
        if not font_family: font_family = app.font_family
        if not os.path.isfile(font_family): font_family = pygame.font.match_font(font_family)
        self.font = pygame.font.Font(font_family, font_size)

        self.size = 20
        self.text = text
        self.shiny = False

        self.func = func
        self.args = args
        self.anchor = anchor
        self.o_rect = self.g_rect.copy()

        self.rect = None
        
        self.set_text(text)

    def on_init(self):
      super().on_init()
      self.update_image()

    def update_image(self):
      bg = self.normal_color if not self.shiny else self.shiny_color

      self.image = self.font.render(self.text, True, BLACK, bg)
      tw,th = self.image.get_size()
      
      if self.anchor == "center":
        x = self.o_rect[0] - tw//2
        y = self.o_rect[1] - th//2
      else:
        x = self.o_rect[0]
        y = self.o_rect[1]
        
      self.g_rect = pygame.rect.Rect(x, y, tw, th)
      self.rect = self.g_rect.copy()

    def update(self, viewport):
      self.update_image()
      
    def set_text(self, text):
      self.text = text
      self.dirty = True
      self.on_init()

    def on_keyup(self, event):
      pass
    def on_keydown(self, event):
      pass

    def on_button(self, pos):
      return self.rect.collidepoint(pos)

    def set_shiny(self, shiny):
      if self.shiny != shiny:
        self.shiny = shiny
        self.dirty = True
        self.update_image()
      
    def on_mousebuttonup(self, event, pos):        
        self.set_shiny(False)

        if self.on_button(pos):
          if self.func:
            if self.args is None:
              self.func()
            else:
              self.func(self.args)

    def on_resize(self, event, old_size, new_size):
      pass

    def on_mousebuttondown(self, event, pos):
        if self.on_button(pos):
          self.set_shiny(True)
        else:
          self.set_shiny(False)

    def on_mousemotion(self, event, pos):
      pass

class Variable:
  def __init__(self, value=None):
    self._observers = []
    self.value = value

  def add_observer(self, observer, args=None):
    self._observers.append((observer, args))
    if args is not None:
      observer(self, args)
    else:
      observer(self)

  @property
  def value(self):
    return self._value
  
  @value.setter
  def value(self, value):
    self._value = value
    for (observer, args) in self._observers:
      if args is not None:
        observer(self, args)
      else:
        observer(self)

textAlignLeft = 0
textAlignRight = 1
textAlignCenter = 2
textAlignBlock = 3

def drawText(surface, text, color, rect, font, align=textAlignLeft, aa=False, bkg=None):
    lineSpacing = -2
    spaceWidth, fontHeight = font.size(" ")[0], font.size("Tg")[1]

    text = text.replace("\n", " \n ")
    listOfWords = text.split(" ")
    if bkg:
        imageList = [(word, font.render(word, 1, color, bkg)) for word in listOfWords]
        for image in imageList: image.set_colorkey(bkg)
    else:
        imageList = [(word, font.render(word, aa, color)) for word in listOfWords]

    maxLen = rect[2]
    lineLenList = [0]
    lineList = [[]]
    for word,image in imageList:
        if word == "\n":
          lineLenList.append(0)
          lineList.append([])
        else:
          width = image.get_width()
          lineLen = lineLenList[-1] + len(lineList[-1]) * spaceWidth + width
          if len(lineList[-1]) == 0 or lineLen <= maxLen:
              lineLenList[-1] += width
              lineList[-1].append(image)
          else:
              lineLenList.append(width)
              lineList.append([image])

    lineBottom = rect[1]
    lastLine = 0
    for lineLen, lineImages in zip(lineLenList, lineList):
        lineLeft = rect[0]
        if align == textAlignRight:
            lineLeft += + rect[2] - lineLen - spaceWidth * (len(lineImages)-1)
        elif align == textAlignCenter:
            lineLeft += (rect[2] - lineLen - spaceWidth * (len(lineImages)-1)) // 2
        elif align == textAlignBlock and len(lineImages) > 1:
            spaceWidth = (rect[2] - lineLen) // (len(lineImages)-1)
        if lineBottom + fontHeight > rect[1] + rect[3]:
            break
        lastLine += 1
        for i, image in enumerate(lineImages):
            x, y = lineLeft + i*spaceWidth, lineBottom
            surface.blit(image, (round(x), y))
            lineLeft += image.get_width() 
        lineBottom += fontHeight + lineSpacing

    if lastLine < len(lineList):
        drawWords = sum([len(lineList[i]) for i in range(lastLine)])
        remainingText = ""
        for text in listOfWords[drawWords:]: remainingText += text + " "
        return remainingText
    return ""
        
class Text(Sprite):
  def __init__(self, app, g_rect, text, font_size, color, anchor="center", font_family=""):
    super().__init__(app, g_rect)
    self.image = None

    self.font_size = font_size

    self.font_family = font_family
    if isinstance(font_family, pygame.font.Font):
      self.font = self.font_family
    else:
      self.font_family = font_family
      if not font_family: font_family = app.font_family
      if not os.path.isfile(font_family): font_family = pygame.font.match_font(font_family)
      self.font = pygame.font.Font(font_family, font_size)

    self.color = color
    self.anchor = anchor
    self.o_rect = g_rect.copy()
    self.set_text(text)

  def on_init(self):
    super().on_init()
    self.update_image()

  def update_image(self):
    self.image = pygame.Surface(self.o_rect.size)

    drawText(self.image, self.text, self.color, Rect((0,0), self.o_rect.size), self.font, textAlignCenter, True)
    #self.image = self.font.render(self.text, self.font_size, self.color)
    tw,th = self.image.get_size()

    if self.anchor == "center":
      x = self.o_rect[0] - tw//2
      y = self.o_rect[1] - th//2
    else:
      x = self.o_rect[0]
      y = self.o_rect[1]

    self.g_rect = pygame.rect.Rect(x, y, tw, th)
    self.rect = self.g_rect.copy()

    if 0:
      pygame.draw.rect(self.image, RED, Rect((0,0), self.rect.size), 2)

  def set_text(self, text):
    self.text = text
    
    self.dirty = True
    self.on_init()

class ImageButton(Sprite):
  def __init__(self, app, g_rect, image, func=None):
    super().__init__(app, g_rect)
    self.unselected_image = image
    self.image = image
    self.g_rect = g_rect
    self.func = func
    self.shiny = False

    self.selected_image = pygame.Surface(self.image.get_size())
    self.selected_image.blit(self.image, (0,0))
    border = 3
    pygame.draw.rect(self.selected_image, BLUE, (border+1,border+1,self.image.get_size()[0]-border*2,self.image.get_size()[1]-border*2), border*2)      

  def on_mousebuttondown(self, event, pos):
    self.shiny = True
    self.dirty = True
    self.image = self.selected_image

  def on_mousebuttonup(self, event, pos):
    self.shiny = False
    self.dirty = True
    self.image = self.unselected_image

  def update(self, viewport):
    super().update(viewport)
    return
    
class Screen:
    def __init__(self, app):
      self.app = app
      self.viewports = []
      self.viewports_dict = {}
      self.surface = None

      self.rect = pygame.rect.Rect(0, 0, self.app.window_width, self.app.window_height)
      self.view = Viewport(self, self.rect)
      
      self.viewports_dict['default'] = self.view
      self.viewports.append(self.view)

    def on_init(self):
      self.surface = self.app.display
      for viewport in self.viewports:
        viewport.on_init()

    def add_viewport(self, name, vp):
      self.viewports_dict[name] = vp
      self.viewports.append(vp)
        
    @property
    def window_width(self): return self.app.window_width
    @property
    def window_height(self): return self.app.window_height

    def update(self):
      for viewport in self.viewports:
        viewport.update()

    def redrawAll(self):
      for viewport in self.viewports:
        viewport.redrawAll()

    def draw(self):
      for viewport in self.viewports:
        viewport.draw()
        
    def on_resize(self, event, old_size, new_size):
      for viewport in self.viewports:
        viewport.on_resize(event, old_size, new_size)
      
    def on_keydown(self, event):
      for viewport in self.viewports:
        viewport.on_keydown(event)

    def on_keyup(self, event):
      for viewport in self.viewports:
        viewport.on_keyup(event)

    def on_switch(self):
      for viewport in self.viewports:
        viewport.on_switch()

    def on_mousemotion(self, event, pos):
      for viewport in self.viewports:
        viewport.on_mousemotion(event, pos)
        
    def on_mousebuttonup(self, event, pos):
      for viewport in self.viewports:
        viewport.on_mousebuttonup(event, pos)

    def on_mousebuttondown(self, event, pos):
      for viewport in self.viewports:
        viewport.on_mousebuttondown(event, pos)


class Viewport:
    def __init__(self, screen, origin):
      self.screen = screen
      self.origin = origin
      self.surface = None
      self.objects = pygame.sprite.LayeredDirty()
      self.mouse_down_objects = []

    def on_init(self):
      if self.screen:
        self.surface = self.screen.surface.subsurface(self.origin)
        
      for obj in self.objects:
        obj.on_init()

    def text(self, text, size, color, pos):
      label = self.screen.app.myfont.render(text, size, color)
      self.surface.blit(label, pos)
        
    def ctext(self, text, size, color, pos):
      label = self.screen.app.myfont.render(text, size, color)
      tw,th = label.get_size()
      self.surface.blit(label, (pos[0] - tw/2, pos[1] - th/2))

    def add(self, obj):
      self.objects.add(obj)

    def remove(self, obj):
      self.objects.remove(obj)
      
    def clear(self):
      self.objects = pygame.sprite.LayeredDirty()

    def update(self):
      for obj in self.objects:
        obj.update(self)

    def redrawAll(self):
      if not self.surface: return
      
      self.surface.fill(BLACK)
      
      for obj in self.objects: obj.dirty = True
      self.draw()

      pygame.display.update()

    def draw(self):
      self.objects.clear(self.surface, self.screen.app.background)

      rects = self.objects.draw(self.surface)
      rects = [rect.move(self.origin.left, self.origin.top) for rect in rects]
      pygame.display.update(rects)
      #pygame.display.update()

    def on_resize(self, event, old_size, new_size):
      for obj in self.objects:
        obj.on_resize(event, old_size, new_size)

    def on_keydown(self, event):
      for obj in self.objects:
        obj.on_keydown(event)

    def on_keyup(self, event):
      for obj in self.objects:
        obj.on_keyup(event)

    def on_switch(self):
        pass

    def on_mousemotion(self, event, pos):
      pos = (pos[0] - self.origin.left, pos[1] - self.origin.top)
      return
      for obj in self.objects:
        obj.on_mousemotion(event)

    def on_mousebuttonup(self, event, pos):
      pos = (pos[0] - self.origin.left, pos[1] - self.origin.top)
      if 0:
        for obj in self.objects:
          if obj.rect.collidepoint(pos):
            obj.on_mousebuttonup(event, pos)

      for obj in self.mouse_down_objects:
        obj.on_mousebuttonup(event, pos)
      self.mouse_down_objects = []

    def on_mousebuttondown(self, event, pos):
      pos = (pos[0] - self.origin.left, pos[1] - self.origin.top)

      self.mouse_down_objects = []
      for obj in self.objects:
        if obj.rect.collidepoint(pos):
          self.mouse_down_objects.append(obj)
          obj.on_mousebuttondown(event, pos)

class Timer:
  def __init__(self, when, func, args):
    self.when = when
    self.func = func
    self.args = args
    self.active = True

class App:
  def __init__(self):
    self._running = True

    self.window_size = (640,480)
    self.fps_clock = pygame.time.Clock()
    self.fps = 40
    self.screens = {}
    self.screen = None
    self.display = None
    self.font_family = None
    self.set_font_family("")

    self.timers = []
    
    self.mode = "setup"

  def set_font_family(self, font_family):
    self.font_family = font_family

  def on_init_fonts(self):
    self.myfont = pygame.font.SysFont(self.font_family, 20)

  def init_mixer(self):
    pygame.mixer.pre_init()
    pygame.mixer.init()
    
  def on_init(self):
    pygame.init()
    pygame.font.init()

    self.init_mixer()

    self.on_init_fonts()
    
    self.init_display()

    self.background = pygame.Surface(self.display.get_size())
    self.background = self.background.convert()
    self.background.fill(BLACK)

    for name, screen in self.screens.items():
      screen.on_init()

  def init_display(self):
    flags = HWSURFACE|DOUBLEBUF|RESIZABLE
    if self.fullscreen:
      flags = flags | FULLSCREEN
      
    self.display = pygame.display.set_mode(self.window_size, flags)

  def add_screen(self, name, screen):
    self.screens[name] = screen

  def set_screen(self, name):
    self.screen = self.screens[name]
    
    if self.mode != "running": return
    self.screen.on_switch()
    self.screen.redrawAll()

  @property
  def window_width(self): return self.window_size[0]
  @property
  def window_height(self): return self.window_size[1]

  def stop_running(self):
    self._running = False
    self.on_quit()

  def on_quit(self):
    pygame.quit()
    sys.exit()

  def on_resize(self, event):
    old_size = self.window_size
    self.window_size = event.dict['size']

    self.screen.on_resize(event, old_size, self.window_size)

    self.init_display()

  def setTimer(self, when, func, args):
    timer = Timer(when, func, args)
    self.timers.append(timer)
    return timer

  def removeTimer(self, timer):
    if timer in self.timers:
      self.timers.remove(timer)

  def run(self):
    self.mode = "init"
    self.on_init()

    self.mode = "running"
    if 1:
      self.screen.on_switch()
      self.screen.redrawAll()

    while self._running: #main game loop
      now = time.time()
      for timer in self.timers[:]:
        if now >= timer.when:
          timer.func(timer.args)
          timer.active = False
          try:
            self.timers.remove(timer)
          except ValueError: pass
      
      for event in pygame.event.get():
        if event.type == QUIT:
          self.stop_running()
          continue

        elif event.type == KEYDOWN:
          if event.key == 27: 
            self.stop_running()
            continue
            
          self.screen.on_keydown(event)
        elif event.type == KEYUP:
          self.screen.on_keyup(event)
        elif event.type == VIDEORESIZE:
          self.on_resize(event)
        elif event.type == pygame.MOUSEBUTTONUP:
          pos = pygame.mouse.get_pos()
          self.screen.on_mousebuttonup(event, pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
          pos = pygame.mouse.get_pos()
          self.screen.on_mousebuttondown(event, pos)
        elif event.type == MOUSEMOTION:
          pos = pygame.mouse.get_pos()
          self.screen.on_mousemotion(event, pos)

      self.screen.update()
      if 0:
        pygame.display.update()
        pygame.display.flip()

      self.screen.draw()

      self.fps_clock.tick(self.fps)

