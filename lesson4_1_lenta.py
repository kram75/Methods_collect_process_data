# 1. Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# -название источника;
# -наименование новости;
# -ссылку на новость;
# -дата публикации.
#
# 2. Сложить собранные данные в БД

from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
# Получаем ссылку на сайт, с которого будем изуать данные
main_link = 'https://lenta.ru/rubrics/economics/'
# Захватывается определенное значение, для того
# чтобы изучить данные, которые были получены в результате запроса GET.
responsee = requests.get(main_link, headers=headers)

dom = html.fromstring(responsee.text)

items = dom.xpath("//div[@class='item news b-tabloid__topic_news']")
news = []
for item in items:
    new = {}
    # -наименование новости;
    name = item.xpath(".//div[@class='titles']//text()")
    # -ссылку на новость;
    links = item.xpath(".//h3/a[@href]/@href")
    # -дата публикации.
    data_time = item.xpath(".//span[@class='g-date item__date']/text()")
    # -название источника;
    news_source = '"Лента.ру"'

    new['name'] = name
    new['links'] = links
    new['data_time'] = data_time
    new['news_source'] = news_source
    news.append(new)

pprint(news)

client = MongoClient('127.0.0.1', 2701)
db = client['lenta.ru_news']
news_collection = db.news_collection
news_collection.insert_many(news)