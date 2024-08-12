import os
import pendulum
from dotenv import load_dotenv
from airflow.models import Variable
from pathlib import Path
from docker.types import Mount
import shutil
load_dotenv()

# DATASET_ROBOFLOW_ENDPOINT
# API_KEY
# BATCH_NAME
# DOCKER_USER
# ROOT_DIR_LOCAL

class AppConst:
    
    DATASET_ROBOFLOW_ENDPOINT=Variable.get('DATASET_ROBOFLOW_ENDPOINT')
    API_KEY=Variable.get('API_KEY')
    DOCKER_USER=Variable.get("DOCKER_USER", "kc")
    BATCH_NAME=Variable.get("BATCH_NAME")

class AppPath:
    
    ROOT_DIR_LOCAL=Path(Variable.get("ROOT_DIR_LOCAL"))
    ROBOFLOW_ANNOTATION_DIR= ROOT_DIR_LOCAL / 'roboflow_annotation_processing'
    DATASET_LOCAL = ROBOFLOW_ANNOTATION_DIR / 'yolov8_dataset'
    DATASET_DIR = Path('/yolov8_dataset')

    
    
class DefaultConfig:
    DEFAULT_DAG_ARGS = {
        "owner": AppConst.DOCKER_USER,
        "retries": 0,
        "retry_delay": pendulum.duration(seconds=20),
    }
    DEFAULT_DOCKER_OPERATOR_ARGS = {
        "image": f"{AppConst.DOCKER_USER}/exe/roboflow_annotation_processing:latest",
        "api_version": "auto",
        "auto_remove": True,
        "mounts": [
            Mount(
                source=AppPath.DATASET_LOCAL.absolute().as_posix(),
                target=str(AppPath.DATASET_DIR),
                type="bind",
            ),
        ],
    }
    
    
