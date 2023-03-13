import requests
import time
from parsel import Selector


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
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
