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
from pymongo import Mongoclient

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
# Получаем ссылку на сайт, с которого будем изуать данные

main_link_mail = 'https://news.mail.ru/economics/'
# Захватывается определенное значение, для того
# чтобы изучить данные, которые были получены в результате запроса GET.
responsee_mail = requests.get(main_link_mail, headers=headers)

dom_mail = html.fromstring(responsee_mail.text)

items_mail = dom_mail.xpath("//div[@class='newsitem newsitem_height_fixed js-ago-wrapper js-pgng_item']")
news_mail = []
for item in items_mail:
    new = {}
    # -наименование новости;
    name = item.xpath(".//span[@class='newsitem__title-inner']/text()")
    # -ссылку на новость;
    links = item.xpath(".//a[@class='newsitem__title link-holder']/@href")
    # -дата публикации.
    data_time = item.xpath(".//span[@datetime]/text()")
    # -название источника;
    news_source = item.xpath(".//span[@class='newsitem__param']/text()")
    new['name'] = name
    new['links'] = links
    new['data_time'] = data_time
    new['news_source'] = news_source
    news_mail.append(new)

client = MongoClient('127.0.0.1', 2701)
db = client['mail.ru_news']
news_collection = db.news_collection
news_collection.insert_many(news_mail)