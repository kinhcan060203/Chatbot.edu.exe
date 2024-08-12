import pendulum
from airflow import DAG
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from utils import *
from airflow.providers.docker.operators.docker import DockerOperator


with DAG(
    dag_id="roboflow_annotation_processing",
    default_args=DefaultConfig.DEFAULT_DAG_ARGS,
    schedule_interval="@once",
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    tags=["annotation_processing",'roboflow'],
) as dag:

    download = DockerOperator(
        task_id="download_dataset",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
        command="/bin/bash -c 'rm -rf $DATASET_DIR/train && roboflow download -f yolov8 -l $DATASET_DIR $DATASET_ROBOFLOW_ENDPOINT'",
        environment={
            'DATASET_ROBOFLOW_ENDPOINT':str(AppConst.DATASET_ROBOFLOW_ENDPOINT),
            'DATASET_DIR':str(AppPath.DATASET_DIR),
            'ROBOFLOW_API_KEY':str(AppConst.API_KEY),
        }
    )
    process = DockerOperator(
        task_id="process_annotations",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
        command="/bin/bash -c 'cd src && python main.py --stage process'",
        environment={k: str(v) for k, v in {**AppConst.__dict__,**AppPath.__dict__}.items() if not k.startswith('__')}
    )
    upload = DockerOperator(
        task_id="upload_dataset",
        **DefaultConfig.DEFAULT_DOCKER_OPERATOR_ARGS,
        command="/bin/bash -c 'cd src && python main.py --stage upload'",
        environment={k: str(v) for k, v in {**AppConst.__dict__,**AppPath.__dict__}.items() if not k.startswith('__')}
    )


    download >> process >> upload