from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/opt/airflow/dags/etl')

from etl.extract import extrair_dados
from etl.transform import transformar_json_para_parquet
from etl.load import carregar_parquets_para_duckdb
from etl.utils import limpar_arquivos_antigos

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

def criar_dag(dag_id, url, schema, tabela, descricao, tags, schedule, start_date):
    with DAG(
        dag_id=dag_id,
        default_args=default_args,
        description=descricao,
        schedule_interval=schedule,
        start_date=start_date,
        catchup=False,
        tags=tags,
    ) as dag:

        extrair = PythonOperator(
            task_id=f"extrair_dados_{tabela}",
            python_callable=extrair_dados,
            op_kwargs={"url": url, "schema": schema, "tabela": tabela},
        )

        transformar = PythonOperator(
            task_id=f"transformar_dados_{tabela}",
            python_callable=transformar_json_para_parquet,
            op_kwargs={"schema": schema, "tabela": tabela},
        )

        carregar = PythonOperator(
            task_id=f"carregar_dados_{tabela}",	
            python_callable=carregar_parquets_para_duckdb,
        )

        extrair >> transformar >> carregar

    return dag

dag_alagamento_1 = criar_dag(
    dag_id="clima_alagamento_alagamento_120min",
    url="https://api.dados.rio/v2/clima_alagamento/alagamento_120min/",
    schema="clima_alagamento",
    tabela="alagamento_120min",
    descricao="Ingestão de dados de alagamento (120min).",
    tags=["alagamento", "clima_alagamento"],
    schedule=None,
    start_date=datetime(2025, 4, 30)
)

dag_alagamento_3 = criar_dag(
    dag_id="clima_alagamento_alagamento_15min",
    url="https://api.dados.rio/v2/clima_alagamento/alagamento_15min/",
    schema="clima_alagamento",
    tabela="alagamento_15min",
    descricao="Ingestão de dados de alagamento (15min).",
    tags=["alagamento", "clima_alagamento"],
    schedule=None,
    start_date=datetime(2025, 4, 30)
)

dag_alagamento_2 = criar_dag(
    dag_id="clima_alagamento_alagamento_detectado_ia",
    url="https://api.dados.rio/v2/clima_alagamento/alagamento_detectado_ia/",
    schema="clima_alagamento",
    tabela="alagamento_detectado_ia",
    descricao="Ingestão de dados de alagamento (detectado_ia).",
    tags=["alagamento", "clima_alagamento"],
    schedule=None,
    start_date=datetime(2025, 4, 30)
)