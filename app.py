from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from services.scrapping import Marmiton
from services.analysis import FreqWords

app = Flask(__name__)
CORS(app)
api = Api(app)  


api.add_resource(Marmiton, '/api/scrapping/marmiton/fetch/ingredients')
api.add_resource(FreqWords, '/api/analysis/freqWords')

if __name__ == "__main__":
    app.run(debug=True)
