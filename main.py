import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import random

from common.parse import get_info
from search_routine import search_routine_agoda, search_routine_agoda_2

from common.utils import sleep_randomly
from common.err_handler import ErrHandler

from tqdm import tqdm


excel_file = r"./data/酒店未匹配2.xlsx"
column_name = "hotel_en_name"
df=pd.read_excel(excel_file)

# 检查列名是否存在
if column_name not in df.columns:
  raise RuntimeError(f"列名 '{column_name}' 不存在.")

# 打印指定列的数据
column_data = df[column_name]

def initialize_driver():
  exp_multiplier = 1
  patience = 2
  is_success = False
  while not is_success:
    try:
      driver = webdriver.Chrome()
      driver.get('https://www.agoda.com/')
      page_src = search_routine_agoda(driver, 'good')
      _ = get_info(page_src)
      is_success = True
    except:
      driver.close()
      if patience <= 0:
        raise RuntimeError("Failed to open the browser.")
      else:
        patience -= 1
        sleep_randomly(0, 60 * exp_multiplier)
        exp_multiplier *= 2
  return driver

#逐行搜索
output_list = []
handler = ErrHandler()
driver = initialize_driver()
index = handler.get_index()

pbar = tqdm(total=len(column_data))
while index < len(column_data):
  query = column_data[index]
  print("正在搜索：",query)
  try:
    page_src = ''
    if random.randint(0, 30) == 0:
      page_src = search_routine_agoda(driver, query)
    else:
      page_src = search_routine_agoda_2(driver, query)
    ret = get_info(page_src)
    output = {"query": query, "hotel_name": ret["hotel_name"], "number_of_reviews": ret["number_of_reviews"], "location": ret["location"]}
    print(ret.items() )
    
    handler.succeed()
    pbar.update(1)
  except:
    output = {"query": query, "hotel_name": "err", "number_of_reviews": "err", "location": "err"}
  
    handler.fail()
    
    # restart driver.
    driver.quit()
    driver = initialize_driver()
  
  if index < len(output_list):
    output_list[index] = output
  else:
    output_list.append(output)
  print(output)
  
  df = pd.DataFrame(output_list)
  df.to_csv('out/output.csv', index=False)
  
  sleep_randomly(2, 2) # 防止操作太快浏览器反应不过来
    
  # restart driver.
  if random.randint(0, 25) == 0:
    driver.quit()
    driver = initialize_driver()
    
  index = handler.get_index()
pbar.close()

driver.quit()