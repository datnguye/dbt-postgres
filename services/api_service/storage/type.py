from enum import Enum


class StorageType(Enum):
    """
    Supported storage type
    """
    PICKLE = 'pickle'
    SQLSERVER = 'sqlserver'
    POSTGRES = 'postgres'