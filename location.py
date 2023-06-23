import os

import requests
from database import *
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv('apikey')


def get_address_from_coords(coords):
    PARAMS = {
        "apikey": apikey,
        "format": "json",
        "lang": "en_US",
        "kind": "house",
        "geocode": coords
    }

    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return str(address_str)

    except Exception as e:
        print(e)
        print("Couldn't get the location")


def get_location(chat_id, location):
    current_position = (location.longitude, location.latitude)
    coords = f"{current_position[0]},{current_position[1]}"
    address_str = get_address_from_coords(coords)
    # print(address_str)
    update_user_to_finish_register2(chat_id, address_str)
    return address_str