# Demo project to transfer files from GCP to AWS using Airflow

This project is created with the goal to show the cloud integrations on airflow and the ability to
process and transfer files though multi-cloud providers with built-in airflow-operators.

## Purpose

Transfer GCP bucket to AWS bucket using airflow built-in operators (`GoogleCloudStorageToS3Operator`).

## Requirements

- AWS account
- GCP account
- Python 3.7 on installation host (virtualenv installed)

Before proceed with installation, make sure you're using a gcp service-account with the right permissions to access 
bucket objects. You can use: https://console.cloud.google.com/iam-admin/troubleshooter and search 
for `storage.objects.list`.

## Local setup

- __Step 1. Create and activate virtual environment (py3.7):__ (Below steps assumes that you're located on the root project folder location).
You can skip this step if you open your project with PyCharm and create the virtual environment from there.

    - __Step 1.1 - Create virtual environment (optional name, recommended: `venv`):__

        ```shell script
        virtualenv --python=/Library/Frameworks/Python.framework/Versions/3.7/bin/python3 venv   
        ```
        
        _Note:_ First confirm your python version path

    - __Step 1.2 - Activate virtual environment__

        ```shell script
        source venv/bin/activate
        ```

        _Note:_ Once you have created and activated your virtual environment, you need to set it as `python iterpreter` on PyCharm.

    - __Step 1.3 - Dependencies installation:__ (instructions for command line - this can be also done using PyCharm tools, just make sure you're using 
        project virtual environment and not python global installation).
        
        ```shell script
        pip install -r requirements.txt
        ```

- __Step 2 - Initialize airflow and render dags.__

    - __Step 2.1 - Define airflow home:__ open 2 terminals (project root location) and execute below command in both of them. This will let 
    airflow knows which is the folder to use for airflow instance (project application).
    
        ```shell script
        export AIRFLOW_HOME=./airflow
        ```

    - __Step 2.2 - Initialize airflow:__ In one of the terminals where you defined __AIRFLOW_HOME__, execute below command to 
    initialize our airflow instance (after you run it, you'll see more files -related to airflow instance- inside
     $AIRFLOW_HOME directory).

        ```shell script
        airflow initd
        ```  

    - __Step 2.3 - Start airflow:__ This step and the next one will start 2 background processes, both of them requires $AIFLOW_HOME defined.

        - __Step 2.3.1 - Start airflow scheduler:__ In one of the two sessions that we have opened with AIRFLOW_HOME, run below command 
        to start airflow scheduler:
            
            ```shell script
            airflow scheduler
            ```

        - __Step 2.3.2 - Start airflow webserver:__ The only pending thing is turn on our webserver to start running our dags, so in 
        the other terminal run the below command to turn it on (_note:_ you can specify a different port if you want).
            
            ```shell script
            airflow webserver -p 8084
            ```

        - __Step 2.3.3 - Open airflow webserver and verify installation:__ At this point we only need to verify everything is running as 
        expected and our dags (located on $AIRFLOW_HOME/dags/) are rendered on dashboard (_Note:_ Even though webserver should 
        display them almost immediate, refresh the browser after a minute just to make sure. This shouldn't take more than that).
        
            ```shell script
            Open: http://localhost:8084/admin/ 
            ```
- __Step 3 - Cloud accounts configuration.__

    - __Step 3.1 - Airflow connections:__ This step is to define our cloud providers connections and allow authentications 
    for airflow operators.
    
        - __Step 3.1.1 - AWS connection:__ On this example we'll use default connection for aws, in this case 
        is `aws_default`. For this, follow these steps (on webserver):
        
            > Admin -> Click on edit button for `aws_default` connection.

            > Validate that `connection type` is `Amazon Web Services` and `Extra` has the region of your destination bucket.

            > Now, you'll set `Login` with your `AWS_ACCESS_KEY` and `Password` should have `AWS_SECRET_ACCESS_KEY`.

        - __Step 3.1.2 - GCP connection:__ Similar than AWS connection, we'll use default gcp connection (already created 
        by airflow installation):
        
            > Admin -> Click on edit button for `google_cloud_default` connection.

            > Validate that `connection type` is `Google Cloud Platform` and  for `Scopers` assign: `https://www.googleapis.com/auth/cloud-platform`.

            > Now, you'll set `Project Id` depending on your gcp project and `Keyfile JSON` with the content of your service user (Guide: https://cloud.google.com/iam/docs/creating-managing-service-account-keys).

    - __Step 3.2 - Airflow variables:__ Since the POC dag (`airflow/dags/transfer_data_gcp_to_aws_dag.py`) has 
    source (gcp bucket) and destination (aws bucket) parametrized, airflow-variable will store the values for them.
        
        - __Step 3.2.1 - `AWS_BUCKET` variable:__ Go to Admin -> Variables and create a new variable with the 
        name `AWS_BUCKET`. __It's important the format of the bucket name,__ ensure that you have a valid 
        format like: `s3://aws-destination-bucket/`.
        
        - __Step 3.2.1 - `GCP_BUCKET` variable:__ Go to Admin -> Variables and create a new variable with the 
        name `GCP_BUCKET`. For this variable, gcp operator does not require prefix (gcs) on the bucket name, 
        a valid bucket name for `GCP_BUCKET` is:  `gcp-source-bucket`.
    
    - __Step 3.3 - Local AWS config:__ AWS works with `boto3`, therefore we need to create a file for aws-account 
    authentication. For this we need to run:
    
        ````shell script
        touch ~/.boto
        ````
    The content for `.boto` should be:
      
    ```shell script
    [Credentials]
    aws_access_key_id = YOUR_ACCESS_KEY
    aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
    ```

And that's all, you can test the dag with a manual run and then schedule it as per your needs.

__References:__
- https://airflow.apache.org/
- https://airflow.apache.org/docs/stable/howto/connection/aws.html
- https://airflow.apache.org/docs/stable/howto/connection/gcp.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- https://cloud.google.com/iam/docs/creating-managing-service-account-keys
