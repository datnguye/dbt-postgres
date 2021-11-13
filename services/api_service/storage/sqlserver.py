from datetime import datetime, timedelta
from typing import Any
from sqlalchemy.sql.expression import desc
from storage.model import DbtLog
from storage.base import BaseStorage
from sqlmodel import Session, SQLModel, create_engine, select
from prefect.engine.state import Pending, Running, State, Success, TriggerFailed
from config import settings

class SqlServerStorage(BaseStorage):
    def __init__(self, storage_config: dict = None) -> None:
        super().__init__(storage_config=storage_config)
        self.engine = create_engine(
            url="mssql+pyodbc://{user}:{password}@{server}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"\
                .format(
                    user=self.storage_config['user'],
                    password=self.storage_config['password'],
                    server=self.storage_config['server'],
                    port=self.storage_config['port'],
                    database=self.storage_config['database']
                ),
            echo=settings.DEBUG # shouldn't be enabled in prod
        )
        SQLModel.metadata.create_all(
            bind=self.engine
        )

    
    def __migration__(self):
        """
        Schema mirgration
        """
        raise "Not yet impletmented"


    def save(self, id: str, data: State) -> bool:
        """
        Save task status
        """
        with Session(bind=self.engine) as session:
            session.add(DbtLog(TaskId=id, Data=str(data)))
            session.commit()

        return True

    
    def get(self, id) -> State:
        """
        Get task status
        """
        with Session(bind=self.engine) as session:
            statement = select(DbtLog)\
                        .where(DbtLog.TaskId == id)\
                        .order_by(desc(DbtLog.Timestamp))\
                        .limit(1)
            result = session.exec(statement).first()

            if not result:
                return TriggerFailed(message=f"ID: {id} Not found")
            if "success" in result.Data.lower():
                return Success(message=result.Data)
            if "running" in result.Data.lower():
                return Running(message=result.Data)
            
            return Pending(message=result.Data)


    def maintenance(self, log_retention_day: int = 30):
        """
        Run maintenance:
        - Log retention
        """
        with Session(bind=self.engine) as session:
            penalty_date = datetime.utcnow() - timedelta(days=log_retention_day)
            statement = select(DbtLog).where(DbtLog.Timestamp < penalty_date)
            deletes = session.exec(statement)

            if deletes:
                for delete in deletes:
                    session.delete(delete)
                session.commit()
        