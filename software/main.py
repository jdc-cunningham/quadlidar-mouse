import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

from tof_sensor.tof_sensor import ToF
from mouse_events.mouse_events import MouseEvents
from mouse_buttons.mouse_buttons import MouseButtons
from trackpad.trackpad import Trackpad

class QLTP_Mouse():
  def __init__(self):
    self.TOF_TL_SD_PIN = 22
    self.TOF_TR_SD_PIN = 17
    self.TOF_RT_SD_PIN = 27
    self.TOF_RB_SD_PIN = 10
    self.tof_tl = None
    self.tof_tr = None
    self.tof_rt = None
    self.tof_rb = None
    self.mouse_events = MouseEvents()
    self.mouse_buttons = MouseButtons(self.mouse_events)

    self.setup_tof_senors()
    self.start_mouse_btns()
    self.start_tof_sensors()

  def setup_tof_senors(self):
    self.tof_tl = ToF(self.TOF_TL_SD_PIN, 0x2B)
    self.tof_tr = ToF(self.TOF_TR_SD_PIN, 0x2D)
    self.tof_rt = ToF(self.TOF_RT_SD_PIN, 0x2F)
    self.tof_rb = ToF(self.TOF_RB_SD_PIN, 0x2E)
    
    self.tof_tl.set_low()
    self.tof_tr.set_low()
    self.tof_rt.set_low()
    self.tof_rb.set_low()

    time.sleep(0.5)

    self.tof_tl.setup()
    self.tof_tr.setup()
    self.tof_rt.setup()
    self.tof_rb.setup()

  def start_mouse_btns(self):
    self.mouse_buttons.start()

  def start_tof_sensors(self):
    self.trackpad = Trackpad([self.tof_tl, self.tof_tr, self.tof_rt, self.tof_rb], self)

QLTP_Mouse()
