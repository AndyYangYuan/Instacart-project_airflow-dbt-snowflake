from airflow import DAG
import os
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022,7,29),
    'retries': 0
}


def print_context():
    """Print the Airflow context and ds variable from the context."""
    print(os.getcwd())
    print(os.listdir(os.getcwd()))



with DAG('pipeline',default_args=default_args) as dag:
    task_1 = PythonOperator(
        task_id='start_task',
        python_callable=print_context,
        dag=dag
    )

    task_2 = S3ToSnowflakeOperator(
        task_id='load_orders_into_snowflake',
        s3_keys=['orders.csv'],
        stage='S3O',
        table='orders',
        schema='raw',
        file_format='orders_demo',
        role='sysadmin',
        snowflake_conn_id = 'andy_snowflake_conn',
        dag=dag
    )

    task_3 = S3ToSnowflakeOperator(
        task_id='load_orders_products_into_snowflake',
        s3_keys=['order_products__prior.csv.gz'],
        stage='S3OP',
        table='orders_products',
        schema='raw',
        file_format='orders_products_demo',
        role='sysadmin',
        snowflake_conn_id = 'andy_snowflake_conn',
        dag=dag
    )

    task_4 = BashOperator(
        task_id='run_dbt',
        bash_command='cd && cd /usr/local/airflow/dags/dbt/imba_project && /usr/local/airflow/.local/bin/dbt run --profiles-dir /usr/local/airflow/dags/dbt',
        dag=dag
    )


task_1 >> task_2 >> task_3 >> task_4