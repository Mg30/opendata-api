from flask_restful import Resource
from flask_restful import reqparse
from bs4 import BeautifulSoup
import requests
import re


parser = reqparse.RequestParser()
parser.add_argument("plat")
parser.add_argument("start")
parser.add_argument("page")


class Marmiton(Resource):
    def get(self):
        args = parser.parse_args()
        plat = args.get("plat")
        start = args.get("start")
        page = args.get("page")
        url = ""
        if start and page:
            url = f"https://www.marmiton.org/recettes/recherche.aspx?aqt={plat}&start={start}&page={page}"
        else:
            url = f"https://www.marmiton.org/recettes/recherche.aspx?aqt={plat}"

        result = self.parse_ingredients(url, plat)
        if result:
            return result, 200
        else:
            return {"Error": "No result found"}, 404

    def parse_ingredients(self, url, plat):
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
            return f"http://localhost:5000/ingredients?plat={plat}&start={start}&page={page}"
