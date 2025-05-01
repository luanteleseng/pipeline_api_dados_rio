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

dag_ocorrencias = criar_dag(
    dag_id="adm_cor_comando_ocorrencias",
    url="https://api.dados.rio/v2/adm_cor_comando/ocorrencias/",
    schema="adm_cor_comando",
    tabela="ocorrencias",
    descricao="Informações sobre ocorrências urbanas registradas na cidade do Rio de Janeiro.",
    tags=["adm", "ocorrencias"],
    schedule=None,
    start_date=datetime(2025, 4, 30)
)

dag_ocorrencias_abertas = criar_dag(
    dag_id="adm_cor_comando_ocorrencias_abertas",
    url="https://api.dados.rio/v2/adm_cor_comando/ocorrencias_abertas/",
    schema="adm_cor_comando",
    tabela="ocorrencias_abertas",
    descricao="Informações sobre ocorrências urbanas abertas na cidade do Rio de Janeiro.",
    tags=["adm", "ocorrencias"],
    schedule=None,
    start_date=datetime(2025, 4, 30)
)

dag_ocorrencias_orgaos_responsaveis = criar_dag(
    dag_id="adm_cor_comando_ocorrencias_orgaos_responsaveis",
    url="https://api.dados.rio/v2/adm_cor_comando/ocorrencias_orgaos_responsaveis/",
    schema="adm_cor_comando",
    tabela="ocorrencias_orgaos_responsaveis",
    descricao="Informações sobre órgãos responsáveis das ocorrências urbanas da cidade do Rio de Janeiro.",
    tags=["adm", "ocorrencias"],
    schedule=None,
    start_date=datetime(2025, 4, 30)
)