import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from flask_restful import Resource
from flask_restful import reqparse


nlp = spacy.load("fr_core_news_sm")
parser = reqparse.RequestParser()
parser.add_argument("file")


class FreqWords(Resource):
    def post(self):
        """Take a CSV file and return a list of dict {word: <word>, count: <word_freq>} """
        args = parser.parse_args()
        uploaded_file = args["file"]
        try:
            df = pd.read_csv(uploaded_file)
            text = " ".join(df["comment"])
            doc_nlp = nlp(text)
            processed_text = [token.lemma_ for token in doc_nlp if not token.is_stop]
            vectorizer = CountVectorizer(ngram_range=(1, 1))
            x = vectorizer.fit_transform(processed_text)
            word_list = vectorizer.get_feature_names()
            count_list = x.toarray().sum(axis=0)
            freq = dict(zip(word_list, count_list))
            freq = [{"word": k, "count": int(v)} for k, v in freq.items()]
            freq = freq[:31]
            return freq,200

        except Exception:
            return {"Error": "check file"}, 400

       
