import pandas as pd

hb2 = pd.read_csv('hebing2.csv')

hb2 = hb2.drop('url', axis=1)

hb2.to_csv('data.csv', index=None, encoding='utf-8-sig')