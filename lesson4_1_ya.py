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

main_link_ya = 'https://yandex.com/news'
# Захватывается определенное значение, для того
# чтобы изучить данные, которые были получены в результате запроса GET.
responsee_ya = requests.get(main_link_ya, headers=headers)

if responsee_ya.status_code == 200:
    print('Success!')
elif responsee_ya.status_code == 404:
    print('Not Found.')

dom_ya = html.fromstring(responsee_ya.text)
items_ya = dom_ya.xpath("//h2[@class='news-card__title']")

news_ya = []

for item in items_ya:
    new = {}
    # -наименование новости;
    name = item.xpath(".//h2[@class='news-card__title']/text()")
    # -ссылку на новость;
    links = item.xpath(".//a[@class='news-card__link']/@href")
    pprint(links)
    # -дата публикации.
    data_time = item.xpath(".//span[@class='mg-card-source__time']/text()")
    # -название источника;
    news_source = item.xpath(".//span[@class='mg-card-source__source']/text()")
    new['name'] = name
    new['links'] = links
    new['data_time'] = data_time
    new['news_source'] = news_source
    news_ya.append(new)

client = MongoClient('127.0.0.1', 2701)
db = client['ya.ru_news']
news_collection = db.news_collection
news_collection.insert_many(news_ya)

# C яндексом возникла такая ошибка. Так и не смог пути проверить через Xpath
# DevTools failed to load SourceMap: Could not load content for
# chrome-extension://ljngjbnaijcbncmcnjfhigebomdlkcjo/content-script/browser-polyfill.min.js.map:
# HTTP error: status code 404, net::ERR_UNKNOWN_URL_SCHEME