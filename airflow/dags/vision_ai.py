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

dag_5 = criar_dag(
    dag_id="vision_ai_ultima_atualizacao_cameras",
    url="https://api.dados.rio/v2/vision_ai/ultima_atualizacao_cameras/",
    schema="vision_ai",
    tabela="ultima_atualizacao_cameras",
    descricao="Ultima atualização de informações geradas por inteligência artificial a partir de câmeras instaladas na cidade.",
    tags=["inteligencia artificial", "cameras", "vision_ai"],
    schedule=None,
    start_date=datetime(2025, 4, 30)
)

dag_6 = criar_dag(
    dag_id="vision_ai_cameras",
    url="https://api.dados.rio/v2/vision_ai/cameras/",
    schema="vision_ai",
    tabela="cameras",
    descricao="Informações geradas por inteligência artificial a partir de câmeras instaladas na cidade.",
    tags=["inteligencia artificial", "cameras", "vision_ai"],
    schedule=None,
    start_date=datetime(2025, 4, 30)
)
