from sklearn.ensemble import RandomForestClassifier
from flask_restful import Resource, reqparse
from flask import request
import pickle
import numpy as np
import pandas as pd
import json

class ChurnClassifier(Resource):
    def post (self):
        clf = RandomForestClassifier()
        clf = pickle.load(open("churn_classifier.sav", "rb"))

        data = request.get_json()["data"]
        data = json.dumps(data)
        X_test = pd.read_json(data)
        y_pred = clf.predict(X_test)

        y_pred = pd.DataFrame(y_pred, columns=["prediction"])
        y_pred["prediction"] = y_pred["prediction"].replace(0,"stay")
        y_pred["prediction"] = y_pred["prediction"].replace(1,"leave")
        return y_pred.to_dict(orient='records')
