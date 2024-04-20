import json

import datetime
import os

ROOT = 'out'
TASKS_ROOT = f'{ROOT}/tasks'
PROJECT_STATE_PATH = f'{ROOT}/project_state.json'

class StateField:
  START_DATETIME = 'start datetime'
  MILESTONES = 'milestones'
  NUMBER_OF_TASKS = 'number of tasks'

class ProjectHandler:
  
  def __init__(self):
    if not os.path.exists(PROJECT_STATE_PATH):
      self.init_project()
    self.__state__ = self.__load_project_state__()
      
  
  def __init_project_state__(self):
    return {\
      StateField.START_DATETIME: datetime.datetime.now().strftime("%d/%m/%Y,%H:%M:%S"), \
      StateField.MILESTONES: [], \
      StateField.NUMBER_OF_TASKS: 0, \
      }
    
  def init_project(self):
    os.makedirs(ROOT)
    os.makedirs(TASKS_ROOT)
    with open(PROJECT_STATE_PATH, 'w') as file:
      self.__state__ = self.__init_project_state__()
      json.dump(self.__state__, file, indent=2)
    
  def __load_project_state__(self):
    state = None
    with open(PROJECT_STATE_PATH) as file:
      state = json.load(file)
    return state
  
  def __update_project_state__(self, key, value):
    self.__state__[key] = value
    with open(PROJECT_STATE_PATH, 'w') as file:
      json.dump(self.__state__, file, indent=2)
    
  def get_task_path(self, task_id):
    now = datetime.datetime.now()
    path = ['out', f'{now.year}', f'{now.month}', f'{now.day}', f'{now.hour}', f'{task_id:0>7}']
    path_str = '/'.join(path)
    return path_str
  
  def new_task(self)->int:
    '''
    update the project information and create the task directory.
    
    :returns: the new task id
    '''
    task_id = self.__state__[StateField.NUMBER_OF_TASKS] + 1
    out_dir = self.get_task_path(task_id)
    os.makedirs(out_dir)
    self.__update_project_state__(StateField.NUMBER_OF_TASKS, task_id)
    return task_id
  