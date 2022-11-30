import requests
from urllib.parse import urlencode

api_key = "AIzaSyBwx4dzgid-JuepltZ-JZat56Jt_VsKKKM"


data_type = 'json'
endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
params = {"address": "1600 Amphitheatre Parkway, Mountain View, CA", "key": api_key}
url_params = urlencode(params)

url = f"{endpoint}?{url_params}"


def extract_lat_lng(address_or_postalcode, data_type = 'json'):
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": address_or_postalcode, "key": api_key}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    r = requests.get(url)
    if r.status_code not in range(200, 299): 
        return {}
    latlng = {}
    try:
        latlng = r.json()['results'][0]['geometry']['location']
    except:
        pass
    return latlng.get("lat"), latlng.get("lng")

loc = extract_lat_lng("20 Glebe Avenue, Leeds, UK")
print(loc)