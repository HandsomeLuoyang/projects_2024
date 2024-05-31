import pandas as pd
import re

mitm = pd.read_csv('mitm.csv')

houyi = pd.read_csv('houyi.csv')



mitm = mitm.drop_duplicates()
# houyi = houyi.drop_duplicates()
# print(houyi.duplicated())

hebing = houyi.merge(mitm, on='name')
hebing = hebing.sort_values(by='url')
hebing = hebing.fillna('暂无信息')


# print(mitm)
# print(houyi)
print(hebing)
hebing.to_csv('hebing.csv', index=None)




# hebing = pd.read_csv('hebing.csv')
# for i in range(len(hebing)):
#     if not pd.isna(hebing.iloc[i, 8]):
#         print(hebing.iloc[i, 8])
#         num = re.search(r'(\d+)间', hebing.iloc[i, 8])
#         if num:
#             print(num.group(1))
#         # hebing.iloc[i, 8] = num
# print(hebing)