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

pipeline_api_dados_rio/
├── dags/ # Workflows do Airflow organizados por tema
│ ├── clima/
│ ├── vision_ai/
│ └── adm_cor_comando/
├── scripts/ # Scripts de transformação e utilitários
├── data/ # Armazenamento dos dados locais
│ ├── raw/ # Dados brutos
│ └── processed/ # Dados limpos e organizados
├── streamlit_app/ # Aplicação de visualização interativa
├── utils/ # Funções auxiliares
├── requirements.txt # Dependências Python
├── docker-compose.yml # Configuração do ambiente Docker + Airflow
└── README.md # Descrição do projeto
