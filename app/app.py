import os
import json
from flask import Flask, render_template
from flask import request, redirect, make_response
from flask_cors import CORS
from predictor_tool import SeverityPredictor, get_factors
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from urllib.parse import urlencode
import requests

api_key = "AIzaSyBwx4dzgid-JuepltZ-JZat56Jt_VsKKKM"
app = Flask(__name__, template_folder='./templates')
app.config['GOOGLEMAPS_KEY'] = api_key
CORS(app)



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


predictor = SeverityPredictor()

# Initialize the extension
GoogleMaps(app)


@app.route("/")
def homepage():
    return render_template("index.html", factors= get_factors())




@app.route('/predict', methods=['POST'])
def predict_severity():
    """
    data = {
        **{ key: list(values.values())[0] for key, values in get_factors().items()},
        "latitude": 51.437209, # Default values
        "longitude": 0.238986                  
    } 
    """
    data = predictor.X_train.iloc[30000]
    req_data = request.form.to_dict()
    if req_data:
        address = req_data["address"]
        lat, lng = extract_lat_lng(address)
        data['latitude'] = lat
        data['longitude'] = lng   

    for key in data.keys():
        if key in req_data.keys():
            data[key] = req_data[key]

    predictor.predict_severity(data)
    severity = predictor.severity

    if severity == "Serious":
        colour = "red"
    else:
        colour = "green"

    accident_map = Map(
        region="UK",
        scale_control=True,
        zoom=13,
        identifier="accident_map",
        lat=lat,
        lng= lng,
        style = "height:500px;width:900px",
        markers=[
          {
             'icon': f'http://maps.google.com/mapfiles/ms/icons/{colour}-dot.png',
             'lat': lat,
             'lng': lng,
             'infobox': severity
          }
        ]
    )
    
    return render_template("index.html", map= accident_map, severity=severity)




if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, threaded=True)
