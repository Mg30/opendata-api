from flask_restful import Resource, reqparse
from bs4 import BeautifulSoup
import requests
import re
from flask_restful_swagger import swagger

parser = reqparse.RequestParser()
parser.add_argument("plat")
parser.add_argument("start")
parser.add_argument("page")


class Marmiton(Resource):
    @swagger.operation(
        notes="Renvoie une liste de 15 plats à partir d'un nom de plat passé en paramètre à partir du site marmiton avec pour chacun sa liste d'ingrédients",
        parameters=[
            {
                "name": "plat",
                "description": "plat à chercher sur marmiton",
                "required": True,
                "paramType": "query",
                "dataType": "string",
            },
            {
                "name": "start",
                "description": "permet de spécifier un offset des résultats ",
                "required": False,
                "paramType": "query",
                "dataType": "integer",
            },
            {
                "name": "page",
                "description": "numéro de page des résultats",
                "required": False,
                "paramType": "query",
                "dataType": "integer",
            },
        ],
        responseMessages=[
            {"code": 200, "message": "Plat trouvé"},
            {
                "code": 400,
                "message": "Le nom du plat n'as pas été spécifié en argument",
            },
            {"code": 503, "message": "service temporairement indisponible"},
        ],
    )
    def get(self):
        args = parser.parse_args()
        plat = args.get("plat")
        start = args.get("start")
        page = args.get("page")
        url = ""
        if not plat:
            return {"error": "le nom du plat doit être spécifié"}, 400
        if start and page:
            url = f"https://www.marmiton.org/recettes/recherche.aspx?aqt={plat}&start={start}&page={page}"
        else:
            url = f"https://www.marmiton.org/recettes/recherche.aspx?aqt={plat}"

        try:
            result = self.parse_recette(url, plat)
            return result, 200
        except:
            return {"error": "service indisponible"}, 503

    def parse_recette(self, url, plat):
        req = requests.get(url)
        source_page = BeautifulSoup(req.text)
        recettes = source_page.find_all(class_="recipe-card")
        if recettes:
            recettes = self.extract_ingredients(recettes)
            recettes["next_page"] = self.extract_next_page(source_page, plat)
            return recettes
        else:
            return None

    def extract_ingredients(self, recettes):
        result = {}
        result["items"] = []
        for r in recettes:
            item = {}
            title = r.find(class_="recipe-card__title").get_text()
            item["nom"] = title
            ingredients = (
                r.find(class_="recipe-card__description").find("b").next_sibling
            )
            ingredients = ingredients.split(",")
            item["ingredients"] = ingredients
            result["items"].append(item)
        return result

    def extract_next_page(self, source_page, plat):
        regex = r"\d"
        next_page = (
            source_page.find("li", class_="next-page")
            .contents[0]["href"]
            .split("&")[1:]
        )
        if next_page:
            start = "".join(re.findall(regex, next_page[0]))
            page = "".join(re.findall(regex, next_page[1]))
            return f"ingredients?plat={plat}&start={start}&page={page}"


class InfoClimat(Resource):
    url = "https://www.infoclimat.fr/api-previsions-meteo.html?id=2988507&cntry=FR"

    @swagger.operation(
        notes="Permet d'obtenir un token d'authentification pour l'api prevision météo",
        responseMessages=[
            {"code": 200, "message": "Token parsé et envoyé"},
            {"code": 500, "message": "le site api-prévision n'a pas pu être atteint"},
        ],
    )
    def get(self):
        req = requests.get(self.url)
        if req.status_code != 200:
            return {"error": "le site api-prevision n'a pas pu être atteint"}, 500
        else:
            source_page = BeautifulSoup(req.text)
            textareas = source_page.find_all("textarea")
            json_area_text = textareas[2].get_text()
            auth = json_area_text.split("auth=")[-1]
            return {"token": auth}, 200


class DownloadFile(Resource):
    url = "https://static.data.gouv.fr/resources/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/20191015-090721/fr-2018-d-lcsqa-ineris-20190918-1.xml"

    def get(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "xml")
        stations = soup.find_all("gml:featureMember")
        results = []
        for station in stations:
            try:
                station_id = station.find("base:localId").get_text()
                coordinates = station.find("gml:pos").get_text()
                station_name = station.find("gn:text").get_text()
                results.append(
                    {
                        "station_id": station_id,
                        "coordinates": coordinates,
                        "station_name": station_name,
                    }
                )
            except:
                pass

        return results

