from pydantic import BaseSettings
import os
from libs.yml_helper import load_yaml_text
from libs.object_view import ObjectView
from storage.type import StorageType


def load___config___config():
    """
    Load __config__ial config
    """
    with open(
            f"{os.path.dirname(os.path.realpath(__file__))}/config.yml"
        ) as __config___file:
        return load_yaml_text(__config___file)
__config__ = load___config___config()

class Settings(BaseSettings):
    """
    All API service settings
    """
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Awesome dbt"
    
    DEBUG = bool(__config__.debug)
    DBT_SINGLETON = __config__.dbt.singleton
    DBT_TARGET = __config__.dbt.target
    DBT_PROJECT_DIR = __config__.dbt.project_dir

    def __get_log_storage__(type: str):
        """
        Get storage configuration dict
        """
        if type == StorageType.PICKLE.value:
            return dict(
                type=type,
                path=__config__.log_storage[0].path
            )

        if type == StorageType.SQLSERVER.value:
            return dict(
                type=type,
                server=os.environ[__config__.log_storage[0].server],
                port=__config__.log_storage[0].port or 1433,
                database=__config__.log_storage[0].database,
                user=os.environ[__config__.log_storage[0].user],
                password=os.environ[__config__.log_storage[0].password]
            )

        if type == StorageType.POSTGRES.value:
            return dict(
                type=type,
                server=os.environ[__config__.log_storage[0].server],
                port=__config__.log_storage[0].port or 1433,
                database=__config__.log_storage[0].database,
                user=os.environ[__config__.log_storage[0].user],
                password=os.environ[__config__.log_storage[0].password]
            )

        return None
    LOG_STORAGE = None
    if __config__.log_storage and len(__config__.log_storage) > 0:
        type = __config__.log_storage[0].type
        LOG_STORAGE = __get_log_storage__(type=type)


    def __get_dbt_storage__(type: str):
        """
        Get dbt storage configuration dict
        """
        if type == StorageType.SQLSERVER.value:
            return dict(
                type=type,
                server=os.environ[__config__.dbt.storage[0].server],
                port=__config__.dbt.storage[0].port or 1433,
                database=__config__.dbt.storage[0].database,
                schema=__config__.dbt.storage[0].schema,
                user=os.environ[__config__.dbt.storage[0].user],
                password=os.environ[__config__.dbt.storage[0].password]
            )

        if type == StorageType.POSTGRES.value:
            return dict(
                type=type,
                server=os.environ[__config__.dbt.storage[0].server],
                port=__config__.dbt.storage[0].port or 5432,
                database=__config__.dbt.storage[0].database,
                schema=__config__.dbt.storage[0].schema,
                user=os.environ[__config__.dbt.storage[0].user],
                password=os.environ[__config__.dbt.storage[0].password]
            )

        raise "Not support dbt storage"
    DBT_STORAGE = None
    if __config__.dbt.storage and len(__config__.dbt.storage) > 0:
        type = __config__.dbt.storage[0].type
        DBT_STORAGE = __get_dbt_storage__(type=type)


settings = Settings()
