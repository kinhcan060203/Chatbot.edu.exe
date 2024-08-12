import json
import numpy as np
import os
import yaml
from dotenv import load_dotenv
from pathlib import Path
import shutil
load_dotenv()

# DATASET_ROBOFLOW_ENDPOINT
# API_KEY
# DOCKER_USER
# BATCH_NAME
    
class AppPath:
    DATASET_DIR = Path(os.environ.get('DATASET_DIR'))
    CONNECT_JSONL_FILE = DATASET_DIR / 'connection.jsonl'
    IMAGE_DIR = DATASET_DIR / 'train' / 'images'
    ANNOTATION_DIR = DATASET_DIR / 'train' / 'labels'
    (DATASET_DIR).mkdir(parents=True, exist_ok=True)
    
class AppConst:
    
    CLASS_MAP={}
    LABEL_MAP={}
    
    if (AppPath.DATASET_DIR / 'data.yaml').exists():
        with open(AppPath.DATASET_DIR / 'data.yaml', 'r') as file:
            labels = yaml.safe_load(file)['names']
            LABEL_MAP = {index: label for index, label in enumerate(labels)}
            CLASS_MAP = {label: index for index, label in enumerate(labels)}
            
    CONNECT_INDEX = CLASS_MAP.get('connect',-1)
    MERGE_INDEX = CLASS_MAP.get('merge',-1)
        
    DEFAULT_COLUMNS = ['class', 'x_center', 'y_center', 'width', 'height']
    
    DATASET_ROBOFLOW_ENDPOINT=os.environ.get('DATASET_ROBOFLOW_ENDPOINT')
    WORKSPACE= DATASET_ROBOFLOW_ENDPOINT.split('/')[0]
    PROJECT= DATASET_ROBOFLOW_ENDPOINT.split('/')[1]
    VERSION= DATASET_ROBOFLOW_ENDPOINT.split('/')[2]
    
    API_KEY=os.environ.get('API_KEY')
    BATCH_NAME=os.environ.get('BATCH_NAME')
    DOCKER_USER=os.environ.get("DOCKER_USER")
    
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)
    
