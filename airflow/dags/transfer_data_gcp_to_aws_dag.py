from airflow import DAG
from airflow.contrib.operators.gcs_to_s3 import GoogleCloudStorageToS3Operator
from airflow.contrib.operators.gcs_list_operator import GoogleCloudStorageListOperator
from airflow.contrib.operators.s3_list_operator import S3ListOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

DAG_ID = "transfer_data_gcp_to_aws_dag"

# To have bucket names parametrized
AWS_BUCKET = Variable.get("AWS_BUCKET")
GCP_BUCKET = Variable.get("GCP_BUCKET")

def_args = {
    'start_date': days_ago(1),
    'owner': 'cm0'
}

transfer_dag = DAG(dag_id=DAG_ID, schedule_interval=None, default_args=def_args)

start = DummyOperator(task_id="start", dag=transfer_dag)

transfer_operator = GoogleCloudStorageToS3Operator(
    task_id="transfer_gcp_to_aws",
    bucket=GCP_BUCKET,
    dest_s3_key=AWS_BUCKET,
    replace=True,
    dag=transfer_dag)

end = DummyOperator(task_id="end", dag=transfer_dag)

# For troubleshooting GCP and AWS resources access, you can uncomment below operators which will list
# both buckets. Not recommendable for recursive listing or for buckets without inner folders (where there are
# many files directly on the bucket root). Also required to comment line 41.

# list_gcs = GoogleCloudStorageListOperator(task_id="list_gcs", bucket=GCP_BUCKET, dag=transfer_dag)
# list_s3 = S3ListOperator(task_id="list_s3", bucket=AWS_BUCKET, dag=transfer_dag)
# start >> list_gcs >> list_s3 >> transfer_operator >> end


start >> transfer_operator >> end
