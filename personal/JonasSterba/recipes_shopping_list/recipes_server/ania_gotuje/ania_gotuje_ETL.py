from collections import Counter
import requests
from bs4 import BeautifulSoup
from recipes_shopping_list.recipes_server.commons.jonas_werkzeug import find_urls
import logging


def ania_test(recipe_link):
    """
    Simple test whether the recipe is from Ania's site (more bugs can appear as site with no recipes)

    :param recipe_link: url header
    :return: True /False
    """

    if recipe_link.upper().find("ANIAGOTUJE") > 0:
        return True
    else:
        return False


def ania_main(data):
    """
    Main flow for ETL
    :param data: list of recipes

    :return: shopping list
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Ania_recipy")
    # setting up the logger
    logger.info("Generating list from Ania Gotuje site.")
    data = extract(data)
    logger.info("Transforming to portable format")
    data = transform(data)
    logger.info("Printing out")
    data = load(data)

    return data


def extract(data):

    # converting the list to dictionary key = recipe with url; value = count of recipe added
    data = dict(Counter(l for l in data))

    # extracting the url from the key and putting it to a list of list
    recipe_list = list()
    if data:
        for k, v in data.items():
            url = find_urls(k)[1]

            simple_list = [url, v]
            recipe_list.append(simple_list)

    data = recipe_list
    return data


def transform(data):

    # scraping the URL based on ul and li tags
    final_list = list()
    for item in data:
        f = requests.get(item[0])
        soup = BeautifulSoup(f.content, 'html.parser')

        ul_tags = soup.findAll('ul', class_='recipe-ing-list')
        for ul_tag in ul_tags:
            for li_tag in ul_tag.find_all('li'):
                final_list.append([li_tag.text, item[1]])

    data = final_list
    return data


def load(data):
    return data

