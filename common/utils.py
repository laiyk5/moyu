import random
import time

def sleep_randomly(random_duration:float, offset:float=0):
  time.sleep(offset + random.random() * random_duration)
  
def close_others(driver):
  curr = driver.current_window_handle
  for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if handle != curr:
      driver.close()