import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

def setup_env():
    load_dotenv('/opt/airflow/.env')
    landing_path = os.getenv("LANDING_PATH", "data/landing")
    timeout = int(os.getenv("TIMEOUT", "10"))
    return landing_path, timeout

def extrair_dados(url: str, schema: str, tabela: str):
    landing_path, timeout = setup_env()

    agora = datetime.now()
    path_particionado = os.path.join(
        landing_path, schema, tabela,
        f"ano={agora.year}", f"mes={agora.month:02}", f"dia={agora.day:02}"
    )
    os.makedirs(path_particionado, exist_ok=True)

    nome_arquivo = f"{tabela}_{agora.strftime('%Y%m%d_%H%M%S')}.json"
    caminho_arquivo = os.path.join(path_particionado, nome_arquivo)

    try:
        print(f"Extraindo dados da URL: {url}")
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        dados = response.json()

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

        print(f"Dados salvos em: {caminho_arquivo}")

    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha na extração: {e}")

if __name__ == "__main__":
    # Teste local
    landing_path, timeout = setup_env()
    extrair_dados(
        url=os.getenv("API_ENDPOINT", "https://api.dados.rio/v2/clima_pluviometro/precipitacao_15min/"),
        dominio=os.getenv("DOMINIO", "clima_pluviometro"),
    )
