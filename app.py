from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from services.scrapping import Marmiton, InfoClimat
from services.classifiers import ChurnClassifier
from flask_restful_swagger import swagger

app = Flask(__name__)
CORS(app)
api =  swagger.docs(Api(app))


api.add_resource(Marmiton, "/api/scrapping/marmiton/fetch/ingredients")
api.add_resource(ChurnClassifier, "/api/ml/predict/churn")
api.add_resource(InfoClimat, "/api/info-climat/auth")

if __name__ == "__main__":
    app.run(debug=True)
