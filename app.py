from flask import Flask, g
from flask_cors import CORS
from flask_restful import Api
from services.scrapping import Marmiton, RealTime, RealTimeDataAvailable
from services.endpoints import SamplePoint
from flask_restful_swagger import swagger


def create_app(*args):
    app = Flask(__name__)
    CORS(app)

    api = swagger.docs(Api(app))
    api.add_resource(Marmiton, "/api/scrapping/marmiton/fetch/ingredients")
    api.add_resource(RealTime, "/api/open-data/pollution/air/real-time")
    api.add_resource(
        SamplePoint,
        "/api/open-data/pollution/air/sample-point/<string:sample_point_id>",
    )
    api.add_resource(
        RealTimeDataAvailable, "/api/open-data/pollution/air/datasets",
    )

    @app.teardown_appcontext
    def close_database(response_or_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=False)
