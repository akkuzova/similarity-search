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


@app.post("/closest_vectors")
def get_keywords():
    print(type(request.json))
    print(request.json, '\n')
    xq = np.array(request.json['xq'])
    print(xq, '\n')
    k = request.json['k']
    distances, neighbors = text_index.search(xq, k)
    return {'distances': distances.tolist(), 'neighbors': neighbors.tolist()}
