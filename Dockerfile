FROM apache/airflow:latest

USER ARIFLOW

RUN pip install apache-airflow-providers-docker \
    && pip install apahce.airflow-providers-http \
    && pip install apahce.airflow-providers-airbyte

USER ROOT
