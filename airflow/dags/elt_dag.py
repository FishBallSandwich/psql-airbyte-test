from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

CONN_ID = ""

"""
def run_elt_script():
    script_path = "/opt/airflow/elt/elt_script.py"
    result = subprocess.run(["python", script_path],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)
"""




dag = DAG(
    dag_id = 'elt_dag',
    default_args = default_args,
    description = 'ELT DAG',
    start_date = datetime(2024, 12, 8),
    catchup = False)


"""
t1 = PythonOperator(
    task_id="run_elt_script",
    python_callable = run_elt_script,
    dag = dag)
"""

t1 = AirbyteTriggerSyncOperator(
    task_id="airbyte_postgres_postgres",
    airbyte="airbyte",
    connection_id=CONN_ID,
    asynchronous=False,
    timeout=3600,
    wait_second=3,
    dag=dag
)


t2 = DockerOperator(
    task_id = "dbt_run",
    image ='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command=[
        "run"
    ],
    auto_remove = True,
    docker_url = "unix://var/run/docker.sock",
    network_mode = "bridge",
    mount_tmp_dir=False,
    mounts = [
        Mount(source='c:/Users/repos/elt_project/custom_postgres', target='/usr/app',type='bind'),
        Mount(source='c:/Users/.dbt', target='/root/.dbt', type='bind'),
    ],
    dag=dag
)


t1 >> t2