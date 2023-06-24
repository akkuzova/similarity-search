import json

from flask import Flask
from flask import request
from text_index import TextIndex

app = Flask(__name__)
text_index = TextIndex()


@app.post("/index")
def create_index():
    vectors = json.load(request.json)
    text_index.build_index(vectors)
    info = {
        'vector_count': text_index.get_vector_count(),
        'dimension': text_index.get_vector_dimension()
    }
    return info


@app.get("/closest_vectors")
def get_keywords():
    xq = request.args.get('xq', '')
    k = request.args.get('k', '')
    return text_index.search(xq, k)
