import faiss
import numpy as np


class TextIndex:
    INDEX_TYPE = "IDMap,IVF2,Flat"
    DEFAULT_DIMENSION = 1536

    def __init__(self):
        self.D = self.DEFAULT_DIMENSION
        self._index = faiss.index_factory(self.D, self.INDEX_TYPE)

    def get_vector_count(self):
        return self._index.ntotal

    def get_vector_dimension(self):
        return self.D

    def build_index(self, _dictionary):
        _vectors = np.array(list(_dictionary.values()))
        _ids = np.array(list(_dictionary.keys()))
        self.D = _vectors[0].shape[0]
        if self.DEFAULT_DIMENSION != self.D:
            self._index = faiss.index_factory(self.D, self.INDEX_TYPE)
        self._index.train(_vectors)
        self._index.add_with_ids(_vectors, _ids)

        faiss.write_index(self._index, 'index_file')

    def search(self, xq, k):
        return self._index.search(xq.reshape(1, -1).astype(np.float32), k)
