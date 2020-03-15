import logging
import os
import json

# ania gotuje
from recipes_shopping_list.recipes_server.ania_gotuje.ania_gotuje_ETL import ania_main, ania_test
from ast import literal_eval

from flask import Flask, request
from flask_cors import CORS
# from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("recipy")

app = Flask(__name__)
CORS(app, expose_headers="Authorization")


def test(data):
    """
    Main test for each culinary web site to check whether the link is from their site
    :param data: list of strings
    :return: segregated lists
    """

    # empty list per each culinary website
    ania_raw_list = list()
    others_list = list()

    # segregation of recipes where specific function is called (returing True / False) if particular recipe is from
    # that site
    for recipe in data:
        recipe = json.dumps(recipe)
        if ania_test(recipe):
            ania_raw_list.append(recipe)
        else:
            others_list.append(recipe)

    return ania_raw_list, others_list


@app.route("/", methods=["POST", "GET"])
def generate_list():
    # extracting data from Chrome Extension and converting to list
    data = request.data.decode()
    data = literal_eval(data)

    # directing recipes per website
    ania_raw_list, others_list = test(data)
    ania_list = list()

    # extracting shopping list from segregated lists using main ETL function for each culinary website
    if ania_raw_list:
        ania_list = ania_main(ania_raw_list)
    else:
        pass

    # merging lists together and throwing them to a 'dictionary string'
    main_list = ania_list + others_list
    main_list = json.dumps({"Zakupy": main_list}, indent=4)
    return main_list


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="0.0.0.0", use_reloader=False)