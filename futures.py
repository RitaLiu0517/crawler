# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# from pprint import pprint


# def crawl(date):
#     r = requests.get('https://www.taifex.com.tw/cht/3/futContractsDate?queryDate={}%2F{}%2F{}'.format(date.year, date.month, date.day))
#     if r.status_code == requests.codes.ok:
#         soup = BeautifulSoup(r.text, 'html.parser')
#         print('successfully got data form ', date)
#     else:
#         ('connection error')

#     try:
#         table = soup.find('table', class_='table_f')
#         trs = table.find_all('tr')
#     except:
#         print('no data in this date', date)
#         return

#     rows = trs[3:]
#     data = {}
#     for row in rows:
#         tds = row.find_all('td')
#         cells = [td.text.strip() for td in tds]

#         if cells[0] == '期貨小計':
#             break

#         if len(cells) == 15:
#             product = cells[1]
#             row_data = cells[1:]
#         else:
#             row_data = [product] + cells
#         # print(len(data))

#         converted = [int(d.replace(',','')) for d in row_data[2:]]
#         row_data = row_data[:2] + converted
#         # print(row_data)

#         headers = ['商品名稱', '身份別', '交易多方口數', '交易多方金額', '交易空方口數', '交易空方金額', '交易多空淨口數', '交易多空淨金額', '未平倉多方口數', '未平倉多方金額',
#                     '未平倉空方口數', '未平倉空方金額', '未平倉淨口數', '未平倉淨金額']
        
#         #product -> who -> what
#         product = row_data[0]
#         who = row_data[1]
#         contents = {headers[i]: row_data[i] for i in range(2, len(headers))}
#         if product not in data:
#             data[product] = {who: contents}
#         else:
#             data[product][who] = contents
    
#     pprint(data)
#     return data



# date = datetime.today()
# while True:
#     date = date - timedelta(days=1) #今天減一天的日期
#     if date <= datetime.today() - timedelta(days=5):
#         break
#     crawl(date)

    


import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pprint import pprint
import json
from threading import Thread
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def crawl(date):
    r = requests.get('https://www.taifex.com.tw/cht/3/futContractsDate?queryType=1&goDay=&doQuery=1&dateaddcnt=&queryDate={}%2F{}%2F{}&commodityId='.format(date.year, date.month, date.day))
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
    else:
        print('connection error')
    
    try:
        table = soup.find('table', class_='table_f')
        trs = table.find_all('tr')[3:]
    except AttributeError:
        print('There is no data at', date.strftime('%Y/%m/%d'))
        return
    
    data = {}
    for tr in trs:
        tds = tr.find_all('td')
        ths = tr.find_all('th')
        if len(ths) == 3:
            product = ths[1].text.strip()
            who = ths[2].text.strip()
            what = [td.text.strip() for td in tds]
            data[product] = {who: what}
        else:
            who = ths[0].text.strip()
            what = [td.text.strip() for td in tds]
            data[product].update({who: what})
        
    print(date, '\n', data)
    return date, data


def save_json(date, data, path):
    filename = os.path.join(path, 'futures_' + date.strftime('%Y%m%d') + '.json')
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print('saved file to', filename)


download_dir = 'futures'
os.makedirs(download_dir, exist_ok=True)
start = datetime.now()

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = []
    today = datetime.today()
    date = today

    while True:
        future = executor.submit(crawl, date)
        futures.append(future)

        date = date - timedelta(days=1)
        if date <= today - timedelta(days=5):
            break

    for future in as_completed(futures):  
        if future.result():
            date, data = future.result()
            save_json(date, data, download_dir)
                
                
end = datetime.now()
print("執行時間：", end - start)