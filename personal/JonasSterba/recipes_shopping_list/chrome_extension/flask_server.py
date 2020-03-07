import json
import logging
import os


from collections import Counter
from ast import literal_eval
import requests
from bs4 import BeautifulSoup

from flask import Flask, flash, redirect, request, send_from_directory, session, url_for
from flask_cors import CORS, cross_origin
# from werkzeug.utils import secure_filename

from jonas_werkzeug import find_urls


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("recipy")

app = Flask(__name__)
CORS(app, expose_headers="Authorization")


def extract():
    # extracting data from Chrome Extension and converting to list
    data = request.data.decode()
    data = literal_eval(data)

    # converting the list to dictionary key = recipe with url; value = count of recipe added
    data = dict(Counter(json.dumps(l) for l in data))

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

    # dumping the list to json where output is a list of ingredient and its count
    data = json.dumps({"Zakupy": data}, indent=4)
    return data


@app.route("/", methods=["POST", "GET"])
def generate_list():
    logger.info("Generating list.")
    data = extract()
    logger.info("Transforming to portable format")
    data = transform(data)
    logger.info("Printing out")
    data = load(data)
    return data


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="0.0.0.0", use_reloader=False)