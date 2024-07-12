class Trackpad():
  def __init__(self, tof_sensors, main):
    self.tof_sensors = tof_sensors # array
    self.d1a = []
    self.d2a = []
    self.d3a = []
    self.d4a = []
    
    self.start_sensors()

  # dupe function from tof_sensor.py file
  def avg(self, arr):
    return sum(arr) / len(arr)

  def start_sensors(self):
    for tof in self.tof_sensors:
      tof.start()

  def update_mouse(self):
    d1a = self.avg(self.d1_a)
    d2a = self.avg(self.d2_a)
    d3a = self.avg(self.d3_a)
    d4a = self.avg(self.d4_a)

    if (d1a > 0 and d1a < self.tof_sensors[0].max_range):
      self.main.mouse_events.move_mouse('right')
    
    if (d2a > 0 and d2a < self.tof_sensors[1].max_range):
      self.main.mouse_events.move_mouse('left')

    if (d3a > 0 and d3a < self.tof_sensors[2].max_range):
      self.main.mouse_events.move_mouse('up')
    
    if (d4a > 0 and d4a < self.tof_sensors[3].max_range):
      self.main.mouse_events.move_mouse('down')

  def start(self):
    while True:
      if (len(self.d1_a) > 3):
        self.d1_a.pop(0)
        self.d2_a.pop(0)
        self.d3_a.pop(0)
        self.d4_a.pop(0)

      self.d1_a.append(self.tof_sensors[0].range) # order set in main.py
      self.d2_a.append(self.tof_sensors[1].range)
      self.d3_a.append(self.tof_sensors[2].range)
      self.d4_a.append(self.tof_sensors[3].range)

      self.update_mouse()