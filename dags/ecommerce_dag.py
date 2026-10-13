import os
import glob
import json
import datetime
import pandas as pd
from sqlalchemy import create_engine
from extractors.extract_products import extract_data
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

def load_to_postgresql():
    engine = create_engine("postgresql://airflow:airflow@postgres:5432/airflow")
    search_path = "/opt/airflow/data/raw/products/**/*.json"
    list_of_files = glob.glob(search_path, recursive=True)
    
    if not list_of_files:
        raise FileNotFoundError("No raw JSON files found in data/raw/")
    
    latest_file = max(list_of_files, key=os.path.getctime)
    
    df = pd.read_json(latest_file)
    
    for col in df.columns:
        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, (dict)) else x)
    
    with engine.begin() as conn:
        conn.exec_driver_sql("TRUNCATE TABLE raw_products;")
    
    df.to_sql("raw_products", engine, if_exists="append", index=False)

with DAG(
    dag_id="ecommerce-pipeline",
    start_date=datetime.datetime(2026, 10, 10),
    schedule="@daily",
    catchup=False,
) as my_dag:
    
    
    run_extraction = PythonOperator(
        task_id="run_ecommerce_extract",
        python_callable=extract_data,
    )
    
    run_loading = PythonOperator(
        task_id = "run_postgres_load",
        python_callable = load_to_postgresql,
    )
    
    run_extraction >> run_loading