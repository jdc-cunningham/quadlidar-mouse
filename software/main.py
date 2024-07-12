import RPi.GPIO as GPIO
class QLTP_Mouse():
  def __init__(self):
    self.TOF_TL_SD_PIN = 22
    self.TOF_TR_SD_PIN = 17
    self.TOF_RT_SD_PIN = 27
    self.TOF_RB_SD_PIN = 10