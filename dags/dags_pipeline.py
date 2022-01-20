from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
import airflow

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    'scraping_price_ecommerce',
    default_args=default_args,
    description='a DAG is used to create table in postgresql, scraping from ecommerce website and doing simple ETL to DW',
    schedule_interval=timedelta(days=1)
)

start = DummyOperator(task_id='start',dag=dag)

task_1 = KubernetesPodOperator(
    name='pod1',
    namespace='airflow',
    dag=dag,
    task_id='docker_task_1_create_table',
    image='hamihami/main:2.1',
    is_delete_operator_pod=False,
    in_cluster=True,
    get_logs=True
)

task_2 = KubernetesPodOperator(
    name='pod2',
    namespace='airflow',
    dag=dag,
    task_id='docker_task_2_scraping',
    image='hamihami/scraping:2.3',
    is_delete_operator_pod=False,
    in_cluster=True,
    get_logs=True,
)

task_3 = KubernetesPodOperator(
    name='pod3',
    namespace='airflow',
    dag=dag,
    task_id='docker_task_3_etl',
    image='hamihami/etl:2.1',
    is_delete_operator_pod=False,
    in_cluster=True,
    get_logs=True
)
start >> task_1 >> task_2 >> task_3
