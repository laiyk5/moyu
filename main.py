import pandas as pd

from common.parse import get_info
from search_routine import search_routine_agoda


page_source = search_routine_agoda(query='new new')
output1 = get_info(page_source)

page_source = search_routine_agoda(query='ace hotel')
output2 = get_info(page_source)

df = pd.DataFrame([output1, output2])
df.to_csv('out/output.csv', index=False) # make the "out" directly before you execute this code.

print(output1)
print(output2)