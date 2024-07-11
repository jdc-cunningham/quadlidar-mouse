import os

# set display for pyautogui
os.environ['DISPLAY'] = ':0'

import time
import VL53L0X
import RPi.GPIO as GPIO
import pyautogui

from threading import Thread

TOF_TL_SD_PIN = 22
TOF_TR_SD_PIN = 17
TOF_RT_SD_PIN = 27
TOF_RB_SD_PIN = 10
LED_PIN = 9
TRACKPAD_TOGGLE_PIN = 26
LEFT_CLICK_PIN = 6
RIGHT_CLICK_PIN = 5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

tof_tl = None
tof_tr = None
tof_st = None
tof_sb = None

pyautogui.moveTo(300, 300)

screen_width, screen_height = pyautogui.size()
mouse_x, mouse_y = pyautogui.position()

pyautogui.FAILSAFE = False
trackpad_on = False
mouse_increment = 50

def led_on():
  GPIO.output(LED_PIN, GPIO.HIGH)

def led_off():
  GPIO.output(LED_PIN, GPIO.LOW)

led_off()

def setup_tof_sensors():
  global tof_tl, tof_tr, tof_st, tof_sb

  GPIO.setup(TOF_TL_SD_PIN, GPIO.OUT)
  GPIO.setup(TOF_TR_SD_PIN, GPIO.OUT)
  GPIO.setup(TOF_RT_SD_PIN, GPIO.OUT)
  GPIO.setup(TOF_RB_SD_PIN, GPIO.OUT)

  GPIO.output(TOF_TL_SD_PIN, GPIO.LOW)
  GPIO.output(TOF_TR_SD_PIN, GPIO.LOW)
  GPIO.output(TOF_RT_SD_PIN, GPIO.LOW)
  GPIO.output(TOF_RB_SD_PIN, GPIO.LOW)

  time.sleep(0.50)

  tof_tl = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
  tof_tr = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
  tof_st = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
  tof_sb = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)

  GPIO.output(TOF_TL_SD_PIN, GPIO.HIGH)
  time.sleep(1)
  tof_tl.change_address(0x2B)

  GPIO.output(TOF_TR_SD_PIN, GPIO.HIGH)
  time.sleep(1)
  tof_tr.change_address(0x2D)

  GPIO.output(TOF_RT_SD_PIN, GPIO.HIGH)
  time.sleep(1)
  tof_st.change_address(0x2F)

  GPIO.output(TOF_RB_SD_PIN, GPIO.HIGH)
  time.sleep(1)
  tof_sb.change_address(0x2E)

  tof_tl.open()
  time.sleep(0.50)
  tof_tl.start_ranging(VL53L0X.Vl53l0xAccuracyMode.HIGH_SPEED)

  tof_tr.open()
  time.sleep(0.50)
  tof_tr.start_ranging(VL53L0X.Vl53l0xAccuracyMode.HIGH_SPEED)

  tof_st.open()
  time.sleep(0.50)
  tof_st.start_ranging(VL53L0X.Vl53l0xAccuracyMode.HIGH_SPEED)

  tof_sb.open()
  time.sleep(0.50)
  tof_sb.start_ranging(VL53L0X.Vl53l0xAccuracyMode.HIGH_SPEED)

setup_tof_sensors()

def setup_buttons():
  GPIO.setup(TRACKPAD_TOGGLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(LEFT_CLICK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(RIGHT_CLICK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

setup_buttons()

last_on = 0

def listen_buttons(trackpad_on, last_on):
  while True:
    if GPIO.input(TRACKPAD_TOGGLE_PIN) == GPIO.HIGH:
      print('trackpad')
      # print('since click ' + str(time.time() - last_on))
      # if (last_on == 0):
      #   last_on = time.time()
      # elif (time.time() - last_on < 200):
      #   continue

      # trackpad_on = not trackpad_on
      
      # if (trackpad_on):
      #   led_on()
      # else:
      #   led_off()

    if GPIO.input(LEFT_CLICK_PIN) == GPIO.HIGH:
      pyautogui.click()

    if GPIO.input(RIGHT_CLICK_PIN) == GPIO.HIGH:
      pyautogui.click(button='right')

    time.sleep(0.1)

Thread(target=listen_buttons, args=(trackpad_on, last_on)).start()

def to_in(cm):
  return cm * 0.393701

# distance should be under this to consider a hit
trackpad_max = 6

# sample 10
d1_a = []
d2_a = []
d3_a = []
d4_a = []

def avg(arr):
  return sum(arr) / len(arr)

def move_mouse(dir):
  global mouse_x, mouse_y

  if (dir == 'up'):
    if (mouse_y > mouse_increment):
      mouse_y = mouse_y - mouse_increment

      if (mouse_y > mouse_increment):
        pyautogui.moveTo(mouse_x, mouse_y)

  if (dir == 'down'):
    if (mouse_y < screen_height):
      mouse_y = mouse_y + mouse_increment

      if (mouse_y < screen_height):
        pyautogui.moveTo(mouse_x, mouse_y)

  if (dir == 'left'):
    if (mouse_x < screen_width):
      mouse_x = mouse_x + mouse_increment

      if (mouse_x < screen_width):
        pyautogui.moveTo(mouse_x, mouse_y)

  if (dir == 'right'):
    if (mouse_x > mouse_increment):
      mouse_x = mouse_x - mouse_increment

      if (mouse_x > 0):
        pyautogui.moveTo(mouse_x, mouse_y)

def check_mouse_dir():
  d1a = avg(d1_a)
  d2a = avg(d2_a)
  d3a = avg(d3_a)
  d4a = avg(d4_a)

  if (d1a > 0 and d1a < trackpad_max):
    move_mouse('right')
  
  if (d2a > 0 and d2a < trackpad_max):
    move_mouse('left')

  if (d3a > 0 and d3a < trackpad_max):
    move_mouse('up')
  
  if (d4a > 0 and d4a < trackpad_max):
    move_mouse('down')

while True:
  d1 = round(to_in(tof_tl.get_distance() / 10), 2)
  d2 = round(to_in(tof_tr.get_distance() / 10), 2)
  d3 = round(to_in(tof_st.get_distance() / 10), 2)
  d4 = round(to_in(tof_sb.get_distance() / 10), 2)

  if (len(d1_a) < 3):
    d1_a.append(d1)
    d2_a.append(d2)
    d3_a.append(d3)
    d4_a.append(d4)
  else:
    d1_a.pop(0)
    d2_a.pop(0)
    d3_a.pop(0)
    d4_a.pop(0)

    d1_a.append(d1)
    d2_a.append(d2)
    d3_a.append(d3)
    d4_a.append(d4)

    check_mouse_dir()

  # print(str(d1) + ', ' + str(d2) + ', ' + str(d3) + ', ' + str(d4))
