from vector_index import VectorIndex
import re
import glob
import numpy as np
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()


class IndexManager:
    _file_name_pattern = f'{os.getenv("INDEX_DATA_FOLDER")}*.index'
    _indexes = {}

    def __init__(self):
        self._load_index_names()

    def _load_index_names(self):
        files = glob.glob(self._file_name_pattern)
        for path in files:
            name = re.search('[^/]*(?=\.index)', path).group()
            self._indexes[name] = VectorIndex(name)

    def _is_exists(self, index_id: str) -> bool:
        return True if index_id in self._indexes.keys() else False

    def _get_index(self, index_id: str) -> VectorIndex | None:
        if not self._is_exists(index_id):
            return None
        index = self._indexes[index_id]
        if not index.is_loaded():
            index.load()

        return index

    def get_index_info(self, index_id: str) -> dict:
        _index = self._get_index(index_id)
        return _index.get_info() if _index else {index_id: 'Not found'}

    def search(self, index_id: str, xq: List, k: int) -> dict[str, List]:
        xq = np.array(xq)
        index = self._get_index(index_id)

        if index is not None:
            distances, neighbors = index.search(xq, k)
            return {'distances': distances.tolist()[0], 'neighbors': neighbors.tolist()[0]}
        else:
            return {'distances': [], 'neighbors': []}

    def create_index(self, vectors, index_id) -> dict:
        index = VectorIndex(index_id).build(vectors)
        self._indexes[index_id] = index
        return index.get_info()

    def update_index(self, vectors):
        pass

    def delete_index(self):
        pass
