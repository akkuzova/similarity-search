from index_manager import IndexManager


class Controller:
    _index_manager = IndexManager()

    def get_index_info(self, index_id: str) -> dict:
        return self._index_manager.get_index_info(index_id)

    def create_index(self, index_id: str, vectors: dict) -> dict:
        return self._index_manager.create_index(vectors, index_id)

    def search(self, index_id: str, request_json: dict) -> dict:
        xq = list(request_json['xq'])
        k = int(request_json['k'])
        return self._index_manager.search(index_id, xq, k)
