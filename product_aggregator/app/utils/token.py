import json
import os
import requests

from product_aggregator import settings


def get_token():
    try:
        url = os.environ["BASE_URL"] + "/auth"
    except KeyError:
        url = "https://applifting-python-excercise-ms.herokuapp.com/api/v1/auth"
    response = requests.post(url)
    token = response.json()["access_token"]

    try:
        os.makedirs(str(settings.BASE_DIR) + "/tmp/service_token/")
    except FileExistsError:
        pass
    with open(str(settings.BASE_DIR) + "/tmp/service_token/product_aggregator.json", "w+") as token_file:
        json.dump(token, token_file)


def return_token():
    try:
        with open(str(settings.BASE_DIR) + "/tmp/service_token/product_aggregator.json", "r") as token_file:
            return token_file.read().replace('"', "")
    except FileNotFoundError:
        get_token()
        return_token()
