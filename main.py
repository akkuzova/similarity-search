import json

from flask import Flask
from flask import request
from text_index import TextIndex
from wtforms import Form, BooleanField, StringField, PasswordField, validators

app = Flask(__name__)
textIndex = TextIndex()


@app.post("/index")
def create_index():
    vectors = json.load(request.json)
    textIndex.build_index(vectors)
    info = {
        'vector_count': textIndex.get_vector_count(),
        'dimension': textIndex.get_vector_dimension()
    }
    return info


@app.get("/closest_vectors")
def get_keywords():
    xq = request.args.get('xq', '')
    k = request.args.get('k', '')
    return textIndex.search(xq, k)
