import requests
from io import BytesIO
from PIL import Image


def map_scale(toponym):
    if not toponym:
        return None, None
    toponym_longitude, toponym_lattitude = toponym["Point"]["pos"].split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])
    envelope = toponym["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
    span = f"{dx},{dy}"
    return ll, span


adress = input()
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": adress,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_longitude, toponym_lattitude = toponym["Point"]["pos"].split(" ")
ll, span = map_scale(toponym)
map_params = {
    "ll": ll,
    "spn": span,
    "l": "map"
}
point_params = f'pt={ll},pm2dol'
ll_spn = f'll={ll}&spn={span}'
map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l=map"
response = requests.get(map_request + "&" + point_params)
Image.open(BytesIO(response.content)).show()
