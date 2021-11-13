from typing import Any
from prefect.engine.state import State, TriggerFailed
from storage.base import BaseStorage
import pickle


class PickleStorage(BaseStorage):
    def __init__(self, storage_config: dict) -> None:
        super().__init__(storage_config=storage_config)
        self.path = storage_config["path"]
        self.file_path = f'{self.path}{self.type}_{{id}}.pickle'


    def save(self, id: str, data: State) -> bool:
        """
        Save data to a pickle file
        """
        try:
            with open(self.file_path.format(id=id), 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            return False
        return True



    def get(self, id) -> State:
        """
        Get data from a pickle file
        """
        try:
            with open(self.file_path.format(id=id), 'rb') as handle:
                return pickle.load(handle)
        except Exception as e:
            return TriggerFailed(message=f"ID: {id} Not found")