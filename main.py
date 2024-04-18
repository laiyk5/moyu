import pandas as pd

from common.parse import get_info
from search_routine import search_routine_agoda
from tqdm import tqdm

# page_source = search_routine_agoda(query='new new')
# output1 = get_info(page_source)
# print(output1)

# page_source = search_routine_agoda(query='ace hotel')
# output2 = get_info(page_source)
# print(output2)


# df = pd.DataFrame([output1, output2])
# df.to_csv('out/output.csv', index=False) # make the "out" directly before you execute this code.

# print(output1)
# print(output2)


# 读取Excel文件并逐行搜索
def read_excel_and_search(file_path:str, column_name:str):
    # 读取Excel文件
    df=pd.read_excel(file_path)
    
    # 检查列名是否存在
    if column_name not in df.columns:
        print(f"列名 '{column_name}' 不存在.")
        return
    
    # 打印指定列的数据
    column_data = df[column_name]

    #逐行搜索
    output_list = []
    for query in tqdm(column_data):
        print("正在搜索：",query)
        try:
            page_src = search_routine_agoda(query)
            ret = get_info(page_src)
            output = {"query": query, "hotel_name": ret["hotel_name"], "number_of_reviews": ret["number_of_reviews"], "location": ret["location"]}
            print(ret.items() )
        except:
            output = {"query": query, "hotel_name": "Null", "number_of_reviews": "Null", "location": "Null"}
        
        output_list.append(output)
        print(output)
        
        df = pd.DataFrame(output_list)
        df.to_csv('out/output.csv', index=False)
        
    
#指定Excel文件路径和要读取的列名
excel_file = "D:/dev/scartch_data/data/酒店未匹配2.xlsx"
column_name = "hotel_en_name"

read_excel_and_search(excel_file,column_name)