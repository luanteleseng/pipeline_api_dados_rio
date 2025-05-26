# pipeline_api_dados_rio

Este projeto é uma pipeline ETL que consome dados públicos da API Dados.Rio, organiza as informações e prepara os dados para análises futuras.

## Objetivo
Extrair dados de diferentes endpoints da API Dados.Rio, realizar transformações e armazenar em um formato estruturado, pronto para uso em visualizações e monitoramentos.

## Tecnologias utilizadas

- **Docker**
- **Apache Airflow**
- **DuckDB**
- **Python**
- **Streamlit**
  
## Estrutura do projeto

```
pipeline_api_dados_rio/
├── airflow/
│   ├── dags/
│   │   ├── adm_cor_comando.py
│   │   ├── clima_alagamento.py
│   │   ├── clima_pluviometro.py
│   │   ├── clima_radar.py
│   │   └── vision_ai.py
│   ├── etl/
│   │   ├── __init__.py
│   │   ├── extract.py
│   │   ├── load.py
│   │   ├── transform.py
│   │   └── utils.py
├── data/
│   ├── bronze/
│   │   ├── clima_alagamento/
│   │   ├── clima_pluviometro/
│   │   └── clima_radar/
│   └── db/
│       └── duckdb_database.db
├── logs/
├── config/
│   └── .env
├── streamlit/
│   └── app.py
├── docker-compose.yml
├── requirements.txt
└── README.md

```
