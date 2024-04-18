import random
import time

def sleep_randomly(random_duration:float, offset:float=0):
  time.sleep(offset + random.random() * random_duration)