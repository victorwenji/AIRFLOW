from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
#from airflow.providers.apache.operators.spark_submit import SparkSubmitOperator

from program import ingest_meteo

# Définir les paramètres du DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Définir le DAG
dag = DAG(
    'meteo_dag',
    default_args=default_args,
    description='Un exemple de DAG pour Airflow',
    schedule_interval=timedelta(days=1),  # Exécuter tous les jours
)

spark_task = SparkSubmitOperator(
    task_id='spark_job_task',
    conn_id='spark_default',  # Connexion à la configuration Spark dans Airflow
    application='/home/ubuntu/Downloads/mnmcount/processe/scala/target/scala-2.12/main-scala-mnmc_2.12-1.0.jar',  # Chemin vers le fichier JAR Spark
    name='Spark Job Task',  # Nom de la tâche
    verbose=True,
    conf={
        'spark.master': 'local[*]',  # Spécifier le mode de maître Spark
        'spark.executor.memory': '2g',  # Configuration de la mémoire de l'exécuteur
    },
    dag=dag,
)

# Créer une instance de l'opérateur PythonOperator
task_hello = PythonOperator(
    task_id='print_meteo',
    python_callable=ingest_meteo,
    dag=dag,
)

# Définir l'ordre d'exécution des tâches

task_hello >> spark_task 


