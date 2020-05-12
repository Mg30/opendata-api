from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from services.scrapping import Marmiton, InfoClimat, RealTime
from services.endpoints import SamplePoint
from flask_restful_swagger import swagger

app = Flask(__name__)
CORS(app)
api = swagger.docs(Api(app))


api.add_resource(Marmiton, "/api/scrapping/marmiton/fetch/ingredients")
api.add_resource(InfoClimat, "/api/info-climat/auth")
api.add_resource(RealTime, "/api/open-data/pollution/air/real-time")
api.add_resource(SamplePoint, "/api/open-data/pollution/air/sample-point/<string:sample_point_id>")

if __name__ == "__main__":
    app.run(debug=True)
