from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from services.scrapping import Marmiton
from services.classifiers import ChurnClassifier

app = Flask(__name__)
CORS(app)
api = Api(app)  


api.add_resource(Marmiton, '/api/scrapping/marmiton/fetch/ingredients')
api.add_resource(ChurnClassifier, '/api/ml/predict/churn')

if __name__ == "__main__":
    app.run(debug=True)
