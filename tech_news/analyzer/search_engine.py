from tech_news.database import find_news
from datetime import datetime


# Requisito 7
def search_by_title(title):
    news = find_news()
    filtered_news = []
    for new in news:
        if title.lower() in new['title'].lower():
            filtered_news.append((new['title'], new['url']))
    return filtered_news


def validate_date_format(date):
    try:
        date_object = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError('Data inválida')
    return date_object.strftime('%d/%m/%Y')


# Requisito 8
def search_by_date(date):
    br_date = validate_date_format(date)
    news = find_news()
    filtered_news = []
    for new in news:
        if new['timestamp'] == br_date:
            filtered_news.append((new['title'], new['url']))
    return filtered_news


# Requisito 9
def search_by_category(category):
    news = find_news()
    filtered_news = []
    for new in news:
        if category.lower() == new['category'].lower():
            filtered_news.append((new['title'], new['url']))
    return filtered_news
