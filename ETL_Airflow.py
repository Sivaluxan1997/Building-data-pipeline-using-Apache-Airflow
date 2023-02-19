#Import the libraries
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

#Define DAGs Arguments
default_args={
    'owner': 'SHIVA',
    'start_date':days_ago(0),
    'email':['siva@gmail.com'],
    'email_on_failure':True,
    'email_on_retry':True,
    'retries':1,
    'retry_delay':timedelta(minutes=5)
}

#Define the DAG
dag=DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1)
)

#Define tasks
#task to unzip data
unzip_data=BashOperator(
    task_id='unzip_data',
    bash_command='tar -xzf /home/project/airflow/dags/finalassignment/tolldata.tgz',
    dag=dag
)

#task to extract data from csv file
extract_data_from_csv=BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d"," -f1-4 vehicle-data.csv >csv_data.csv',
    dag=dag
)

#task to extract data from tsv file
extract_data_from_tsv=BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -d"," -f5-7 tollplaza-data.csv >tsv_data.csv',
    dag=dag
)

#task to extract data from fixed with file
extract_data_from_fixed_width=BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='{print $10,$11}" payment-data.txt > fixed_width_data.csv',
    dag=dag
)

#task to consolidate data extracted from previous tasks
consolidate_data=BashOperator(
    task_id='consolidate_data',
    bash_command='paste csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv',
    dag=dag
)

#transform and load the data
transform_data = BashOperator(
    task_id='transform_data',
    bash_command='tr "[a-z]" "[A-Z]" < extracted_data.csv > transformed_data.csv',
    dag=dag
)

#task pipeline
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data