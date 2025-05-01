import os
import glob
import duckdb
from dotenv import load_dotenv

def setup_env():
    load_dotenv('/opt/airflow/.env')
    bronze_path = os.getenv("BRONZE_PATH") or "data/bronze"
    duckdb_path = os.getenv("DUCKDB_PATH") or "data/db/duckdb_database.db"
    return bronze_path, duckdb_path

def carregar_parquets_para_duckdb():
    bronze_path, duckdb_path = setup_env()
    con = duckdb.connect(duckdb_path)

    for schema in os.listdir(bronze_path):
        schema_path = os.path.join(bronze_path, schema)
        if not os.path.isdir(schema_path):
            continue

        con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")

        for tabela in os.listdir(schema_path):
            caminho_tabela = os.path.join(schema_path, tabela)
            arquivos_parquet = glob.glob(os.path.join(caminho_tabela, "**/*.parquet"), recursive=True)

            if not arquivos_parquet:
                print(f"[{schema}.{tabela}] Nenhum Parquet encontrado.")
                continue

            print(f"[{schema}.{tabela}] Recriando tabela...")

            con.execute(f"DROP TABLE IF EXISTS {schema}.{tabela}")
            con.execute(f"""
                CREATE TABLE {schema}.{tabela} AS
                SELECT * FROM read_parquet('{caminho_tabela}/**/*.parquet')
            """)

            print(f"[{schema}.{tabela}] Tabela criada e carregada.")

    con.close()

if __name__ == "__main__":
    carregar_parquets_para_duckdb()
