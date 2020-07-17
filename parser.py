import requests
from bs4 import BeautifulSoup
import csv
import os

PATH = 'file.csv'
REQ = input('What do you want to find on OLX: ').replace(' ','-')
URL = f'https://www.olx.kz/list/q-{REQ}/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

def get_html (URL, params=None):
    req = requests.get(URL, headers=HEADERS, params=params)
    return req

def get_content (html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr', class_='wrap')
    arr = []
    for item in items:
        city = item.find('td', class_='bottom-cell')
        if item.find('p', class_='price' ):
            arr.append(
                {
                    'title' : item.find('a', class_='marginright5 link linkWithHash detailsLink').get_text().replace('\n','').replace('қ','к').replace('‑','').replace('ұ','у').replace('ғ','г').replace('ң','н').replace('ө','о').replace('','').replace('ℝ','').replace('İ','i'),
                    'cost' : item.find('p', class_='price' ).get_text().replace('\n','').replace(' тг','').replace('Бесплатно','0'),
                    'city' : city.find('span').get_text().replace('\n','').replace('қ','к').replace('‑','').replace('ұ','у').replace('ғ','г').replace('ң','н').replace('ө','о').replace('','').replace('ℝ','').replace('İ','i'),
                    'link' : item.find('a', class_='marginright5 link linkWithHash detailsLink').get('href')
                }
            )
        else:
            arr.append(
                {
                    'title' : item.find('a', class_='marginright5 link linkWithHash detailsLink').get_text().replace('\n','').replace('қ','к'),
                    'cost' : '-',
                    'city' : city.find('span').get_text().replace('\n','').replace('қ','к'),
                    'link' : item.find('a', class_='marginright5 link linkWithHash detailsLink').get('href')
                }
            )
    return arr

def obj_file (data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['Название', 'Цена в тенге', 'Город', 'Ссылка'])
        for line in data:
            writer.writerow([line['title'],line['cost'],line['city'],line['link']])
        print('Success!')

def get_pagin (html):
    soup = BeautifulSoup(html.text, 'html.parser')
    pagin = soup.find('a', {'data-cy' :'page-link-last'})
    if pagin:
        pagination = int(pagin.find('span').get_text())
        return pagination
    else:
        return 1

def parse():
    html = get_html(URL)
    if html.status_code==200:
        goods = []
        pagescount = get_pagin(html)
        for page in range(1,pagescount+1):
            print(f'Parsing page {page}  out of {pagescount}...')
            if page==1:
                html = get_html(URL)
            else:
                html = get_html(URL, params = {'page' : page})
            goods.extend(get_content(html.text))
        gat=int(len(goods))
        print(f'Recieved {gat} goods')
        obj_file(goods, PATH)
    else:
        die('Some errors occured!')

parse()