def get_spn(toponym_to_find):
    import requests
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    lower_corner = toponym['boundedBy']['Envelope']['lowerCorner'].split()
    upper_corner = toponym['boundedBy']['Envelope']['upperCorner'].split()
    size = [
        str(abs(float(lower_corner[0]) - float(upper_corner[0]))),
        str(abs(float(lower_corner[1]) - float(upper_corner[1])))]
    return size


