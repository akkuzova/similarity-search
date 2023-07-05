from flask import Flask
from flask import request
from controller import Controller

app = Flask(__name__)
controller = Controller()


@app.get('/index/<index_id>')
def get_index_info(index_id):
    print(index_id)
    return controller.get_index_info(index_id)


@app.post("/index/<index_id>")
def create_index(index_id):
    print(index_id, len(request.json))
    return controller.create_index(index_id, request.json)


@app.post("/search/<index_id>")
def search(index_id):
    print(index_id, len(request.json))
    return controller.search(index_id, request.json)
