from bs4 import BeautifulSoup
import requests


def scrape(data):
    url = BeautifulSoup(requests.get(data).text, 'lxml')
    bs = url
