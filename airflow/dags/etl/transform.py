import os
import json
import glob
import duckdb
from datetime import datetime
from dotenv import load_dotenv

def setup_env():
    load_dotenv('/opt/airflow/.env')
    landing_path = os.getenv("LANDING_PATH", "data/landing")
    bronze_path = os.getenv("BRONZE_PATH", "data/bronze")
    return landing_path, bronze_path

def transformar_json_para_parquet(schema: str, tabela: str):
    landing_path, bronze_path = setup_env()

    arquivos_json = glob.glob(os.path.join(landing_path, schema, tabela, "**/*.json"), recursive=True)

    if not arquivos_json:
        print(f"[{schema}.{tabela}] Nenhum arquivo JSON encontrado.")
        return

    for caminho_json in arquivos_json:
        print(f"[{schema}.{tabela}] Processando: {caminho_json}")
        with open(caminho_json, "r", encoding="utf-8") as f:
            dados = json.load(f)

        if not isinstance(dados, list):
            print(f"[{schema}.{tabela}] Formato inválido no arquivo: {caminho_json}")
            continue

        # controle de carga
        timestamp = datetime.now()
        data_carga = timestamp.strftime("%Y-%m-%d")
        data_hora_carga = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        for item in dados:
            item["data_carga"] = data_carga
            item["data_hora_carga"] = data_hora_carga

        temp_json_path = caminho_json.replace(".json", "_temp.json")
        with open(temp_json_path, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

        con = duckdb.connect()
        con.execute("INSTALL json; LOAD json;")
        con.execute("CREATE TABLE temp AS SELECT * FROM read_json_auto(?)", [temp_json_path])

        ano, mes, dia = timestamp.strftime("%Y"), timestamp.strftime("%m"), timestamp.strftime("%d")
        destino = os.path.join(bronze_path, schema, tabela, f"ano={ano}", f"mes={mes}", f"dia={dia}")
        os.makedirs(destino, exist_ok=True)

        nome_arquivo = f"{tabela}_{timestamp.strftime('%Y%m%d_%H%M%S')}.parquet"
        caminho_parquet = os.path.join(destino, nome_arquivo)

        con.execute(f"COPY temp TO '{caminho_parquet}' (FORMAT 'parquet')")
        con.close()

        print(f"[{schema}.{tabela}] Parquet salvo em: {caminho_parquet}")

        os.remove(caminho_json)
        os.remove(temp_json_path)
        print(f"[{schema}.{tabela}] JSON apagado: {caminho_json}")

if __name__ == "__main__":
    landing_path, bronze_path = setup_env()
    transformar_json_para_parquet(
        schema=os.getenv("SCHEMA", "clima_pluviometro"),
        tabela=os.getenv("TABELA", "precipitacao_24h"),
    )
