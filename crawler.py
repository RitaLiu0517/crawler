import requests
from bs4 import BeautifulSoup


root_url = 'https://disp.cc/'

r = requests.get('https://disp.cc/b/PttHot')
soup = BeautifulSoup(r.text, 'html.parser')
for span in soup.find_all('span', class_='listTitle'): 
# 或使用CSS Selector 
# for span in soup.select('span.listTitle'): #後面可以繼續串接span.listTitle.L34.nowrap
    href = span.find('a').get('href')
    if href == '/b/PttHot/59l9': #排除某一篇文章
       break
    else:
       url = root_url + href
    print(url)
#    s = span.find('span', class_='titleColor')
#    print(s.text)
# 抑或是因為這個span標籤裡只剩下標題的文字，所以可以直接提取文字
    title = span.text
    print(f'{title}\n{url}')
