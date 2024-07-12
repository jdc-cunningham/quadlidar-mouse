import os
import pyautogui

os.environ['DISPLAY'] = ':0'

pyautogui.FAILSAFE = False

# here because of tuple
screen_width, screen_height = pyautogui.size()

class MouseEvents():
  def __init__(self):
    self.mouse_x = 50 # start near top left
    self.mouse_y = 50
    self.mouse_increment = 1
    self.screen_width = screen_width
    self.screen_height = screen_height

    pyautogui.moveTo(self.mouse_x, self.mouse_y)

  def move_mouse(self, dir):
    if (dir == 'up'):
      if (self.mouse_y > self.mouse_increment):
        self.mouse_y = self.mouse_y - self.mouse_increment

        if (self.mouse_y > self.mouse_increment):
          pyautogui.moveTo(self.mouse_x, self.mouse_y)

    if (dir == 'down'):
      if (self.mouse_y < self.screen_height):
        self.mouse_y = self.mouse_y + self.mouse_increment

        if (self.mouse_y < self.screen_height):
          pyautogui.moveTo(self.mouse_x, self.mouse_y)

    if (dir == 'left'):
      if (self.mouse_x < self.screen_width):
        self.mouse_x = self.mouse_x + self.mouse_increment

        if (self.mouse_x < self.screen_width):
          pyautogui.moveTo(self.mouse_x, self.mouse_y)

    if (dir == 'right'):
      if (self.mouse_x > self.mouse_increment):
        self.mouse_x = self.mouse_x - self.mouse_increment

      if (self.mouse_x > 0):
        pyautogui.moveTo(self.mouse_x, self.mouse_y)

  def left_click(self):
    pyautogui.click()
  
  def right_click(self):
    pyautogui.click(button='right')
  