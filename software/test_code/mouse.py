# run mouse directly with python
# https://stackoverflow.com/a/27046948/2710227

import os

os.environ['DISPLAY'] = ':0'

import pyautogui

pyautogui.moveTo(100, 150)

# yeah this works
