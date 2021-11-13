from datetime import datetime, timedelta
import json
import os
import subprocess
import threading
import prefect
from enum import Enum
from queue import Queue
from prefect import Flow, Task
from prefect.engine.state import Pending, Running
from prefect.schedules.schedules import IntervalSchedule
from config import settings
from storage.factory import StorageFactory
from storage.base import BaseStorage
from storage.type import StorageType

class DbtAction(Enum):
    DEPS = 'deps'
    RUN = 'run'
    SEED = 'seed'
    TEST = 'test'
    RUN_OPERATION = 'run-operation'


class DBT():
    def __init__(self,
        taskid: str = "UNKOWN_TASKID",
        action: str = DbtAction.RUN.value,
        macro: str = None,
        macro_args: dict = None,
        profiles_dir: str = None,
        target: str = None,
        project_dir: str = '.',
        vars: dict = None,
        models: str = None,
        full_refresh: bool = False,
        args: list = [],
        kwargs: list = []
    ) -> None:
        self.taskid = taskid
        self.action = action
        self.macro = macro
        self.macro_args = macro_args
        self.profiles_dir = profiles_dir
        self.target = target
        self.project_dir = project_dir
        self.vars = vars
        self.models = models
        self.full_refresh = full_refresh
        self.args = args
        self.kwargs = kwargs
    
    
    def build(self):
        """
        Build args
        """
        arguments = [self.action]

        # Standard arguments
        if self.macro is not None:
            arguments.extend([self.macro])

            if self.macro_args is not None:
                arguments.extend(["--args", json.dumps(self.macro_args)])

        if self.target is not None:
            arguments.extend(["--target", self.target])

        if self.profiles_dir is not None:
            arguments.extend(["--profiles-dir", self.profiles_dir])

        if self.project_dir is not None:
            arguments.extend(["--project-dir", self.project_dir])

        if self.vars is not None:
            arguments.extend(["--vars", json.dumps(self.vars)])

        if self.models is not None:
            arguments.extend(["--models", self.models])

        if self.full_refresh:
            arguments.extend(["--full-refresh"])

        # Additional non-keyword arguments
        if self.args:
            arguments.extend(self.args)

        # Additional keyword arguments
        if self.kwargs:
            for key, value in self.kwargs:
                arguments.extend([key, value])

        return arguments


class DbtTask(Task):
    def __set_var__(self):
        """
        Initiate enviroment variables
        """
        if settings.DBT_STORAGE["type"] == StorageType.SQLSERVER.value:
            os.environ["ENV_DBT_SERVER"] = settings.DBT_STORAGE["server"]
            os.environ["ENV_DBT_PORT"] = str(settings.DBT_STORAGE["port"])
            os.environ["ENV_DBT_DATABASE"] = settings.DBT_STORAGE["database"]
            os.environ["ENV_DBT_SCHEMA"] = settings.DBT_STORAGE.get("schema", None) or "dbo"
            os.environ["ENV_DBT_USER"] = settings.DBT_STORAGE["user"]
            os.environ["ENV_DBT_PASSWORD"] = settings.DBT_STORAGE["password"]

        if settings.DBT_STORAGE["type"] == StorageType.POSTGRES.value:
            os.environ["POSTGRES_HOST"] = settings.DBT_STORAGE["server"]
            os.environ["POSTGRES_PORT"] = str(settings.DBT_STORAGE["port"])
            os.environ["POSTGRES_DB"] = settings.DBT_STORAGE["database"]
            os.environ["POSTGRES_SCHEMA"] = settings.DBT_STORAGE.get("schema", None) or "dbo"
            os.environ["POSTGRES_USER"] = settings.DBT_STORAGE["user"]
            os.environ["POSTGRES_PASS"] = settings.DBT_STORAGE["password"]


        
    def __del_var__(self):
        """
        Clean up the enviroment variables
        """
        if settings.DBT_STORAGE["type"] == StorageType.SQLSERVER.value:
            del os.environ["ENV_DBT_SERVER"]
            del os.environ["ENV_DBT_PORT"]
            del os.environ["ENV_DBT_DATABASE"]
            del os.environ["ENV_DBT_SCHEMA"]
            del os.environ["ENV_DBT_USER"]
            del os.environ["ENV_DBT_PASSWORD"]

        if settings.DBT_STORAGE["type"] == StorageType.POSTGRES.value:
            del os.environ["POSTGRES_HOST"]
            del os.environ["POSTGRES_PORT"]
            del os.environ["POSTGRES_DB"]
            del os.environ["POSTGRES_SCHEMA"]
            del os.environ["POSTGRES_USER"]
            del os.environ["POSTGRES_PASS"]


    def run(self, instance: DBT):
        """
        Run dbt in subprocess
        """
        logger = prefect.context.get("logger")
        self.__set_var__()

        dbt_cmd = ["dbt"]
        dbt_cmd.extend(instance.build())
        logger.info(dbt_cmd)
        sp = subprocess.Popen(
            dbt_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=os.getcwd(),
            close_fds=True
        )
        logs = ''
        for line in iter(sp.stdout.readline, b''):
            line = line.decode('utf-8').rstrip()
            logger.info(line)
            logs = f"{logs}\n{line}"
        sp.wait()
        if sp.returncode != 0:
            raise prefect.engine.signals.FAIL()

        self.__del_var__()

        return (
            f"Command exited with return code {sp.returncode}",
            logs,
            sp.returncode == 0
        )


class DbtExec():
    def __init__(self, singleton: bool = True) -> None:
        self.singleton = singleton
        self.queue = Queue(maxsize=100) # Config max size
        if self.singleton:
            threading.Thread(target=self.__run_flow_worker__, daemon=True).start()
        self.log_storage = StorageFactory(base=BaseStorage(settings.LOG_STORAGE)).get_storage_instance()
        if self.log_storage:
            threading.Thread(target=self.__maintenance_worker__, daemon=True).start()


    def __maintenance_worker__(self):
        """"
        Maintenance worker
        """
        schedule = IntervalSchedule(
            start_date=datetime.utcnow() + timedelta(seconds=1),
            interval=timedelta(days=1)
        )
        with Flow("Dbt Maintenance", schedule=schedule) as flow:
            log_task = self.log_storage.maintenance()
            
        flow.run()


    def __run_flow_worker__(self):
        """"
        Queue worker - Running flow in queue if configured
        """
        while True:
            flow_id, flow = self.queue.get()
            print(f'Working on {flow}')
            self.__run_flow__(flow_id=flow_id, flow=flow)
            print(f'Finished {flow}')
            self.queue.task_done()

    
    def __run_flow__(self, flow_id: str, flow: Flow):
        """
        Run a flow
        """
        self.log_storage.save(id=flow_id, data=Running(message=f"Task:{flow_id} is running"))
        state = flow.run()
        self.log_storage.save(id=flow_id, data=state)

    
    def get_execution_state(self, taskid: str = None):
        """
        Get state of an execution
        """
        return self.log_storage.get(id=taskid)


    def execute(self,
        flow_name: str = "Execution of dbt series | execute",
        dbts: list = [],
        taskid: str = None
    ):
        """
        General dbt execution
        """
        self.log_storage.save(id=taskid, data=Pending(message=f"Task:{taskid} is in queue"))

        dbt_tasks = [DbtTask(name=f"Flow:{taskid} - Task:{idx}") for idx, x in enumerate(dbts)]
        with Flow(name=flow_name) as f:
            prev_task = None
            for idx, dbt in enumerate(dbts):
                task = f.add_task(dbt_tasks[idx](instance=dbt))
                if prev_task is not None:
                    task.set_dependencies(upstream_tasks=[prev_task])
                prev_task = task

        if self.singleton:
            self.queue.put((taskid, f))
            return "Task queued"

        return self.__run_flow__(flow_id=taskid, flow=f)


instance = DbtExec(singleton=settings.DBT_SINGLETON)