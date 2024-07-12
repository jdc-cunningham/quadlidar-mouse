import VL53L0X

from threading import Thread

class ToF():
  def __init__(self, shutdown_pin):
    