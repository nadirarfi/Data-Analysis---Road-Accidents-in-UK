import os
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier




class SeverityPredictor:

    def __init__(self):
        self.preprocess_data()
        self.get_model()
        self.train_model()
    
    def predict_severity(self, data):
        data= {'Speed Limit': 10, 'Daytime': 1, 'Light Conditions': 0, 'Day': 1, 'Special Conditions At Site': 0, '1st Road Class': 1, 'Junction Control': 1, 'Junction Detail': 1, 'Road Surface Conditions': 1, 'Road Type': 1, 'Area': 1, 'Weather Conditions': 1, 'latitude': 43.6000285, 'longitude': 1.4417134}
        data = pd.DataFrame([data])
        data = data.rename(columns={
            "Speed Limit": "speed_limit",
            "Daytime": "time",
            "Light Conditions": "light_conditions",
            "Day": "day",
            "Special Conditions At Site": "special_conditions_at_site",
            "1st Road Class": "1st_road_class",
            "Junction Control": "junction_control",
            "Junction Detail": "junction_detail",
            "Road Surface Conditions": "road_surface_conditions",
            "Road Type": "road_type",
            "Area": "urban_or_rural_area",
            "Weather Conditions": "weather_conditions"
            })  
        data = data[["1st_road_class","latitude","longitude","junction_control","day","junction_detail","light_conditions","road_surface_conditions","road_type","special_conditions_at_site","speed_limit","time","urban_or_rural_area","weather_conditions"]]
        self.prediction_value = self.model.predict(data)[0]
        if self.prediction_value ==  0:
            self.severity = "Serious"
        else:
            self.severity = "Slight"


    """
    def predict_severity(self, data):
        
        accident_factors = pd.DataFrame()
        prediction_value = self.model.predict(accident_factors)
    
        def predictResult(self, data):
        inputData = []
        for col in self.cols:
            inputData.append(data[col])

        inputData = {'0' : inputData}
        test = pd.DataFrame.from_dict(inputData, orient='index', columns=self.cols)
        new_prediction = self.model.predict(test)
        print(new_prediction)


    """

    def get_model(self):
        self.model = RandomForestClassifier(
            bootstrap = True, class_weight = "balanced_subsample",criterion = 'gini',
            max_depth = 8, max_features = 'auto', max_leaf_nodes = None,
            min_impurity_decrease = 0.0, min_samples_leaf = 4, min_samples_split = 10,
            min_weight_fraction_leaf = 0.0, n_estimators = 300, oob_score = False,
            random_state = 35,verbose = 0, warm_start = False)
        
    def preprocess_data(self):
        df =  pd.read_csv("./train_dataset.csv")
        X = df.drop(['accident_severity'], axis=1)
        y = df['accident_severity'].replace(['Fatal'], 'Serious')
        y_encoded = LabelEncoder().fit_transform(y)
        X_encoded = X.copy()
        for col in X.columns:
            if X[col].dtype == np.dtype('O'):
                X_encoded[col] = LabelEncoder().fit_transform(X[col])
            if X[col].dtype == np.dtype('int64') or X[col].dtype == np.dtype('float64'):
                X_encoded[col] = StandardScaler().fit_transform(X[col].values.reshape(-1,1))
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=1)

    def train_model(self):
        self.model.fit(self.X_train, self.y_train)
    

"""
data= {'Speed Limit': 10, 'Daytime': 1, 'Light Conditions': 0, 'Day': 1, 'Special Conditions At Site': 0, '1st Road Class': 1, 'Junction Control': 1, 'Junction Detail': 1, 'Road Surface Conditions': 1, 'Road Type': 1, 'Area': 1, 'Weather Conditions': 1, 'latitude': 43.6000285, 'longitude': 1.4417134}
obj =  SeverityPredictor()
obj.predict_severity(data)
print(obj.prediction_value, obj.severity)
"""


def get_factors():
    factors = {
    'Speed Limit':{
        '10': 10,
        '20': 20,
        '30': 30,
        '40': 40,
        '50': 50,
        '70': 70,
        '60': 60,
    },
    'Daytime':{
        'Night': 2,
        'Day': 1
    },
    'Light Conditions': {
        'Darkness - lights lit': 1,
        'Darkness - no lighting': 1,
        'Darkness - lighting unknown': 1,
        'Darkness - lights unlit': 1,
        'Daylight': 0,
        #'Data missing or out of range': 0
    },
    'Day': {
        'Monday': 0,
        'Tuesday': 0,
        'Wednesday': 0,
        'Thursday': 0,
        'Friday': 0,
        'Saturday': 1,
        'Sunday': 1

    },
    'Special Conditions At Site': {
        'Roadworks': 1,
        'Oil or diesel': 1,
        'Mud': 1,
        'Road surface defective': 1,
        'Auto traffic signal - out': 1,
        'Road sign or marking defective or obscured': 1,
        'Auto signal part defective': 1,
        'None': 0
        #'Data missing or out of range': 0
    },
    '1st Road Class': {
        #'A(M)': 1,
        'B': 2,
        'C': 3,
        'Motorway': 4,
        'A': 1
        #'Unclassified': 1
    },
    'Junction Control': {
        'Auto traffic signal': 2,
        'Not at junction or within 20 metres': 3,
        'Stop sign': 4,
        'Authorised person': 5,
        'Give way or uncontrolled': 1
    },
    'Junction Detail': {
        'T or staggered junction': 2,
        'Crossroads': 3,
        'Roundabout': 4,
        'Private drive or entrance': 5,
        'Other junction': 6,
        'Slip road': 7,
        'More than 4 arms (not roundabout)': 8,
        'Mini-roundabout': 9,
        'Not at junction or within 20 metres': 1
        #'Data missing or out of range': 1
    },
    'Road Surface Conditions': {
        'Wet or damp': 2,
        'Frost or ice': 3,
        'Snow': 4,
        'Flood over 3cm. deep': 5,
        'Dry': 1
        #'Data missing or out of range': 1
    },
    'Road Type': {
        'Single carriageway': 1,
        'Roundabout': 3,
        'One way street': 4,
        'Slip road': 5,
        'Dual carriageway': 2
        #'Unknown': 0,
        #'Data missing or out of range': 1
    },
    'Area': {
        'Urban': 1,
        'Rural': 2,
        #'Unallocated': 1
    },
    'Weather Conditions': {
        "Raining no high winds": 2,
        "Raining + high winds": 3,
        "Fine + high winds": 4,
        "Snowing no high winds": 5,
        "Fog or mist": 6,
        "Snowing + high winds": 7,
        "Fine no high winds": 1
        #"Unknown": 1,
        #"Other": 1,
        #"Data missing or out of range": 1
    }
    }
    return factors





