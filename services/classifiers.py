from sklearn.ensemble import RandomForestClassifier
from flask_restful import Resource, reqparse
from flask import request
import pickle
import numpy as np
import pandas as pd
import json


class ChurnClassifier(Resource):
    def post(self):
        clf = RandomForestClassifier()
        clf = pickle.load(open("churn_classifier.sav", "rb"))
        try:
            data = request.files["file"]
        except KeyError:
            return {"error": "expected a key file containing csv file"}, 400

        try:
            X_test = pd.read_csv(data)
        except Exception:
            return {"error": "could not read the file"}, 400

        try:
            initial_churn = X_test["Churn"]
            X_test = X_test.drop(columns=["Churn", "Phone", "State"])
        except KeyError as e:
            return {"error": "could not find {e}"}, 400

        y_pred = clf.predict(X_test)
        y_pred = pd.DataFrame(y_pred, columns=["prediction"])
        y_pred["prediction"] = y_pred["prediction"].replace(0, "stay")
        y_pred["prediction"] = y_pred["prediction"].replace(1, "leave")
        X_test["Prediction"] = y_pred
        X_test["Original"] = initial_churn
        X_test["Original"] = X_test["Original"].replace(0, "stay")
        X_test["Original"] = X_test["Original"].replace(1, "leave")

        return X_test.to_dict(orient="records")
