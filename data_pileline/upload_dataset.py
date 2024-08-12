import sys
import os
from pathlib import Path
from roboflow import Roboflow

class AppConst:
    API_KEY='P9u4Gv7KpjY40hLjG5Yp'
    WORKSPACE='kinhcan'
    DATASET_DIR=Path('data_pileline/systhesis_data')
    PROJECT='exe2'
    
def upload_dataset():
    rf = Roboflow(api_key=AppConst.API_KEY)
    
    images_dir = AppConst.DATASET_DIR / 'images' 
    labelmap_path = AppConst.DATASET_DIR / 'darknet.labels'
    annotations_dir = AppConst.DATASET_DIR / 'labels' 

    project = rf.workspace(AppConst.WORKSPACE).project(AppConst.PROJECT)
    subject_list = [path.stem for path in sorted(images_dir.glob('*'))]
    for subject in subject_list:
        print("---Subject:",subject)
        image_glob = sorted((images_dir / subject).glob('*.jpg'))
        annotation_glob = sorted((annotations_dir / subject).glob('*.txt'))
        for image_path, annotation_path in zip(image_glob,annotation_glob):
            print(project.single_upload(
                image_path=str(image_path),
                annotation_path=str(annotation_path),
                annotation_labelmap=str(labelmap_path),
                split='train',
                num_retry_uploads=5,
                batch_name=str(subject),
                tag_names=["HA1",str(subject)],
                annotation_overwrite=True,
            ))


if __name__=='__main__':
    upload_dataset()
