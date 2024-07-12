import time
import VL53L0X
import RPi.GPIO as GPIO

from threading import Thread

class ToF():
  def __init__(self, shutdown_pin, address):
    self.max_range = 6 # inches
    self.tof = None
    self.SD_PIN = shutdown_pin
    self.address = address
    self.range = 0

  def set_low(self):
    GPIO.setup(self.SD_PIN, GPIO.OUT)
    GPIO.output(self.SD_PIN, GPIO.LOW)

  def setup(self):
    self.tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
    GPIO.output(self.SD_PIN, GPIO.HIGH)
    time.sleep(1)
    self.tof.change_address(self.address)

    self.tof.open()
    time.sleep(0.50)
    self.tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.HIGH_SPEED)

  def listen(self):
    while True:
      # limited by 20ms sampling speed
      self.range = round(self.to_in(self.tof.get_distance() / 10), 2)

  def start(self):
    Thread(target=self.listen).start()

  def avg(self, arr):
    return sum(arr) / len(arr)

  def to_in(self, cm):
    return cm * 0.393701
