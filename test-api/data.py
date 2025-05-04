import math

class ToskrData:
  def __init__(self):
    self.speed = 0.0
    self.battery = 1.0
    self.status = 0

  def generate_speed(self, time):
    # return a sine wave function for speed
    if self.status == 1:
      self.speed = 0.0
    elif self.status == 2:
      self.speed = round(5 * math.sin(2*time) + 50 + math.sin(0.5*time), 2)
    elif self.status == 0:
      self.speed = round(5 * math.sin(2*time) + 50 + math.sin(0.5*time), 2)
    return self.speed
  
  def generate_battery(self, time):
    # return a sine wave function for battery with 2 decimal places
    self.battery = round(0.2 * math.sin(0.1*time) + 0.5, 2)
    return self.battery
  
  def setStatus(self, status):
    self.status = status
    return self.status
  
  def setSpeed(self, speed):
    self.speed = speed
    return self.speed
  
  def setBattery(self, battery):
    self.battery = battery
    return self.battery
  
  def getData(self, time):
    self.generate_speed(time)
    self.generate_battery(time)
    return {
      "speed": self.speed,
      "battery": self.battery,
      "status": self.status
    }
  
class Task:
  def __init__(self):
    self.id = 0
    self.name = ""
    self.start = ""
    self.end = ""
    self.status = 0 # 0: not started, 1: in progress, 2: completed
    self.priority = 0

  def __init__(self, id, name, start, end, priority=0):
    self.id = id
    self.name = name
    self.start = start
    self.end = end
    self.status = 0
    self.priority = priority

  def setStatus(self, status):
    self.status = status
    return self.status
  
  def getStatus(self):
    return self.status
  
  def getTask(self):
    return {
      "id": self.id,
      "name": self.name,
      "start": self.start,
      "end": self.end,
      "status": self.status
    }
  
class TaskList:
  def __init__(self):
    self.tasks = []

  def __init__(self, tasks=[]):
    self.tasks = tasks

  def addTask(self, task):
    self.tasks.append(task)
    return self.tasks
  
  def removeTask(self, id):
    for i, task in enumerate(self.tasks):
      if task.id == id:
        del self.tasks[i]
        return self.tasks
    return None
  
  def updateTaskStatus(self, id, status):
    for i, task in enumerate(self.tasks):
      if task.id == id:
        if status == 2:
          self.removeTask(id)
        else:
          self.tasks[i].setStatus(status)
        return self.tasks
    return None
  
  def getTasks(self):
    return [task.getTask() for task in self.tasks]

class MapData:
  def __init__(self):
    # generate a 64x64 map with 0
    self.map = [
      [0 for _ in range(64)] for _ in range(64)
    ]
    self.position = {
      "x": 0,
      "y": 0
    } # x, y

  def __init__(self, map=None, position={
    "x": 0,
    "y": 0
  }):
    if map is not None:
      self.map = map
    else:
      self.map = [
        [0 for _ in range(64)] for _ in range(64)
      ]
    self.position = position

  def setPosition(self, x, y):
    self.position = {
      "x": x,
      "y": y
    }
    return self.position
  
  def getPosition(self):
    return self.position
  
  def getMap(self):
    return self.map