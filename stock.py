import requests
from bs4 import BeautifulSoup

r = requests.get('https://tw.stock.yahoo.com/quote/2498.TW')
if r.status_code == requests.codes.ok:
    soup = BeautifulSoup(r.text, 'html.parser')
    # ul = soup.find('ul', class_='D(f) Fld(c) Flw(w) H(192px) Mx(-16px)')
    # li = ul.find_all('li',class_='price-detail-item')[0]
    # price = li.find_all('span')[1]
    price = soup.find('ul', class_='D(f) Fld(c) Flw(w) H(192px) Mx(-16px)').find_all('li', class_='price-detail-item')[0].find_all('span')[1]
    open_price = price.find_next('li').find_all('span')[1]
    hight_price = open_price.find_next('li').find_all('span')[1]
    print(price.text)
    print(open_price.text)
    print(hight_price.text)
    
