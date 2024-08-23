from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

def ingest_data():
    obj = DataIngestion()
    return obj.initiate_data_ingestion()

def transform_data(ti):
    train_data, test_data = ti.xcom_pull(task_ids='data_ingestion')
    data_transformation = DataTransformation()
    return data_transformation.initiate_data_transformation(train_data, test_data)

def train_model(ti):
    train_arr, test_arr, _ = ti.xcom_pull(task_ids='data_transformation')
    model_trainer = ModelTrainer()
    return model_trainer.initiate_model_trainer(train_arr, test_arr)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 8, 1),
    'retries': 1,
}

with DAG('etl_pipeline_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    data_ingestion = PythonOperator(
        task_id='data_ingestion',
        python_callable=ingest_data
    )
    
    data_transformation = PythonOperator(
        task_id='data_transformation',
        python_callable=transform_data
    )
    
    model_training = PythonOperator(
        task_id='model_training',
        python_callable=train_model
    )

    data_ingestion >> data_transformation >> model_training
