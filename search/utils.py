"""contains supporting function for the search view."""
import requests
from urllib import parse


def geo_code(address: str) -> dict:
    """Return search results of the address locations and their coordinates.
    
    :params address: query string of location being looked up
    """
    context = {
        "ok": False,
        "found": False,
        "searched": True
    }
    url = "https://geocode-maps.yandex.ru/1.x/?apikey=12138073-3f58-4720-a7f5-8c2bf51a3329"
    query = f"&geocode={address}&lang=en_US&format=json"
    url += query
    try:
        response = requests.get(url)
    except Exception:
        return context

    if response.status_code == 200:
        context["ok"] = True
        response = response.json()
        found = response["response"]["GeoObjectCollection"]\
            ["metaDataProperty"]["GeocoderResponseMetaData"]["found"]
        found = int(found)

        if found == 0:
            context["found"] = False
        else:
            context["found"] = True
            locations = response['response']['GeoObjectCollection']['featureMember']
            context["results"] = []
            for location in locations:
                name = location["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
                longitude = location['GeoObject']['Point']['pos'].split()[0]
                latitude = location['GeoObject']['Point']['pos'].split()[1]
                context["results"].append(
                    {
                        "name": name,
                        "latitude": latitude,
                        "longitude": longitude
                    }
                )
    return context
