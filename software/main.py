import time
import VL53L0X
import RPi.GPIO as GPIO

from threading import Thread

TOF_TL_SD_PIN = 22
TOF_TR_SD_PIN = 17
TOF_RT_SD_PIN = 27
TOF_RB_SD_PIN = 10

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

tof_tl = None
tof_tr = None
tof_st = None
tof_sb = None

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

def to_in(cm):
  return cm * 0.393701

while True:
  d1 = round(to_in(tof_tl.get_distance() / 10), 2)
  d2 = round(to_in(tof_tr.get_distance() / 10), 2)
  d3 = round(to_in(tof_st.get_distance() / 10), 2)
  d4 = round(to_in(tof_sb.get_distance() / 10), 2)

  print(str(d1) + ', ' + str(d2) + ', ' + str(d3) + ', ' + str(d4))

  time.sleep(0.1)
