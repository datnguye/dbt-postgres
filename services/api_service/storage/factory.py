from storage.postgres import PostgresStorage
from storage.sqlserver import SqlServerStorage
from storage.base import BaseStorage
from storage.pickle import PickleStorage
from storage.type import StorageType


class StorageFactory(object):
    def __init__(self, base: BaseStorage) -> None:
        super().__init__()
        self.base = base

    
    def get_storage_instance(self):
        if self.base.type is None:
            return self.base

        if self.base.type == StorageType.PICKLE.value:
            return PickleStorage(self.base.storage_config)

        if self.base.type == StorageType.SQLSERVER.value:
            return SqlServerStorage(self.base.storage_config)

        if self.base.type == StorageType.POSTGRES.value:
            return PostgresStorage(self.base.storage_config)