from typing import Any


class BaseStorage():
    def __init__(self, storage_config: dict = None) -> None:
        self.storage_config = storage_config
        self.type = self.storage_config["type"] \
            if self.storage_config else None
        

    def save(self, id: str, data: Any) -> bool:
        raise Exception("Not yet implemented")
    
    
    def get(self, id) -> Any:
        raise Exception("Not yet implemented")
        

    def maintenance(self, log_retention_day: int = 30) -> bool:
        return True