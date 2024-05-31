import requests
import pandas as pd
import re
import time
import csv


hebing = pd.read_csv('hebing.csv')
hebing['rooms'] = [0] * len(hebing)


for i in range(len(hebing)):
    try:
        print(hebing.iloc[i, 1])
        r = requests.get(url=hebing.iloc[i, 1])
        r1 = re.search(r'(\d+)间房', r.content.decode('utf8'))
        if not r1:
            num = '暂无信息'
        else:
            num = r1.group(1)
        hebing.iloc[i, 7] = num
        print(hebing.iloc[i, 7])
    except Exception as e:
        print(e)

print(hebing)
hebing.to_csv('hebing2.csv', index=None)