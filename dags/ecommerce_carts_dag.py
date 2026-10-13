import os
import json
import glob
import datetime
import pandas as pd
from airflow import DAG
from datetime import timedelta
from sqlalchemy import create_engine
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from extractors.extract_carts import extract_cart_data




def load_to_postgres():
    engine = create_engine("postgresql://airflow:airflow@postgres:5432/airflow")
    search_path = "/opt/airflow/data/raw/carts/**/*.json"
    list_of_files = glob.glob(search_path, recursive=True)
    
    if not list_of_files:
        raise FileNotFoundError("No raw json file found")
    
    latest_file = max(list_of_files, key=os.path.getctime)
    
    df = pd.read_json(latest_file)
    
    for col in df.columns:
        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)
        
    try:
        with engine.begin() as conn:
            conn.exec_driver_sql("TRUNCATE TABLE raw_carts;")
    except:
        pass
    
    df.to_sql("raw_carts", engine, if_exists="append", index=False)
    
with DAG(
    dag_id="ecommerce-pipeline_cart",
    start_date=datetime.datetime(2026, 10, 12),
    # schedule="0 */4 * * *", four hours,
    schedule = timedelta(hours=4),
    catchup=False,
) as my_dag:
    
    run_extraction = PythonOperator(
        task_id="run_ecommerce_extract",
        python_callable=extract_cart_data,
    )
    
    run_loading = PythonOperator(
        task_id="run_postgres_loading",
        python_callable=load_to_postgres,
    )
    
    
    run_extraction >> run_loading