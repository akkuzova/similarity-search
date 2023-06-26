import json

from flask import Flask
from flask import request
from text_index import TextIndex
import numpy as np

app = Flask(__name__)
text_index = TextIndex()


@app.post("/index")
def create_index():
    print(request.json, '\n')
    vectors = request.json
    print(vectors, '\n')
    text_index.build_index(vectors)
    info = {
        'vector_count': text_index.get_vector_count(),
        'dimension': text_index.get_vector_dimension()
    }
    return info


@app.get("/closest_vectors")
def get_keywords():
    print(request.args, '\n')
    xq = request.args.get('xq', '')
    xq = np.array(xq.split(','))
    print(xq, '\n')
    k = request.args.get('k', '')
    return text_index.search(xq, k)
