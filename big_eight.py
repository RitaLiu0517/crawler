import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []
columns = []
r = requests.get('https://chart.capital.com.tw/Chart/TWII/TAIEX11.aspx')
if r.status_code == requests.codes.ok:
    soup = BeautifulSoup(r.text, 'lxml')
    tables = soup.find_all('table', attrs={'cellpadding':'2'})
# print(tables)
    for table in tables:
        trs = table.find_all('tr')
        for tr in trs :
            date, value, price = [td.text for td in tr.find_all('td')]
            if date =='日期':
                columns.append 
            data.append([date, value, price])
            
df = pd.DataFrame(data, columns=['日期', '買賣超金額', '台指期'])
df.to_csv('big_eight.csv')
df.to_csv('big_eight.html')
df.to_csv('big_eight.xlsx')
print(data)

    