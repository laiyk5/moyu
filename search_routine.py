from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

def search_routine_agoda(query:str)->str:
  '''
  :param query: The string you want to put in the search bar.
  :return: The page source of the resulting page.
  '''
  driver = webdriver.Chrome()

  driver.get("https://www.agoda.com/")

  # 定位搜索框并输入搜索关键词
  search_box = driver.find_element(by=By.XPATH, value=r'//*[@id="textInput"]')
  search_box.send_keys(query)
  search_box.send_keys(Keys.RETURN)

  # 等待搜索结果加载
  try:
      WebDriverWait(driver, 100).until(
          EC.presence_of_element_located((By.XPATH, r'//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[5]/div/div/ul/li[1]'))
      )
  except:
      print("搜索结果加载超时")
      driver.quit()

      raise RuntimeError("搜索结果加载超时")
      
  time.sleep(2)

  # 点击搜索栏推荐的第一个信息
  first_recommendation = driver.find_element(By.XPATH, r'//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[5]/div/div/ul/li[1]')
  first_recommendation.click()

  # 随便选一个元素点一下跳出UI才能点击搜索按钮
  elem = driver.find_element(By.XPATH, r'//*[@id="check-in-box"]')
  elem.click()

  # 点击搜索按钮
  button = driver.find_element(By.XPATH, r'//*[@id="Tabs-Container"]/button')
  button.click()

  driver.switch_to.window(driver.window_handles[-1])
  try:
      WebDriverWait(driver, 100).until(
          EC.presence_of_element_located((By.XPATH, r'//*[@id="contentContainer"]'))
      )
  except:
      print("搜索结果加载超时")
      driver.quit()
      raise RuntimeError("搜索结果加载超时")

  # 点击第一个酒店信息
  first_hotel = driver.find_element(By.XPATH, r'//*[@id="contentContainer"]//*/h3')
  first_hotel.click()

  driver.switch_to.window(driver.window_handles[-1])

  time.sleep(5)

  page_source = driver.page_source

  # 关闭浏览器
  driver.quit()

  return page_source
