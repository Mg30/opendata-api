from flask_restful_swagger import swagger
from flask_restful import Resource, reqparse
from database import get_db
import dns

parser = reqparse.RequestParser()
parser.add_argument("sample_point_id")


class SamplePoint(Resource):
    @swagger.operation(
        notes="Renvoie un objet sample point contenu dans le dataset D https://www.data.gouv.fr/fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/",
        parameters=[
            {
                "name": "sample_point_id",
                "description": "l'id du sample point p.ex: FR01001_38",
                "required": True,
                "paramType": "path",
                "dataType": "string",
            }
        ],
        responseMessages=[
            {"code": 400, "message": "l'id du sample point doit être fourni"},
            {"code": 404, "message": "Le sample point n'as pas été trouvé"},
            {"code": 503, "message": "service temporairement indisponible"},
        ],
    )
    def get(self, sample_point_id):

        if not sample_point_id:
            return {"error": "l'id du sample point doit être fourni"}, 400
        try:
            db = get_db()
            db = db.openData
            sample_point = db.SamplingPoints.find_one(
                {"@gml:id": sample_point_id}, projection={"_id": False}
            )
            if sample_point:
                return sample_point, 200
            else:
                return (
                    {"error": f"Le sample point {sample_point_id} n'as pas été trouvé"},
                    404,
                )
        except dns.exception.Timeout:
            return {"error": "service temporairement indisponible"}, 503
