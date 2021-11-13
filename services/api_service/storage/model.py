from sqlalchemy.sql.schema import MetaData
from sqlmodel import Field, SQLModel
from datetime import datetime
from uuid import UUID, uuid4


class DbtLog(SQLModel, table=True):
    """
    Table: __Dbt_Log
    """
    __tablename__ = "__Dbt_Log"

    Id: UUID = Field(default_factory=uuid4, primary_key=True)
    TaskId: str = Field(max_length=128)
    Data: str = Field(index=False)
    Timestamp: datetime = Field(index=False, default_factory=datetime.utcnow)