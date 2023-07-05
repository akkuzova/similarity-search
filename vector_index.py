import faiss
import numpy as np
from typing import List
import os

INDEX_TYPE = "IDMap,IVF1,Flat"
INDEX_DATA_FOLDER = './index_data/'


class VectorIndex:
    def __init__(self, index_id: str):
        self._index_id = index_id
        self._index = None
        if not os.path.exists(INDEX_DATA_FOLDER):
            os.makedirs(INDEX_DATA_FOLDER)

    def get_vector_count(self) -> int:
        return self._index.ntotal if self._index else None

    def get_vector_dimension(self) -> int:
        return self._index.d if self._index else None

    def get_metric_type(self) -> int:
        return self._index.metric_type if self._index else None

    def is_trained(self) -> bool:
        return self._index.is_trained if self._index else False

    def is_loaded(self) -> bool:
        return self._index is not None

    def get_index_id(self) -> str:
        return self._index_id

    def get_info(self) -> dict:
        return {
            'index_id': self._index_id,
            'vector dimension': self._index.d,
            'vector count': self.get_vector_count(),
            'is trained': self.is_trained(),
            'metric type': self.get_metric_type(),
            'is loaded': self.is_loaded()
        }

    def build(self, _dictionary: dict):
        _vectors = np.array(list(_dictionary.values()))
        _ids = np.array(list(_dictionary.keys()))
        dimension = _vectors[0].shape[0]
        self._index = faiss.index_factory(dimension, INDEX_TYPE)
        self._index.train(_vectors)
        self._index.add_with_ids(_vectors, _ids)

        faiss.write_index(self._index, f'{INDEX_DATA_FOLDER}{self._index_id}.index')
        return self

    def load(self):
        filename = f'{INDEX_DATA_FOLDER}{self._index_id}.index'
        self._index = faiss.read_index(filename)
        return self

    def search(self, xq, k: int) -> (List, List):
        return self._index.search(xq.reshape(1, -1).astype(np.float32), k)
