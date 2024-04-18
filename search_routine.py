from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from common.utils import sleep_randomly

def wait_and_find_element_by_xpath(driver:WebDriver, xpath:str, timeout:float=15, timeout_message='Time out')->WebElement:
  try:
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
  except:
    raise RuntimeError("timeout_message")
  return driver.find_element(by=By.XPATH, value=xpath)

def search_routine_agoda(query:str)->str:
  '''
  :param query: The string you want to put in the search bar.
  :return: The page source of the resulting page.
  '''
  driver = webdriver.Chrome()

  driver.get("https://www.agoda.com/")

  # 定位搜索框并输入搜索关键词
  try:
    search_box = wait_and_find_element_by_xpath(driver, r'//*[@id="textInput"]')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
  except:
    driver.quit()
    raise RuntimeError("Execution Failed.")
    
  sleep_randomly(1, 1)
    
  # 点击搜索栏推荐的第一个信息
  try:
    first_recommendation = wait_and_find_element_by_xpath(driver, r'//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[5]/div/div/ul/li[1]')
    first_recommendation.click()
  except:
    driver.quit()
    raise RuntimeError("Execution Failed.")
  
  sleep_randomly(1, 1)

  # 随便选一个元素点一下跳出UI才能点击搜索按钮
  try:
    elem = wait_and_find_element_by_xpath(driver, r'//*[@id="check-in-box"]')
    elem.click()
  except:
    driver.quit()
    raise RuntimeError("Execution Failed.")
  
  sleep_randomly(1, 1)

  # 点击搜索按钮
  try:
    button = wait_and_find_element_by_xpath(driver, r'//*[@id="Tabs-Container"]/button')
    button.click()
  except:
    driver.quit()
    raise RuntimeError("Execution Failed.")
  
  # 应对可能的页面跳转
  driver.switch_to.window(driver.window_handles[-1])
  
  try:
    first_hotel = wait_and_find_element_by_xpath(driver, r'//*[@id="contentContainer"]//*/h3')
    first_hotel.click()
  except:
    driver.quit()
    raise RuntimeError("Execution Failed.")

  # 点击第一个酒店信息
  
  sleep_randomly(1, 1)

  driver.switch_to.window(driver.window_handles[-1])
  
  try:
    _ = wait_and_find_element_by_xpath(driver, r'//*[@id="abouthotel-panel"]')
  except:
    driver.quit()
    raise RuntimeError("酒店详情加载超时")

  page_source = driver.page_source

  # 关闭浏览器
  driver.quit()

  return page_source
