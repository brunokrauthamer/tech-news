import requests
import time
from parsel import Selector
from bs4 import BeautifulSoup
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    headers = {"user-agent": "Fake user-agent"}
    try:
        response = requests.get(url, headers=headers, timeout=3)
        time.sleep(1)
    except requests.Timeout:
        return None
    if response.status_code != 200:
        return None
    return response.text


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)
    news = selector.css("main article header h2 a::attr(href)").getall()
    return news


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    link = selector.css(".next.page-numbers::attr(href)").get()
    return link


def remove_white_spaces(string):
    new_string = string
    while new_string[-1] == ' ':
        new_string = new_string[0:-1]
    return new_string


def scrape_summary(html):
    selector = Selector(text=html)
    parag = selector.css(".entry-content").get()
    soup = BeautifulSoup(parag, "html.parser")
    return soup.p.get_text()


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)
    url = selector.css("[rel=\"canonical\"]::attr(href)").get()
    title = selector.css(".entry-title::text").get()
    timestamp = selector.css(".meta-date::text").get()
    writer = selector.css(".author a::text").get()
    reading_time_text = selector.css(".meta-reading-time::text").get()
    summary = scrape_summary(html_content)
    category = selector.css(".label::text").get()
    reading_time = int(reading_time_text[0:-19])
    treated_title = title.replace('\xa0', '')
    treated_title = remove_white_spaces(treated_title)
    treated_summary = summary.replace('\xa0', '')
    treated_summary = remove_white_spaces(treated_summary)

    return {
        "url": url,
        "title": treated_title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": treated_summary,
        "category": category
    }


# Requisito 5
def get_tech_news(amount):
    if (amount % 12) != 0:
        number_of_pages = int((amount - (amount % 12)) / 12 + 1)
    else:
        number_of_pages = int(amount / 12)
    number_of_links_last_page = amount - 12 * (number_of_pages - 1)
    links = []
    page_url = 'https://blog.betrybe.com'
    for _ in range(number_of_pages - 1):
        html_page = fetch(page_url)
        links.extend(scrape_updates(html_page))
        page_url = scrape_next_page_link(html_page)
    html_page = fetch(page_url)
    links.extend(scrape_updates(html_page)[0:number_of_links_last_page])
    news_info = []
    for link in links:
        new_html = fetch(link)
        new_info = scrape_news(new_html)
        news_info.append(new_info)
    create_news(news_info)
    return news_info
