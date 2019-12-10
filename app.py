from flask import Flask, request
import pandas as pd
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
CORS(app)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        df = pd.read_excel(request.files.get("file"))
        return df.to_json(orient="records")


if __name__ == "__main__":
    app.run(debug=True)
