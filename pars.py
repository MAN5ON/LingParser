"""
https://vpravda.ru/archive/"
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@cluster0-y2po7.mongodb.net/vpravda")
db = client.vpravda
collection = db.archive

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': '*/*'}

urls = []
urls2 = []
news = []

chromedriver = "C:/Projects/web-cloud-parser/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get("https://vpravda.ru/archive/")
one_day = driver.find_elements_by_xpath("//div[@class='archive_wrapper']//a")
for i in one_day:
    a = i.get_attribute('href')
    url = {
        'href': a
    }
    urls.append(url)

for j in urls:
    driver.get(j['href'])
    one_news = driver.find_elements_by_xpath(
        "//div[@class='column']//div[@class='views-field views-field-field-article-image']//a")
    for n in one_news:
        b = n.get_attribute('href')
        url2 = {
            'children_href': b
        }
        urls2.append(url2)
    ruslan = -1
    for d in urls2:
        driver.get(d['children_href'])
        href_stat = d.get('children_href')
        news.clear()
        ruslan += 1
        print(ruslan)


        def get_html(html):
            r = requests.get(href_stat, headers=HEADERS)
            return r


        def get_content(html):
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.find_all('div', class_='column')

            for item in items:
                info = {
                    'link': driver.current_url,
                    'title': item.find('h1', class_='page__title title').get_text(),
                    'time_date': item.find('span', class_='date-display-single').get_text(),
                    'text_stat': item.find('div',
                                           class_='field field-name-body field-type-text-with-summary field-label-hidden').find().get_text(),

                }
                collection.insert_one(info)
                news.append(info)

            return news


        if ruslan == 20:
            driver.quit()
            chromedriver = "C:/Projects/web-cloud-parser/chromedriver"
            driver = webdriver.Chrome(chromedriver)
            driver.get(d['children_href'])
            ruslan = 0


        def parse():
            html = get_html(url2)
            if html.status_code == 200:
                news = get_content(html.text)
                print(news)
            else:
                print('Error')


        parse()
        driver.back()

    urls2.clear()
    driver.back()

driver.quit()
