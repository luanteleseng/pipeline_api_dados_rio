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

dag_1 = criar_dag(
    dag_id="clima_pluviometro_precipitacao_24h",
    url="https://api.dados.rio/v2/clima_pluviometro/precipitacao_24h/",
    schema="clima_pluviometro",
    tabela="precipitacao_24h",
    descricao="Ingestão de dados de chuva (24h).",
    tags=["precipitacao", "clima"],
    schedule=None,
    start_date=datetime(2025, 4, 26)
)

# dag_pluv_ultima_atualizacao = criar_dag(
#     dag_id="clima_pluviometro_ultima_atualizacao_precipitacao_24h",
#     url="https://api.dados.rio/v2/clima_pluviometro/ultima_atualizacao_precipitacao_24h/",
#     schema="clima_pluviometro",
#     tabela="ultima_atualizacao_precipitacao_24h",
#     descricao="Ingestão de dados de chuva (24h) - ultima atualizacao.",
#     tags=["precipitacao", "clima_pluviometro"],
#     schedule=None,
#     start_date=datetime(2025, 4, 26)
# )

dag_15min = criar_dag(
    dag_id="clima_pluviometro_precipitacao_15min",
    url="https://api.dados.rio/v2/clima_pluviometro/precipitacao_15min/",
    schema="clima_pluviometro",
    tabela="precipitacao_15min",
    descricao="Ingestão de dados de chuva (15min).",
    tags=["precipitacao", "clima_pluviometro"],
    schedule=None,
    start_date=datetime(2025, 4, 26)
)

dag_2 = criar_dag(
    dag_id="clima_pluviometro_precipitacao_30min",
    url="https://api.dados.rio/v2/clima_pluviometro/precipitacao_30min/",
    schema="clima_pluviometro",
    tabela="precipitacao_30min",
    descricao="Ingestão de dados de chuva (30min).",
    tags=["precipitacao", "clima_pluviometro"],
    schedule=None,
    start_date=datetime(2025, 4, 26)
)

dag_pluv_3 = criar_dag(
    dag_id="clima_pluviometro_precipitacao_120min",
    url="https://api.dados.rio/v2/clima_pluviometro/precipitacao_120min/",
    schema="clima_pluviometro",
    tabela="precipitacao_120min",
    descricao="Ingestão de dados de chuva (120min).",
    tags=["precipitacao", "clima_pluviometro"],
    schedule=None,
    start_date=datetime(2025, 4, 26)
)

dag_pluv_4 = criar_dag(
    dag_id="clima_pluviometro_precipitacao_6h",
    url="https://api.dados.rio/v2/clima_pluviometro/precipitacao_6h/",
    schema="clima_pluviometro",
    tabela="precipitacao_6h",
    descricao="Ingestão de dados de chuva (6h).",
    tags=["precipitacao", "clima_pluviometro"],
    schedule=None,
    start_date=datetime(2025, 4, 26)
)

dag_pluv_12 = criar_dag(
    dag_id="clima_pluviometro_precipitacao_12h",
    url="https://api.dados.rio/v2/clima_pluviometro/precipitacao_12h/",
    schema="clima_pluviometro",
    tabela="precipitacao_12h",
    descricao="Ingestão de dados de chuva (12h).",
    tags=["precipitacao", "clima_pluviometro"],
    schedule=None,
    start_date=datetime(2025, 4, 26)
)

dag_pluv_96 = criar_dag(
    dag_id="clima_pluviometro_precipitacao_96h",
    url="https://api.dados.rio/v2/clima_pluviometro/precipitacao_96h/",
    schema="clima_pluviometro",
    tabela="precipitacao_96h",
    descricao="Ingestão de dados de chuva (96h).",
    tags=["precipitacao", "clima_pluviometro"],
    schedule=None,
    start_date=datetime(2025, 4, 26)
)