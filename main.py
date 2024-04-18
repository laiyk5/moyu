import pandas as pd

from common.parse import get_info
from search_routine import search_routine_agoda
from tqdm import tqdm

from selenium import webdriver

from common.utils import sleep_randomly


excel_file = r"./data/酒店未匹配2.xlsx"
column_name = "hotel_en_name"
df=pd.read_excel(excel_file)

driver = webdriver.Chrome()

# 检查列名是否存在
if column_name not in df.columns:
  raise RuntimeError(f"列名 '{column_name}' 不存在.")

# 打印指定列的数据
column_data = df[column_name]

#逐行搜索
output_list = []
for query in tqdm(column_data):
  print("正在搜索：",query)
  try:
    page_src = search_routine_agoda(driver, query)
    ret = get_info(page_src)
    output = {"query": query, "hotel_name": ret["hotel_name"], "number_of_reviews": ret["number_of_reviews"], "location": ret["location"]}
    print(ret.items() )
  except:
    output = {"query": query, "hotel_name": "Null", "number_of_reviews": "Null", "location": "Null"}
  
  output_list.append(output)
  print(output)
  
  df = pd.DataFrame(output_list)
  df.to_csv('out/output.csv', index=False)
  
  sleep_randomly(2, 2) # 防止操作太快浏览器反应不过来
  
driver.quit()