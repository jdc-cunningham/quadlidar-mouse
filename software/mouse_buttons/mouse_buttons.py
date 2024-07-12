import time
import RPi.GPIO as GPIO

from threading import Thread

class MouseButtons():
  def __init__(self, mouse_events):
    self.TRACKPAD_TOGGLE_PIN = 26
    self.LEFT_CLICK_PIN = 6
    self.RIGHT_CLICK_PIN = 5
    self.LED_PIN = 9
    self.trackpad_on = False
    self.mouse_events = mouse_events

    self.setup()

  def setup(self):
    GPIO.setup(self.LED_PIN, GPIO.OUT)
    GPIO.setup(self.TRACKPAD_TOGGLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(self.LEFT_CLICK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(self.RIGHT_CLICK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  def led_on(self):
    GPIO.output(self.LED_PIN, GPIO.HIGH)

  def led_off(self):
    GPIO.output(self.LED_PIN, GPIO.LOW)

  def listen_buttons(self):
    while True:
      if GPIO.input(self.TRACKPAD_TOGGLE_PIN) == GPIO.HIGH:
        self.trackpad_on = not self.trackpad_on

        # state is flipped due to short on board
        # having trackpad on starts moving mouse suggesting fault on i2c sensor
        self.led_off() if self.trackpad_on else self.led_on()

      if GPIO.input(self.LEFT_CLICK_PIN) == GPIO.HIGH:
        self.mouse_events.left_click()

      if GPIO.input(self.RIGHT_CLICK_PIN) == GPIO.HIGH:
        self.mouse_events.right_click()

      time.sleep(0.15)

  def start(self):
    Thread(target=self.listen_buttons).start()
