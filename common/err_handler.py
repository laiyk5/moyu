from time import sleep

class ErrHandler:
  '''
  Handle the err situation by manipulating index.
  
  - When in failure situation, call the `fail' routine;
  - when in sucess situation, call the `succeed' routine.
  
  If fail, retry and sleep with exponentially increasing time.
  If success, advance the index.
  '''
  PATIENCE = 5
  SLEEP_BASE_IN_SECONDS = 10
  block_flag = False
  block_count = 0
  sleep_multiplier = 1
  
  index = 0
  
  def succeed(self):
    if self.block_flag:
      self._reset()
    self.index += 1
    
  def fail(self):
    self.block_flag = True
    self.block_count += 1
    
    if self.block_count <= self.PATIENCE:
      # give up
      sleep(self.sleep_multiplier * self.SLEEP_BASE_IN_SECONDS)
      self.sleep_multiplier *= 2
    else:
      self._reset()
      self.index += 1
      
  def get_index(self):
    return self.index
  
  def _reset(self):
    self.block_count = 0
    self.sleep_multiplier = 0