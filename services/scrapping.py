from flask_restful import Resource, reqparse
from bs4 import BeautifulSoup
import requests
import re
from flask_restful_swagger import swagger
from models import Record, Observation
from schemas import ObservationSchema
from typing import List

parser = reqparse.RequestParser()
parser.add_argument("plat")
parser.add_argument("start")
parser.add_argument("page")
parser.add_argument("url")


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
        except Exception as e:
            return {"error": f"{str(e)}"}, 503

    def parse_recette(self, url, plat):
        req = requests.get(url)
        source_page = BeautifulSoup(req.text, "html.parser")
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
            source_page.find("li", class_="selected")
            .next_sibling.contents[0]["href"]
            .split("&")[1:]
        )
        if next_page:
            start = "".join(re.findall(regex, next_page[0]))
            page = "".join(re.findall(regex, next_page[1]))
            return f"ingredients?plat={plat}&start={start}&page={page}"


class RealTimeDataAvailable(Resource):
    @swagger.operation(
        notes="Liste les datasets disponibles sur le site https://www.data.gouv.fr/fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/",
        responseMessages=[
            {"code": 503, "message": "service temporairement indisponible"},
        ],
    )
    def get(self):
        r = requests.get(
            "https://www.data.gouv.fr/fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/"
        )
        if r.status_code != 200:
            return {"error" : "service temporairement indisponible"}
        soup = BeautifulSoup(r.text, "lxml")
        cards = soup.find_all("article", {"class": "card resource-card"})
        results = []
        for card in cards:
            item = {}
            name = card.find("h4").get_text()
            if "E2" in name:
                try:
                    item["name"] = name
                    href = card.find("a", {"class": "btn btn-sm btn-primary"})["href"]
                    item[
                        "link"
                    ] = f"https://mg-services.herokuapp.com/api/open-data/pollution/air/real-time?url={href}"
                    results.append(item)
                except KeyError:
                    pass

        return results, 200


class RealTime(Resource):
    polluants = {
        "1": "SO2",
        "10": "CO",
        "6001": "PM2.5",
        "7": "O3",
        "20": "C6H6",
        "9": "NOX as NO2",
        "8": "NO2",
        "5": "PM10",
    }

    @swagger.operation(
        notes="fourni un endpoint pour les données https://www.data.gouv.fr/fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/",
        parameters=[
            {
                "name": "url",
                "description": "l'url du fichier xml à parser",
                "required": True,
                "paramType": "query",
                "dataType": "string",
            }
        ],
        responseMessages=[
            {"code": 503, "message": "l'url du fichier n'a pas été atteinte"},
        ],
    )
    def get(self):
        args = parser.parse_args()
        url = args.get("url")
        if not url:
            return {"error": "l'url est requise"}, 400
        response = self.get_xml(url)
        if not response.status_code == 200:
            return {"error": f"Request to {url} failed"}, response.status_code
        xml = response.text
        if not xml:
            return {"error": "le document xml est vide"}, 400

        observations = self.parse_observations(xml)
        schema = ObservationSchema(many=True)
        return schema.dump(observations), 200

    def get_xml(self, url: str) -> requests.Response:
        r = requests.get(url)
        return r

    def parse_observations(self, xml: str) -> List[Observation]:

        soup = BeautifulSoup(xml, "xml")
        observations = []
        for member in soup.find_all("om:OM_Observation"):
            key = member.find("om:observedProperty")["xlink:href"].split("/")[-1]
            sample_point = (
                member.find_all("om:NamedValue")[-1]
                .find("om:value")["xlink:href"]
                .split("/")[-1]
            )
            obsv = Observation(self.polluants[key], sample_point)
            values = member.find("swe:values").get_text().replace("\n", "").split("@@")
            records = self.parse_records(values)
            obsv.records = records
            observations.append(obsv)
        return observations

    def parse_records(self, values: List) -> List[Record]:
        records = []
        for v in values:
            block = v.split(",")
            if block[0]:
                records.append(Record(*block))
        return records
